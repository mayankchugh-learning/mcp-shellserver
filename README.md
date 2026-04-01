# shellserver

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server written in Python with the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). It exposes one tool so a client can run shell commands and read exit code, stdout, and stderr.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or another way to install dependencies from `pyproject.toml`

## Install and run

From this directory:

```bash
uv sync
uv run shellserver
```

The server uses **stdio** transport (default for `FastMCP`), which suits MCP clients that spawn a subprocess and talk over standard input/output.

You can also run:

```bash
uv run python server.py
```

## Resource: `mcpreadme`

| Field | Value |
|-------|-------|
| URI | `file:///Desktop/mcpreadme.md` |
| MIME type | `text/markdown` |
| Description | Reads `mcpreadme.md` from the current user's Desktop (`~/Desktop/mcpreadme.md`) and returns its contents as a string. Returns a descriptive error message if the file is missing or unreadable. |

## Tool: `terminal_tool`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `command` | string | (required) | Shell command to run |
| `working_directory` | string | `null` | Working directory for the process |
| `timeout_seconds` | integer | `120` | Timeout in seconds |

**Security:** This executes arbitrary shell commands as your user. Only connect it in environments you trust, or harden it (e.g. allowlists, sandboxing) before wider use.

## Example MCP client configuration

Adjust paths to match your machine.

```json
{
  "mcpServers": {
    "shellserver": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\githunb\\mcp-servers\\shellserver",
        "server.py"
      ]
    }
},

  "preferences": {
    "coworkWebSearchEnabled": true,
    "coworkScheduledTasksEnabled": true,
    "ccdScheduledTasksEnabled": true
  }
}
```

On Unix, use a POSIX path in `--directory`.
