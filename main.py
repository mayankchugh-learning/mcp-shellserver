import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))

stdio_server = StdioServerParameters(
   command="python",
    args ={"C:\\\githunb\mcp-servers\\shellserver\\servers\\math_server.py"}
)


async def main():
    print("Hello from shellserver!")


if __name__ == "__main__":
    asyncio.run(main())
