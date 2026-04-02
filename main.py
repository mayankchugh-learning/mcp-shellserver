import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_REPO_ROOT = Path(__file__).resolve().parent
_MATH_SERVER = _REPO_ROOT / "servers" / "math_server.py"

llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
)

stdio_server = StdioServerParameters(
    command="python",
    args=[str(_MATH_SERVER)],
)

async def main():
    async with stdio_client(stdio_server) as (read,write) :
        async with ClientSession(read_stream=read,write_stream=write) as session :
            await session.initialize()  
            print("session initialized")
            tools = await load_mcp_tools(session)
            print(tools)
            print("tools loaded")
            agent = create_react_agent(llm, tools)
            print("agent created")
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
