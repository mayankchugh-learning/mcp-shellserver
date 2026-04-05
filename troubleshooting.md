# Troubleshooting

Common issues when running the MCP FastMCP servers under `servers/` and the LangChain entrypoints in this repo.

## Port already in use (Windows `WinError 10048`)

When a server uses **SSE** transport, Uvicorn binds to a TCP port on `127.0.0.1`. If something else is already listening on that address and port, Windows returns:

`[Errno 10048] ... only one usage of each socket address (protocol/network address/port) is normally permitted`

That is a **port conflict**, not a bug in the server script.

### Default ports in this repo

| Server            | Script                     | Default port |
| ----------------- | -------------------------- | ------------ |
| Weather (SSE)     | `servers/weather_server.py` | **8000**     |
| Math (SSE)        | `servers/math_server.py`   | **8001**     |

### 1. Find which PID is listening

Replace `8000` with `8001` (or any port) as needed. Open **PowerShell**:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

- **`OwningProcess`** is the process ID (PID) holding the port.
- `-State Listen` limits results to active listeners.
- If nothing prints, nothing is **listening** on that port at that moment.

### 2. Map the PID to a program

Replace `<pid>` with the number from `OwningProcess`:

```powershell
Get-Process -Id <pid> | Select-Object Id, ProcessName, Path
```

**One-liner** (name and path for every listener on a port):

Use **single quotes** around the `-Command` argument when calling `powershell -Command '...'` from `cmd.exe` or some terminals, so `$_` is not stripped before PowerShell sees it:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
  ForEach-Object { Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue } |
  Select-Object Id, ProcessName, Path -Unique
```

### 3. Or use Task Manager

1. Open Task Manager (Ctrl+Shift+Esc).
2. Open the **Details** tab.
3. Right-click the column header → **Select columns** → enable **PID (Process identifier)**.
4. Find the row whose PID matches `OwningProcess`.

### 4. Free the port

- If it is a leftover **Python / Uvicorn / FastAPI** run, stop it in its terminal or end that task in Task Manager.
- To stop from PowerShell (only if you intend to kill that process):

```powershell
Stop-Process -Id <pid> -Force
```

Alternatively, change the **port** in the FastMCP server (see `port=` in `servers/math_server.py`) and point clients at the new URL (see environment variables below).

### Example (port 8000)

Commands used while documenting:

```text
PS> Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
      Select-Object LocalAddress, LocalPort, OwningProcess

LocalAddress LocalPort OwningProcess
------------ --------- -------------
127.0.0.1         8000         35640
```

```text
PS> Get-Process -Id 35640 | Select-Object Id, ProcessName, Path

  Id ProcessName Path
  -- ----------- ----
35640 python      …\uv\python\cpython-3.13.11-windows-x86_64-none\python.exe
```

Your PID and path will differ; the pattern is often another **python** process still running a server on that port.

---

## `langchain_client.py`: connection refused or timeout

`langchain_client.py` connects to **already running** SSE endpoints. Start the servers **before** the client:

1. Terminal A: `uv run python servers/weather_server.py` (listens on `http://127.0.0.1:8000/sse` by default).
2. Terminal B: `uv run python servers/math_server.py` (listens on `http://127.0.0.1:8001/sse` by default).
3. Terminal C: `uv run python langchain_client.py`.

Override URLs if you change ports or hosts:

```env
MCP_WEATHER_SSE_URL=http://127.0.0.1:8000/sse
MCP_MATH_SSE_URL=http://127.0.0.1:8001/sse
```

---

## Missing or invalid `ANTHROPIC_API_KEY`

Both `main.py` and `langchain_client.py` use **Anthropic** (`ChatAnthropic`). Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_key_here
```

If the key is missing or wrong, you will see authentication errors from the Anthropic API when the agent runs.

---

## MCP over stdio (`main.py`)

`main.py` spawns `servers/math_server.py` as a **stdio** MCP subprocess. The subprocess must speak the MCP protocol over stdin/stdout. If you change `math_server.py` to only run **SSE** in `__main__`, that subprocess will not match what `stdio_client` expects—use `langchain_client.py` with the SSE servers running instead, or run the math server with stdio transport when invoked for `main.py`.

---

## Further help

- [README.md](README.md) — setup, env vars, and how to run each script.
