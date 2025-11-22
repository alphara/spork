import os
import asyncio
import argparse

from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from dotenv import load_dotenv

load_dotenv(override=True)


def load_texts_from_files(files):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    texts = {}

    for rel_path in files:
        full_path = os.path.join(BASE_DIR, rel_path)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                texts[rel_path] = f.read()
        except Exception as e:
            texts[rel_path] = f"ERROR: {e}"

    return texts


def join_all_texts(texts, separator="\n\n"):
    return separator.join(texts.values())


# The following documents are from the spoon-core repo
# The docs are licensed under `Apache-2.0`:
files = [
    "spoon-core/doc/agent.md",
    "spoon-core/doc/builtin_tools.md",
    "spoon-core/doc/graph_agent.md",

    "spoon-core/examples/agent/graph_agent_demo.py",
    "spoon-core/examples/agent/my_agent_demo.py",

    # "spoon-core/examples/chatbot_streaming_demo.py",
    # "spoon-core/examples/graph_crypto_analysis.py",
    # "spoon-core/examples/intent_graph_demo.py",
    # "spoon-core/examples/llm_architecture_example.py",
    # "spoon-core/examples/llm_infrastructure_example.py",
    # "spoon-core/examples/llm_integrated_graph_demo.py",
    # "spoon-core/examples/llm_manager_example.py",
    # "spoon-core/examples/neo_toolkit_agent_demo.py",
    # "spoon-core/examples/neofs-agent-demo.py",
    # "spoon-core/examples/short_term_memory_usage.py",
    # "spoon-core/examples/solana_toolkit_demo.py",
    # "spoon-core/examples/turnkey-agent-demo.py",
    # "spoon-core/examples/x402_agent_demo.py",

    # "spoon-core/examples/mcp/deepwiki_demo.py",
    # "spoon-core/examples/mcp/mcp_thirdweb_collection.py",
    # "spoon-core/examples/mcp/spoon_search_agent.py",
    # "spoon-core/examples/mcp/SpoonThirdWebagent.py",

    # "spoon-core/examples/turnkey/build_unsigned_eip1559_tx.py",
    # "spoon-core/examples/turnkey/multi_account_use_case.py",
    # "spoon-core/examples/turnkey/turnkey_trading_use_case.py",

    # "spoon-core/examples/README.md",
]

texts = load_texts_from_files(files)
agent_guide = join_all_texts(texts)

print('agent_guide:', agent_guide)


# Define a custom tool
class GreetingTool(BaseTool):
    name: str = "greeting"
    description: str = "Generate personalized greetings"
    parameters: dict = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Person's name"}
        },
        "required": ["name"]
    }

    async def execute(self, name: str) -> str:
        return f"Hello {name}! Welcome to SpoonOS! 🚀"


# Create your agent
class SporkitechtAgent(ToolCallAgent):
    name: str = "SporkitechtAgent"
    description: str = "Spork agent architects agents for SpoonOS"

    system_prompt: str = f"""
    Your name is Spork. You are an agent that develops agents.
    You works on SpoonOS agentic AI operating system.
    The agents that you create also work on SpoonOS.

    User inputs a description of an agent for you and you
    write code of that agent according to the Agent Creation Guide below.

    You output only the code of the agents written on Python.
    You do not output anything else.

    Here is an Agent Creation Guide for the SpoonOS:

    {agent_guide}
    """

    available_tools: ToolManager = ToolManager([GreetingTool()])


async def main():
    # Initialize agent with LLM
    agent = SporkitechtAgent(
        llm=ChatBot(
            llm_provider="openai",         # or "anthropic", "gemini", "deepseek", "openrouter"
            # model_name="gpt-5.1",        # TODO: Framework default for OpenAI
            # model_name="gpt-5",
            model_name="gpt-4o",

            # llm_provider="gemini",         # or "anthropic", "gemini", "deepseek", "openrouter"
            # model_name="gemini-2.5-flash",
        )
    )
    # print('agent:', agent)

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True, help="Input prompt text")
    args = parser.parse_args()
    print("Prompt:", args.prompt)

    prompt = args.prompt or "Generate me a web3 agent that helps with finance customer support"

    # Run the agent - framework handles all error cases automatically
    response = await agent.run(prompt)

    print('Response:', response)
    return response

if __name__ == "__main__":
    result = asyncio.run(main())
