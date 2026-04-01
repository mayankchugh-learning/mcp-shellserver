"""MCP server with async shell execution, a benign fetch tool, and a Desktop file resource."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shellserver")

_FETCH_URL = "https://example.com"


@mcp.tool()
async def run_command(command: str) -> dict[str, Any]:
    """
    Run a terminal command and return the output.
    
    Args:
        command: The command to execute in the terminal
        
    Returns:
        A dictionary containing stdout, stderr, and return code
    """
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout_bytes, stderr_bytes = await proc.communicate()
    return {
        "stdout": stdout_bytes.decode(errors="replace"),
        "stderr": stderr_bytes.decode(errors="replace"),
        "return_code": proc.returncode,
    }


@mcp.tool()
async def benign_tool() -> dict[str, Any]:
    """Fetch a fixed URL using curl and return its content."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "curl", "-s", "-L", _FETCH_URL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        if proc.returncode != 0:
            return {
                "content": "",
                "error": stderr_bytes.decode(errors="replace"),
                "success": False,
            }
        return {
            "content": stdout_bytes.decode(errors="replace"),
            "error": "",
            "success": True,
        }
    except Exception as exc:
        return {
            "content": "",
            "error": str(exc),
            "success": False,
        }


@mcp.resource(
    uri="file:///Desktop/mcpreadme.md",
    name="mcpreadme",
    description="Contents of mcpreadme.md from the user's Desktop.",
    mime_type="text/markdown",
)
def mcpreadme() -> str:
    readme_path = Path(os.path.expanduser("~/Desktop/mcpreadme.md"))
    try:
        return readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: file not found at {readme_path}"
    except OSError as exc:
        return f"Error reading file: {exc}"


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
