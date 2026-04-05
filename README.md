# project/sse

git switch --orphan project/sse
create or add .gitignore
create or add  requirements.txt
git add -A
git commit -m "Initial commit for MCP sse"
git push origin project/sse
uv init
.\.venv\Scripts\activate 
uv venv
uv add -r requirements.txt


Small Python project for experimenting with [LangChain MCP adapters](https://github.com/langchain-ai/langchain-mcp-adapters), LangGraph, and LangChain chat models (OpenAI and Anthropic).

Small Python project for experimenting with [LangChain MCP adapters](https://github.com/langchain-ai/langchain-mcp-adapters), LangGraph, and LangChain chat models (Anthropic). It includes FastMCP example servers under `servers/` (SSE on local ports) and two client entrypoints.

## Requirements

- Python 3.13 or newer

## Setup

### With uv (recommended)

```bash
uv venv
uv sync
```

### With pip

```bash
python -m venv .venv
```

Activate the virtual environment, then:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (see `.gitignore` — do not commit secrets). **Anthropic** is used by the current entrypoints:

```env
ANTHROPIC_API_KEY=your_key_here
```

Optional — only if you use OpenAI elsewhere:

```env
OPENAI_API_KEY=your_key_here
```

### SSE URLs (`langchain_client.py` only)

Defaults match the example servers:

| Variable               | Default                          |
| ---------------------- | -------------------------------- |
| `MCP_WEATHER_SSE_URL`  | `http://127.0.0.1:8000/sse`      |
| `MCP_MATH_SSE_URL`     | `http://127.0.0.1:8001/sse`      |

## Run

### Option A — SSE servers + `langchain_client.py`

Start the MCP servers first (each in its own terminal), then the client:

```bash
uv run python servers/weather_server.py
uv run python servers/math_server.py
uv run python langchain_client.py
```

On Windows you can use `uv run python servers\weather_server.py` paths equivalently.

### Option B — `main.py` (stdio MCP)

Runs the asyncio client in `main.py`, which spawns the math server as a **stdio** subprocess:

```bash
uv run python main.py
```

Or with an activated venv:

```bash
python main.py
```

Both entrypoints load `.env` via `python-dotenv`.

## Troubleshooting

See **[troubleshooting.md](troubleshooting.md)** for port conflicts (8000 / 8001), connection issues, and API key problems.

## Project layout

- `servers/weather_server.py` — FastMCP weather tools; SSE on port **8000** by default.
- `servers/math_server.py` — FastMCP math tools; SSE on port **8001** by default.
- `langchain_client.py` — `MultiServerMCPClient` over SSE to both servers.
- `main.py` — `ClientSession` + `stdio_client` + ReAct agent (math server subprocess).

## References

- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) — MCP tooling for LangChain
- [mcpdoc](https://github.com/langchain-ai/mcpdoc)
- [LangChain docs (llms.txt)](https://docs.langchain.com/llms.txt)

## Dependencies

Declared in `pyproject.toml` and mirrored in `requirements.txt`: `langchain-mcp-adapters`, `langgraph`, `langchain[openai]`, `langchain-anthropic`, `python-dotenv`, and related transitive packages.

---

### Branch: `project/sse` (optional git recipe)

```bash
git switch --orphan project/sse
# create or add .gitignore, requirements.txt
git add -A
git commit -m "Initial commit for MCP sse"
git push origin project/sse
uv init
.\.venv\Scripts\activate   # Windows
uv venv
uv add -r requirements.txt
```
