import sys

from fastmcp import FastMCP
from mcp.server.streamable_http import (
    LAST_EVENT_ID_HEADER,
    MCP_PROTOCOL_VERSION_HEADER,
    MCP_SESSION_ID_HEADER,
)
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("research-prompt-mcp")

# Lets the MCP Inspector UI (port from env CLIENT_PORT, default 6274) call this server in "Direct" mode.
_INSPECTOR_ORIGINS = (
    "http://localhost:6274",
    "http://127.0.0.1:6274",
)
# Browsers hide response headers from JS unless listed here; Streamable HTTP needs
# mcp-session-id on follow-up POSTs.
_CORS_EXPOSE_HEADERS = (
    MCP_SESSION_ID_HEADER,
    MCP_PROTOCOL_VERSION_HEADER,
    LAST_EVENT_ID_HEADER,
)


from mcp.types import PromptMessage, TextContent

@mcp.prompt()
def deep_research_prompt(topic: str, depth: str = "comprehensive") -> list[PromptMessage]:
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"You are a senior research analyst. Your task is a {depth} study."
            )
        ),
        PromptMessage(
            role="user", 
            content=TextContent(
                type="text",
                text=f"Research topic: {topic}\n\nProvide sources, key insights, and a summary."
            )
        ),
    ]

@mcp.prompt(
    name="research_assistant",          # overrides function name
    description="Generates a structured research prompt for any topic"
)
def get_research_prompt(topic: str, style: str = "academic") -> str:
    return f"Research '{topic}' in a {style} style. Include citations."



@mcp.tool()
def ping_research_server() -> str:
    """Sanity check that research-prompt-mcp tools are loaded in Claude Desktop."""
    return "ok"


if __name__ == "__main__":
    # Claude Desktop (and most local MCP clients) expect stdio transport, not HTTP.
    if "--http" in sys.argv:
        mcp.run(
            "http",
            host="127.0.0.1",
            port=8000,
            middleware=[
                Middleware(
                    CORSMiddleware,
                    allow_origins=list(_INSPECTOR_ORIGINS),
                    allow_methods=["*"],
                    allow_headers=["*"],
                    expose_headers=list(_CORS_EXPOSE_HEADERS),
                ),
            ],
        )
    else:
        mcp.run()
