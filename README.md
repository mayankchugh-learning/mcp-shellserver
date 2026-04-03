## Git: new orphan branch (clean history)

Use this when you want a **fresh branch with no parent commits**, but you keep your **current working tree**—then make that tree the **first commit** on the new line.

Replace the branch name and commit message as needed.

```bash
git switch --orphan project/resources
```
### `create or add .gitignore`
### `create or add  requirements.txt`
```bash
git add -A
git commit -m "Initial commit for MCP resources"'
git push origin project/resources 
```
```bash
uv init
uv venv
uv add -r requirements.txt

uv sync
```
