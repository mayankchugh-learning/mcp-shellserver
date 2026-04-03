from fastmcp import FastMCP
from mcp.server.streamable_http import (
    LAST_EVENT_ID_HEADER,
    MCP_PROTOCOL_VERSION_HEADER,
    MCP_SESSION_ID_HEADER,
)
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("research-prompt-mcp")

# Lets the MCP Inspector UI (localhost:6274) call this server in "Direct" mode.
_INSPECTOR_ORIGINS = ("http://localhost:6274", "http://127.0.0.1:6274")
# Browsers hide response headers from JS unless listed here; Streamable HTTP needs
# mcp-session-id on follow-up POSTs.
_CORS_EXPOSE_HEADERS = (
    MCP_SESSION_ID_HEADER,
    MCP_PROTOCOL_VERSION_HEADER,
    LAST_EVENT_ID_HEADER,
)

@mcp.prompt()
def get_research_prompt(topic: str) -> str:
    return f"Please research the following topic: {topic}"

if __name__ == "__main__":
    mcp.run(
        "http",
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
