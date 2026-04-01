import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")


async def main():
    print("Hello from shellserver!")


if __name__ == "__main__":
    asyncio.run(main())
