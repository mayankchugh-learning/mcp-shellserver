https://github.com/langchain-ai/mcpdoc


https://docs.langchain.com/llms.txt

https://github.com/langchain-ai/langchain-mcp-adapters


pip install langchain-mcp-adapters langgraph "langchain[openai]"

export OPENAI_API_KEY=<your_api_key>

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-20250514")  # pick a model you use