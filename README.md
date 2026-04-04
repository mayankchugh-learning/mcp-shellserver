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