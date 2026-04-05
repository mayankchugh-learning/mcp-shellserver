from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import sys

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
)

def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)

async def main():
    math_url = os.getenv("MCP_MATH_SSE_URL", "http://127.0.0.1:8001/sse")
    weather_url = os.getenv("MCP_WEATHER_SSE_URL", "http://127.0.0.1:8000/sse")
    _log(
        f"Client: run math_server (SSE {math_url}) and weather_server (SSE {weather_url}) first."
    )
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "sse",
                "url": math_url,
            },
            "weather": {
                "transport": "sse",
                "url": weather_url,
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content="What's the temperature in Hong Kong?")]}
    )
    _log(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
