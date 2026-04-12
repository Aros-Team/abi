import uuid
import asyncio
from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from app.models.chat import ChatRequest
from app.agents.factory import create_business_agent, stream_agent
from app.services.session_store import session_store

router = APIRouter()

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = create_business_agent()
    return _agent


@router.post(
    "/chat/stream",
    tags=["Chat"],
    summary="Chat con streaming SSE",
    description="Envía un mensaje y recibe la respuesta del agente en chunks SSE. "
    "El stream termina con 'data: [DONE] session_id'. "
    "Usa el session_id retornado para continuar la conversación.",
    responses={
        200: {
            "description": "Stream SSE con respuesta del agente",
            "content": {"text/event-stream": {}},
        }
    },
)
async def chat_stream(request: ChatRequest, response: Response):
    """
    Chat streaming SSE para el agente BI de restaurante.

    - **message**: Pregunta en lenguaje natural

    El response es un stream SSE donde cada chunk llega como:
    `data: contenido_del_chunk\\n\\n`

    Eventos especiales:
    - `data: [TOOL_CALL] nombre_herramienta\\n\\n` - cuando se usa una herramienta
    - `data: [TOOL_RESULT] resultado\\n\\n` - cuando la herramienta termina
    - `data: [DONE] session_id\\n\\n` - cuando termina la conversación
    """
    session_id = str(uuid.uuid4())

    response.headers["X-Request-ID"] = session_id

    agent = get_agent()

    history = session_store.get_history(session_id)
    messages = (
        [("system", build_system_prompt_content())]
        + history
        + [("human", request.message)]
    )

    response_buffer = []

    async def generate():
        nonlocal response_buffer
        agen = stream_agent(agent, messages, session_id)
        async for chunk in agen:
            if chunk.startswith("data: [DONE]"):
                session_store.add_message(session_id, "user", request.message)
                full_response = "".join(response_buffer)
                session_store.add_message(session_id, "assistant", full_response)
            elif chunk.startswith("data: [TOOL_CALL]") or chunk.startswith(
                "data: [TOOL_RESULT]"
            ):
                response_buffer.append("")
                yield chunk
            else:
                if response_buffer:
                    response_buffer[-1] += chunk.replace("data: ", "").replace(
                        "\n\n", ""
                    )
                else:
                    response_buffer.append(
                        chunk.replace("data: ", "").replace("\n\n", "")
                    )
                yield chunk
            await asyncio.sleep(0)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Request-ID": session_id,
            "X-Accel-Buffering": "no",
        },
    )


def build_system_prompt_content() -> str:
    from app.agents.prompts import build_system_prompt
    from app.models.business import restaurant_context

    return build_system_prompt(restaurant_context)
