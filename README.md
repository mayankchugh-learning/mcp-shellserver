# shellserver — Mini Pokédex Lite (MCP resources demo)



## **Git: new orphan branch (clean history)**

Use this when you want a **fresh branch with no parent commits**, but you keep your **current working tree**—then make that tree the **first commit** on the new line.

Replace the branch name and commit message as needed.

```
git switch --orphan project/resources
```

##### `create or add .gitignore`

##### `create or add requirements.txt`

```
git add -A
git commit -m "Initial commit for MCP resources"'
git push origin project/resources 
```

```
uv init
uv venv
uv add -r requirements.txt
```



A small [FastMCP](https://github.com/jlowin/fastmcp) server that demonstrates **MCP resources**: static URIs, templates with parameters, and live data from [PokeAPI](https://pokeapi.co/).

## Requirements

- Python **3.13+** (see `pyproject.toml`)

## Setup

From the repo root:

```bash
uv sync
```

Or create a venv and install dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```

## Run

```bash
python main.py
```

By default, `main.py` starts the server with **HTTP** transport. FastMCP listens on `**http://127.0.0.1:8000`**; the streamable HTTP MCP endpoint is typically `**http://127.0.0.1:8000/mcp**` (override with `FASTMCP_HOST`, `FASTMCP_PORT`, or `FASTMCP_STREAMABLE_HTTP_PATH` if you configure them).

To use **stdio** instead (common for local MCP clients that spawn a subprocess), use `app.run()` without `transport="http"` at the bottom of `main.py`.

## Resources


| URI                           | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| `poke://starters`             | Lists demo starter Pokémon with links to `poke://pokemon/{id}`              |
| `poke://pokemon/{id_or_name}` | Pokémon details (ID or name, e.g. `1`, `pikachu`, `charizard`)              |
| `poke://types/{type_name}`    | Sample Pokémon for a type (e.g. `fire`, `water`, `grass`); first 10 entries |


Responses are JSON (height/weight normalized where applicable). Missing Pokémon or types return a `ResourceError` with a clear message.

## Connecting an MCP client

Point your client at the HTTP URL above (same pattern as `claude mcp add --transport http <name> <url>`), or configure a **stdio** command that runs `python main.py` after switching to stdio transport in code.