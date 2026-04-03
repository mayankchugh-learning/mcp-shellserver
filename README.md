# research-prompt-mcp (shellserver)

FastMCP server that exposes a **research prompt** and a small **tool** used to verify Claude Desktop wiring.

**Requirements:** Python **3.13+** (see [`pyproject.toml`](pyproject.toml)), [**uv**](https://docs.astral.sh/uv/), and **Node.js** (for `npx`, used by `fastmcp dev inspector`).

**More help:** [`troubleshooting.md`](troubleshooting.md) (Inspector flows, ports, Claude Desktop, common errors).

## GitHub & repository setup

### `.gitignore`

This repo includes a [`.gitignore`](.gitignore) so typical local and sensitive files are not committed:

- Virtual environments (`.venv/`, `venv/`, …)
- **`.env` and `.env.*`** (secrets); use **`.env.example`** (optional) for non-secret keys only
- Python caches, build artifacts, eggs, wheels
- Test/coverage/linter caches
- Common IDE folders (`.idea/`, `.vscode/`)

If a tool asks you to “add a `.gitignore`”, use this file as the project default.

### `requirements.txt` and uv

[`requirements.txt`](requirements.txt) lists direct dependencies in **pip-style** form (kept in line with [`pyproject.toml`](pyproject.toml)).

**Import packages from `requirements.txt` into the project** (updates `pyproject.toml` / lockfile workflow):

```bash
uv add -r requirements.txt
```

**Install from the lockfile** (usual day-to-day after `pyproject.toml` is already correct):

```bash
uv sync
```

Prefer editing **`pyproject.toml`** for new deps, then `uv lock` / `uv sync`, and refresh `requirements.txt` when you need a pip-compatible export.

## Git: new orphan branch (clean history)

Use this when you want a **fresh branch with no parent commits**, but you keep your **current working tree**—then make that tree the **first commit** on the new line.

Replace the branch name and commit message as needed.

```bash
git switch --orphan project/langchain-mcp-adapters-clean
git add -A
git commit -m "Initial commit for langchain MCP adapters"
```

- **`git switch --orphan <branch>`** creates the branch and resets the index; your files stay as unstaged/untracked until you add.
- **`git add -A`** stages everything; **do not** stage secrets (e.g. `.env`). Ensure `.env` is in `.gitignore` before committing.

To publish (only after the commit is safe to push):

```bash
git push -u origin project/langchain-mcp-adapters-clean
```

## Claude Desktop

### Config file (Windows)

Add the server under `mcpServers` in:

`%APPDATA%\Claude\claude_desktop_config.json`

Example (adjust paths if your checkout differs):

```json
{
  "mcpServers": {
    "research-prompt-mcp": {
      "command": "C:\\githunb\\mcp-servers\\shellserver\\.venv\\Scripts\\python.exe",
      "args": ["C:\\githunb\\mcp-servers\\shellserver\\main.py"]
    }
  }
}
```

Quit Claude completely (including background/tray), then restart after editing the config.

### Stdio vs HTTP

Claude Desktop starts your process and speaks MCP over **stdio** (stdin/stdout). Running this repo’s `main.py` **without** extra arguments uses stdio (`mcp.run()`).

Do **not** point Claude Desktop at HTTP-only mode: that transport does not match what the desktop app expects, so the connector may fail to load or behave oddly.

For browser **MCP Inspector** with **Streamable HTTP**, the server must listen on HTTP (see `fastmcp.json` and [MCP Inspector](#mcp-inspector)). The **`--http`** flag is for running that mode manually via `python main.py --http` (see [Run](#run)).

### Prompts vs tools in the UI

- **`@mcp.tool()`** functions appear under **Settings → Connectors →** your server → **Tool permissions**.
- **`@mcp.prompt()` entries do not** show in that tool list; they are prompts you pick from the chat / prompt UI (wording varies by Claude version).

This project includes `ping_research_server` so you can confirm tools are listed after a restart.

### Other editors (e.g. Cursor)

Configure MCP in that product’s settings (workspace or user). This repo may include a placeholder [`mcp.json`](mcp.json); wire it per your editor’s docs—often the same **stdio** pattern as Claude (`python` + `main.py`).

## Local dev ports (reference)

| Port | Role |
|------|------|
| **8000** | Streamable HTTP MCP endpoint (`/mcp`) when using [`fastmcp.json`](fastmcp.json) or `python main.py --http` |
| **6274** | MCP Inspector **browser UI** (default) |
| **6277** | MCP Inspector **proxy** (default; used with “Via Inspector Proxy”) |

## Run

**Stdio** (Claude Desktop, Cursor, and most local MCP clients):

```bash
uv run python main.py
```

**HTTP + CORS** (e.g. MCP Inspector in Direct mode on `localhost:6274`):

```bash
uv run python main.py --http
```

**Stdio via CLI** (same as `python main.py`; no HTTP on 8000):

```bash
uv run fastmcp run main.py
```

**Streamable HTTP via CLI** (uses deployment in [`fastmcp.json`](fastmcp.json); no Inspector UI):

```bash
uv run fastmcp run fastmcp.json
```

> **Browser Inspector + Direct to `8000`:** the **`CORSMiddleware`** and **`expose_headers`** in `main.py` run only on **`python main.py --http`** (the `if __name__ == "__main__"` path). If the Inspector shows **CORS** or **Missing session ID** while using **`fastmcp dev inspector fastmcp.json`** with **Direct**, run **`uv run python main.py --http`** in a second terminal instead, or see **section 11** in [`troubleshooting.md`](troubleshooting.md).

## MCP Inspector

[`fastmcp.json`](fastmcp.json) sets **`streamable-http`** on **`127.0.0.1:8000`** so a Streamable HTTP client can connect. If you run `fastmcp dev inspector main.py` (file only), FastMCP defaults that process to **stdio**, so **nothing listens on port 8000** and the Inspector shows a connection error for `http://localhost:8000/mcp`.

From the project root, start the stack using the config file:

```bash
uv run fastmcp dev inspector fastmcp.json
```

Or auto-detect `fastmcp.json` in the current directory:

```bash
uv run fastmcp dev inspector
```

**Stdio-only dev** (no HTTP on 8000; use the URL + token the CLI prints):

```bash
uv run fastmcp dev inspector main.py
```

In the Inspector UI use:

- **Transport:** Streamable HTTP  
- **URL:** `http://127.0.0.1:8000/mcp` (prefer this over `localhost` on Windows if IPv6 causes issues)  
- **Connection type:** Direct  

If you still see auth-related errors, clear **Proxy Session Token** when using **Direct**, or switch to **Via Inspector Proxy** and fill **Inspector Proxy Address** plus the token from the terminal output.

## See also

- [`troubleshooting.md`](troubleshooting.md) — flows, **127.0.0.1** vs **localhost**, port in use, `PromptMessage` import, proxy token
- [`fastmcp.json`](fastmcp.json) — `streamable-http` on **127.0.0.1:8000**
