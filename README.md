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

Create a `.env` file in the project root (see `.gitignore` — do not commit secrets). At minimum, set the provider you use:

```env
OPENAI_API_KEY=your_key_here
```

For Anthropic models, add:

```env
ANTHROPIC_API_KEY=your_key_here
```

## Run

```bash
uv run python main.py
```

Or, with an activated venv:

```bash
python main.py
```

The entrypoint loads `.env` via `python-dotenv` and runs the asyncio `main()` in `main.py`.

## References

- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) — MCP tooling for LangChain
- [mcpdoc](https://github.com/langchain-ai/mcpdoc)
- [LangChain docs (llms.txt)](https://docs.langchain.com/llms.txt)

## Dependencies

Declared in `pyproject.toml` and mirrored in `requirements.txt`: `langchain-mcp-adapters`, `langgraph`, `langchain[openai]`, `langchain-anthropic`, `python-dotenv`, and related transitive packages.