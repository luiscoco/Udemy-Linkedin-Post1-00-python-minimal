import asyncio
import os
from claude_agent_sdk import query, ResultMessage

os.environ["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"  # Hide the "claude.ai connectors are disabled" warning

async def main():
    async for message in query(prompt="Hello world!"):
        if isinstance(message, ResultMessage):
            print(message.result)

asyncio.run(main())
