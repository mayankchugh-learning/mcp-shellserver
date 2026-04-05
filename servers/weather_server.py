import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    _log("---------------start-----------------")
    _log("This is the log from SSE server")
    _log(f"Getting weather for {location}")
    _log("---------------end-----------------")
    return "Hot as hells"


if __name__ == "__main__":
    mcp.run(transport="sse")
