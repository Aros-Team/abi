import json
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage

from app.agents.prompts import build_system_prompt
from app.agents.tools.sql_query import sql_query
from app.models.business import restaurant_context
from app.config import settings


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


async def stream_agent(
    agent, messages: list[tuple[str, str]], session_id: str | None = None
):
    response_text = []
    in_tool_process = False

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

    yield format_sse(session_id or "", "[DONE]")
