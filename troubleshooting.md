# Troubleshooting: FastMCP + MCP Inspector + Claude Desktop (Windows / local dev)

This document records issues seen with this project (**FastMCP**, **MCP Inspector**, **Claude Desktop**), including **symptoms**, **root cause**, and **what to do**.

---

## Architecture (pick one flow; do not mix incompatible settings)

### Flow A — `uv run fastmcp dev inspector main.py` (stdio server)

- Starts the **Inspector UI** (default **6274**) and an **Inspector proxy** (default **6277**).
- Runs **`fastmcp run main.py`**, which loads your `FastMCP` instance and uses **stdio** by default. **No HTTP listener on port 8000** for your app.
- The typical wiring is: browser ↔ Inspector ↔ **proxy** ↔ Python process (**stdio**).
- In the Inspector, do **not** expect **Streamable HTTP → Direct → `http://localhost:8000/mcp`** to work unless you also start an HTTP server (Flow B or C).

### Flow B — HTTP server only (manual Streamable HTTP)

- Run **`uv run python main.py --http`** (see `main.py`; **without** `--http`, `main.py` uses **stdio**).
- Server listens on **`127.0.0.1:8000`** with path **`/mcp`** (Streamable HTTP).
- In the Inspector: **Streamable HTTP**, URL **`http://127.0.0.1:8000/mcp`**, **Connection type: Direct**.
- **`main.py`** must include **CORS** for Inspector origins and **`expose_headers`** for **`mcp-session-id`** (see `main.py`).

### Flow C — `uv run fastmcp dev inspector fastmcp.json` (recommended Streamable HTTP + dev inspector)

- This repo’s **[`fastmcp.json`](fastmcp.json)** sets **`deployment.transport`** to **`streamable-http`** and **`127.0.0.1:8000`**.
- The subprocess runs **`fastmcp run fastmcp.json`**, which **does** bind **8000** for Streamable HTTP.
- From the project root:
  - **`uv run fastmcp dev inspector fastmcp.json`**, or
  - **`uv run fastmcp dev inspector`** (auto-detects **`fastmcp.json`** in the current directory).
- Then in the Inspector use **Streamable HTTP**, **`http://127.0.0.1:8000/mcp`**, **Direct** (prefer **`127.0.0.1`** over **`localhost`** on Windows if IPv6 causes odd failures).

**Summary:** **`fastmcp dev inspector main.py`** alone does **not** open **`8000/mcp`**. Use **Flow C** or **Flow B** for that URL.

---

## Claude Desktop

### Connector never appears / errors on connect

| Item | Detail |
|------|--------|
| **Symptom** | Server never shows under Connectors after editing config and restarting. |
| **Root cause** | Claude Desktop uses **stdio** (stdin/stdout). If **`main.py`** only runs **`mcp.run("http", …)`** or HTTP-only mode, the process does not speak MCP over stdio. |
| **What to do** | Use **`python main.py`** with default **`mcp.run()`** (stdio). Put **`command`** + **`args`** in `%APPDATA%\Claude\claude_desktop_config.json` under **`mcpServers`**. Fully quit Claude (including tray), then restart. See [`README.md`](README.md). |

### Connector shows but “Tool permissions” is empty

| Item | Detail |
|------|--------|
| **Symptom** | Settings → Connectors → your server → **Tool permissions** lists nothing. |
| **Root cause** | **`@mcp.prompt()`** entries are **not tools**. Only **`@mcp.tool()`** appears in that list. |
| **What to do** | Use prompts from the chat / prompt UI. Add **`@mcp.tool()`** functions if you need rows under **Tool permissions** (this repo includes **`ping_research_server`** as a smoke test). |

---

## 1. `SSE error: Failed to fetch` / “Connection Error” / generic connection failure

| Item | Detail |
|------|--------|
| **Symptom** | Inspector shows connection error, *SSE error: Failed to fetch*, *TypeError: Failed to fetch*, or *Connection Error - Check if your MCP server is running and proxy token is correct*. |
| **Root cause** | **Wrong transport + URL + flow:** e.g. **Streamable HTTP** pointed at **`http://localhost:8000/mcp`** while only **`fastmcp dev inspector main.py`** is running (stdio — **nothing on 8000**). Or **Direct** mode with a **wrong/stale proxy token**. Or Inspector opened **without** `?MCP_PROXY_AUTH_TOKEN=...` when the proxy expects auth. |
| **What to do** | **Streamable HTTP to 8000:** Use **Flow B** or **Flow C** so **8000** is actually listening. **Flow A (stdio):** open the **exact** URL printed in the terminal (including token). If using **Direct** to **8000**, clear **Proxy Session Token** or fix it; if using **Via Inspector Proxy**, set **Inspector Proxy Address** (e.g. **`http://127.0.0.1:6277`**) and the **full** token from the CLI. |

---

## 2. Nothing listening on port 8000

| Item | Detail |
|------|--------|
| **Symptom** | Connection refused / failed fetch to `http://127.0.0.1:8000/mcp`. |
| **Root cause** | **`fastmcp dev inspector main.py`** runs **`fastmcp run main.py`** → **stdio** by default. **`uv run python main.py`** (no `--http`) also uses **stdio**. |
| **What to do** | **Flow B:** `uv run python main.py --http`. **Flow C:** `uv run fastmcp dev inspector fastmcp.json` (or `uv run fastmcp dev inspector`). Verify with `Get-NetTCPConnection -LocalPort 8000 -State Listen` (PowerShell) or try the URL after the server prints its listen banner. |

---

## 3. Wrong path or transport (`/mcp` vs `/sse`)

| Item | Detail |
|------|--------|
| **Symptom** | 404, wrong behavior, or client/server mismatch. |
| **Root cause** | This project’s HTTP entry uses **Streamable HTTP** with default path **`/mcp`**. **SSE** uses a different path (often **`/sse`**) and **`--transport sse`**. |
| **What to do** | For current **`main.py` / `fastmcp.json`:** **Streamable HTTP** and **`http://127.0.0.1:8000/mcp`**. |

---

## 4. CORS (cross-origin) — Inspector on 6274, server on 8000

| Item | Detail |
|------|--------|
| **Symptom** | *Failed to fetch* in the browser Inspector; `curl` may still work. |
| **Root cause** | Origins **`http://localhost:6274`** and **`http://127.0.0.1:8000`** differ. Without CORS, **`fetch`** from the Inspector page is blocked. |
| **What to do** | Keep **`CORSMiddleware`** on **`--http`** / **`fastmcp.json`** HTTP mode with Inspector origins. See **`main.py`**. |

---

## 5. `Bad Request: Missing session ID` (JSON-RPC 32600)

| Item | Detail |
|------|--------|
| **Symptom** | Connect progresses then fails with *Missing session ID* on Streamable HTTP. |
| **Root cause** | Streamable HTTP uses the **`mcp-session-id`** response header; under CORS the browser must see it via **`Access-Control-Expose-Headers`**. |
| **What to do** | **`expose_headers`** must include **`mcp-session-id`** (and related MCP headers). See **`main.py`** and `mcp.server.streamable_http` constants. |

---

## 6. Wrong `mcp.run` keyword: `middlewares` vs `middleware`

| Item | Detail |
|------|--------|
| **Symptom** | `TypeError: unexpected keyword argument 'middlewares'`. |
| **Root cause** | FastMCP expects **`middleware=`** (singular). |
| **What to do** | Use **`middleware=[Middleware(...)]`**. |

---

## 7. MCP Inspector Proxy / “proxy token” errors

| Item | Detail |
|------|--------|
| **Symptom** | *Error Connecting to MCP Inspector Proxy* or *proxy token is correct*. |
| **Root cause** | **Via Proxy** needs a reachable proxy (**`127.0.0.1:6277`**). Stale or truncated tokens, or **Direct** to **8000** while a bad token is still configured, causes confusing errors. |
| **What to do** | Restart **`fastmcp dev inspector …`**, use the **full** printed URL or token. **Direct** to **8000:** clear proxy fields if unnecessary. **Via Proxy:** set **Inspector Proxy Address** to **`http://127.0.0.1:6277`** and paste the **full** token. |

---

## 8. `ImportError: cannot import name 'Message' from 'mcp.types'`

| Item | Detail |
|------|--------|
| **Symptom** | `fastmcp dev inspector …` traceback when importing **`main.py`**. |
| **Root cause** | The MCP SDK exposes **`PromptMessage`**, not **`Message`**, for prompt result messages. |
| **What to do** | Use **`from mcp.types import PromptMessage, TextContent`** and **`PromptMessage(...)`** in prompt return values. |

---

## 9. `MCP Inspector PORT IS IN USE` (6274)

| Item | Detail |
|------|--------|
| **Symptom** | CLI prints port **6274** already in use. |
| **Root cause** | A previous Inspector or another process is still bound to **6274**. |
| **What to do** | Close old Inspector tabs/processes, then identify and stop the listener, e.g. in PowerShell: **`Get-NetTCPConnection -LocalPort 6274 -State Listen`**, then **`Stop-Process -Id <OwningProcess> -Force`**. Also check **6277** if the proxy conflicts. |

---

## 10. Duplicate / legacy entry files (`main.py` vs `main-working.py`)

| Item | Detail |
|------|--------|
| **Symptom** | One file “works” in the browser, the other does not. |
| **Root cause** | **Only what you run** matters. HTTP Flow B needs **CORS + expose_headers**; stdio-only or HTTP without those breaks the browser. |
| **What to do** | Treat **`main.py`** + **`fastmcp.json`** as canonical; avoid long-lived divergent copies. |

---

## Quick reference checklists

### Streamable HTTP in browser → `8000/mcp`

1. **Flow C:** `uv run fastmcp dev inspector fastmcp.json` (or `uv run fastmcp dev inspector`), **or**
2. **Flow B:** `uv run python main.py --http` in a dedicated terminal (leave it running).
3. Inspector: **Transport** = Streamable HTTP, **URL** = `http://127.0.0.1:8000/mcp`, **Connection** = **Direct** (clear proxy token if it causes auth noise).

### Dev inspector with stdio only (`fastmcp run main.py`)

1. `uv run fastmcp dev inspector main.py`
2. Open the **printed** URL including **`MCP_PROXY_AUTH_TOKEN`** when required.
3. Do **not** rely on **8000/mcp** unless you also start Flow B or C.

### Claude Desktop

1. Config: `%APPDATA%\Claude\claude_desktop_config.json` → **`mcpServers`** → **`python.exe` + `main.py`**.
2. **`main.py`** must use **stdio** for that entry (default `mcp.run()`, not HTTP-only).
3. **Tool permissions** only lists **`@mcp.tool()`**; prompts are separate in the UI.

---

## References

- MCP Inspector — [modelcontextprotocol/inspector README](https://github.com/modelcontextprotocol/inspector/blob/main/README.md).
- FastMCP + Claude Desktop — [FastMCP docs](https://gofastmcp.com/integrations/claude-desktop).
- CORS — [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).
