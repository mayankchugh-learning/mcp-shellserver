import sys

from mcp.server.fastmcp import FastMCP

# SSE on :8001 (weather uses :8000). Logs to stderr appear in this terminal.
mcp = FastMCP("Math", port=8001)


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    _log("---------------start-----------------")
    _log("This is the log from math MCP (SSE)")
    _log(f"Adding {a} and {b}")
    _log("---------------end-----------------")
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    _log("---------------start-----------------")
    _log("This is the log from math MCP (SSE)")
    _log(f"Multiplying {a} and {b}")
    _log("---------------end-----------------")
    return a * b


if __name__ == "__main__":
    mcp.run(transport="sse")
