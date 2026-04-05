# Troubleshooting

## Port 8000 already in use (Windows WinError 10048)

When starting an MCP server with SSE transport (for example `uv run .\servers\weather_server.py`), Uvicorn may try to bind to `127.0.0.1:8000`. If another process is already listening on that address and port, Windows returns:

`[Errno 10048] ... only one usage of each socket address (protocol/network address/port) is normally permitted`

That means a **port conflict**, not a bug in your server script.

### 1. Find which PID is listening on port 8000

Open **PowerShell** and run:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

- **`OwningProcess`** is the process ID (PID) holding the port.
- `-State Listen` limits results to active listeners (ignore `TIME_WAIT` unless you are debugging connections).
- If this prints nothing, nothing is **listening** on 8000 at that moment (the port may be free).

### 2. Map the PID to a program

Replace `<pid>` with the number from `OwningProcess`:

```powershell
Get-Process -Id <pid> | Select-Object Id, ProcessName, Path
```

**One-liner** (name and path for every listener on 8000):

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

Alternatively, configure your MCP server to use a **different port** if your stack supports it.

### Example run (this repo, one session)

Commands executed while documenting:

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

Your PID and path will differ; the pattern is usually another **python** process still running a server on 8000.
