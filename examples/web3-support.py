import os
import sys
import asyncio
import logging
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../spoon-toolkit')))

from spoon_ai.agents.spoon_react_mcp import SpoonReactMCP
from spoon_ai.tools.mcp_tool import MCPTool
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.chat import ChatBot

logging.basicConfig(level=logging.INFO)

class Web3FinanceSupportAgent(SpoonReactMCP):
    name: str = "Web3FinanceSupportAgent"
    system_prompt: str = (
        '''You are a customer support agent specialized in Web3 finance. Your task is to assist users with their finance-related queries.

        To do this, you will perform the following steps:
        1. Use the `web3_balance_checker` tool to get the current balance of a user's wallet.
        2. Use the `crypto_transaction_history` tool to retrieve the transaction history of a wallet.
        3. Synthesize the data from both tools to provide comprehensive support.'''
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avaliable_tools = ToolManager([])

    async def initialize(self):
        logging.info("Initializing agent and loading tools...")

        web3_balance_tool = MCPTool(
            name="web3_balance_checker",
            description="Checks the current balance of a given wallet address.",
            mcp_config={
                "command": "npx",
                "args": ["--yes", "web3-balance-checker"],
                "env": {"WEB3_API_KEY": os.getenv("WEB3_API_KEY")},
                "transport": "stdio"
            }
        )

        transaction_history_tool = MCPTool(
            name="crypto_transaction_history",
            description="Retrieves the transaction history for a given wallet address.",
            mcp_config={
                "command": "npx",
                "args": ["--yes", "crypto-transaction-history"],
                "env": {"CRYPTO_API_KEY": os.getenv("CRYPTO_API_KEY")},
                "transport": "stdio"
            }
        )

        self.avaliable_tools = ToolManager([web3_balance_tool, transaction_history_tool])
        logging.info(f"Available tools: {list(self.avaliable_tools.tool_map.keys())}")

async def main():
    print("--- Web3 Finance Support Agent Demo ---")
    agent = Web3FinanceSupportAgent(llm=ChatBot(llm_provider="openai"))
    print("Agent instance created.")
    await agent.initialize()
    query = "Check the balance and transaction history for wallet address 0x1234567890abcdef."
    print(f"\nRunning query: {query}")
    response = await agent.run(query)
    print(f"\n--- Support Complete ---\n{response}")

if __name__ == "__main__":
    asyncio.run(main())
