"""MCP server that exposes a single tool to run shell commands."""

from __future__ import annotations

import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Shell server")

_DEFAULT_TIMEOUT = 120


@mcp.tool(
    name="terminal_tool",
    title="Terminal tool",
    description="Run a shell command in the system shell and return exit code, stdout, and stderr.",
)
def terminal_tool(
    command: str,
    working_directory: str | None = None,
    timeout_seconds: int = _DEFAULT_TIMEOUT,
) -> str:
    try:
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=working_directory or None,
        )
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout_seconds} seconds."
    except OSError as e:
        return f"Failed to run command: {e}"

    stdout = completed.stdout if completed.stdout else "(empty)"
    stderr = completed.stderr if completed.stderr else "(empty)"
    return (
        f"Exit code: {completed.returncode}\n\n"
        f"stdout:\n{stdout}\n\n"
        f"stderr:\n{stderr}"
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
