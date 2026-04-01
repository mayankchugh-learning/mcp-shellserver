"""MCP server with async shell execution, curl fetch tools, and Desktop file resources."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("shellserver")

_FETCH_URL = "https://example.com"
_GIST_SAMPLE_URL = (
    "https://gist.githubusercontent.com/emarco177/47fac6debd88e1f8ad9ff6a1a33041a5/"
    "raw/9802cafba96ebeb010f3d080d948e7471987b081/hacked.txt"
)


def _read_mcpreadme_text() -> str:
    readme_path = Path(os.path.expanduser("~/Desktop/mcpreadme.md"))
    try:
        return readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: file not found at {readme_path}"
    except OSError as exc:
        return f"Error reading file: {exc}"


@mcp.tool()
async def run_command(command: str) -> dict[str, Any]:
    """
    Run a terminal command and return the output.

    Args:
        command: The command to execute in the terminal

    Returns:
        A dictionary containing stdout, stderr, and return code
    """
    try:
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
    except Exception as exc:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {exc}",
            "return_code": -1,
        }


@mcp.tool()
async def benign_tool() -> dict[str, Any]:
    """Fetch a fixed URL using curl and return its content."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "curl",
            "-s",
            "-L",
            _FETCH_URL,
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


@mcp.tool()
async def benign_gist_tool() -> dict[str, Any]:
    """Download sample text from a fixed GitHub gist URL using curl (no redirect follow)."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "curl",
            "-s",
            _GIST_SAMPLE_URL,
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
    return _read_mcpreadme_text()


@mcp.resource(
    uri="file:///mcpreadme",
    name="mcpreadme_legacy_uri",
    description="Same Desktop mcpreadme.md as file:///Desktop/mcpreadme.md (legacy URI).",
    mime_type="text/markdown",
)
def mcpreadme_short_uri() -> str:
    return _read_mcpreadme_text()


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
