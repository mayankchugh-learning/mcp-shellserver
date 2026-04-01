# shellserver

A small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server written in Python with the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

It exposes:

- **`run_command`** — run a shell command and return `stdout`, `stderr`, and `return_code` (or `-1` with an error message if setup fails).
- **`benign_tool`** — fetch a fixed URL (`https://example.com`) with `curl -s -L` and return the body (or an error).
- **`benign_gist_tool`** — fetch a fixed sample gist URL with `curl -s` (no `-L`), matching the older `server-last.py` demo.
- **Resources `mcpreadme`** — read `mcpreadme.md` from the current user’s Desktop, available as `file:///Desktop/mcpreadme.md` or legacy `file:///mcpreadme`.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or another way to install dependencies from `pyproject.toml`
- **`benign_tool`** and **`benign_gist_tool`** need `curl` on your `PATH`.

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
| URIs | `file:///Desktop/mcpreadme.md` (primary), `file:///mcpreadme` (legacy alias, same file) |
| MIME type | `text/markdown` |
| Description | Reads `mcpreadme.md` from the current user’s Desktop (`~/Desktop/mcpreadme.md` on Unix; on Windows this resolves under your user profile’s Desktop). Returns a descriptive message if the file is missing or unreadable. |

## Tool: `run_command`

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Shell command to run |

**Returns:** `stdout`, `stderr`, and `return_code` (dictionary).

**Security:** This executes arbitrary shell commands as your user. Only connect it in environments you trust, or harden it (for example allowlists or sandboxing) before wider use.

## Tool: `benign_tool`

No parameters. Runs `curl -s -L` against a fixed URL bundled in the server.

**Returns:** `content`, `error`, and `success` (dictionary).

## Tool: `benign_gist_tool`

No parameters. Runs `curl -s` (no redirect follow) against a fixed raw gist URL bundled in the server.

**Returns:** `content`, `error`, and `success` (dictionary).

## Example MCP client configuration

Adjust paths to match your machine.

**Windows (example path):**

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
  }
}
```

**Unix:** use a POSIX path in `--directory` (for example `/home/you/mcp-servers/shellserver`).
