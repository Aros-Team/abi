import json
import logging
from httpx import ConnectError, TimeoutException
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage

from app.agents.prompts import build_system_prompt
from app.agents.tools.sql_query import sql_query
from app.models.business import restaurant_context
from app.config import settings
from app.services.session_store import session_store

logger = logging.getLogger(__name__)


def format_sse(content: str, prefix: str = "") -> str:
    escaped = content.replace("\n", "\\n")
    prefix_str = f"{prefix} " if prefix else "data: "
    return f"{prefix_str}{escaped}\n\n"


def create_business_agent():
    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=settings.deepseek_api_key,
        temperature=0,
    )

    tools = [sql_query]

    system_prompt = build_system_prompt(restaurant_context)

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt,
    )

    return agent


def invoke_agent(agent, message: str, session_id: str | None = None) -> dict:
    response = agent.invoke({"messages": [("human", message)]})

    return {
        "answer": response.get("output", ""),
        "session_id": session_id or "",
    }


class AgentStreamError(Exception):
    def __init__(self, message: str, error_type: str = "unknown"):
        self.message = message
        self.error_type = error_type
        super().__init__(message)


def _safe_error_message(error: Exception) -> str:
    error_type = type(error).__name__

    if isinstance(error, ConnectError):
        return (
            "No se pudo conectar al proveedor de IA. Verifica tu conexión a internet."
        )
    elif isinstance(error, TimeoutException):
        return "El proveedor de IA no respondió a tiempo. Por favor intenta de nuevo."
    elif "api_key" in str(error).lower() or "auth" in str(error).lower():
        return "Error de autenticación con el proveedor de IA."
    elif "rate_limit" in str(error).lower() or "429" in str(error):
        return "Demasiadas solicitudes. Por favor espera un momento e intenta de nuevo."
    elif "deepseek" in str(error).lower():
        return "El servicio de IA no está disponible temporalmente."
    else:
        logger.error(f"[AGENT] Unexpected error: {error_type}: {error}")
        return "Ocurrió un error inesperado. Por favor intenta de nuevo."


async def stream_agent(
    agent, messages: list[tuple[str, str]], session_id: str | None = None
):
    response_text = []
    in_tool_process = False
    error_occurred = False
    error_message = ""

    try:
        async for event in agent.astream_events({"messages": messages}, version="v1"):
            event_type = event.get("event", "")

            if event_type == "on_chat_model_stream":
                content = event.get("data", {}).get("chunk", {}).content
                if content:
                    response_text.append(content)
                    if in_tool_process:
                        yield format_sse(content, "[PROCESS]")
                    else:
                        yield format_sse(content)

            elif event_type == "on_tool_start":
                tool_name = event.get("name", "unknown")
                in_tool_process = True
                yield format_sse(tool_name, "[TOOL_CALL]")

            elif event_type == "on_tool_end":
                in_tool_process = False
                tool_output = event.get("data", {}).get("output", {})
                if isinstance(tool_output, dict):
                    if tool_output.get("success"):
                        rows = tool_output.get("row_count", 0)
                        yield format_sse(f"{rows} filas encontradas", "[TOOL_RESULT]")
                    else:
                        error = tool_output.get("error", "error desconocido")
                        yield format_sse(f"Error: {error}", "[TOOL_RESULT]")

    except (ConnectError, TimeoutException) as e:
        error_occurred = True
        error_message = _safe_error_message(e)
        logger.error(f"[AGENT] Connection error: {e}")
        yield format_sse(error_message, "[ERROR]")

    except Exception as e:
        error_occurred = True
        error_message = _safe_error_message(e)
        logger.error(f"[AGENT] Unexpected error: {type(e).__name__}: {e}")
        yield format_sse(error_message, "[ERROR]")

    finally:
        yield format_sse(session_id or "", "[DONE]")

    if error_occurred and session_id:
        session_store.add_message(
            session_id, "user", messages[-1][1] if len(messages) > 1 else ""
        )
        session_store.add_message(session_id, "assistant", f"[ERROR] {error_message}")
