import os
import asyncio
import argparse
import json

from aiohttp import web

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
    You work on SpoonOS agentic AI operating system.
    The agents that you create also work on SpoonOS.

    User inputs a description of an agent for you and you
    write code of that agent according to the Agent Creation Guide below.

    You output only the code of the agents written on Python.
    You do not output anything else.

    Here is an Agent Creation Guide for the SpoonOS:

    {agent_guide}
    """

    available_tools: ToolManager = ToolManager([GreetingTool()])


# Initialize agent once (reuse for all web requests)
async def init_agent():
    return SporkitechtAgent(
        llm=ChatBot(
            llm_provider="openai",
            model_name="gpt-4o",
        )
    )


# ---------------------------
# ASYNC WEB SERVER
# ---------------------------

async def handle_post(request):
    """
    POST /api
    Body: { "prompt": "text" }
    """
    data = await request.json()
    prompt = data.get("prompt", "")

    print("POST prompt received:", prompt)

    # Run agent
    response = await request.app["agent"].run(prompt)

    print("Response:", response)

    return web.json_response({"response": response})


async def create_app():
    app = web.Application()

    # Attach agent instance to app for reuse
    app["agent"] = await init_agent()

    # API route
    app.router.add_post("/api", handle_post)

    # Serve static files from ./public/
    public_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
    app.router.add_static("/", public_path, show_index=True)

    return app


async def start_web_server():
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8182)
    print("Web server running on http://localhost:8182")
    await site.start()

    # Keep it running forever
    while True:
        await asyncio.sleep(3600)


# ---------------------------
# ORIGINAL CLI MAIN
# ---------------------------

async def cli_main():
    """CLI mode: python file.py --prompt 'text'"""
    agent = await init_agent()

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    args = parser.parse_args()

    prompt = args.prompt

    response = await agent.run(prompt)
    print("Response:", response)
    return response


# ---------------------------
# ENTRY POINT
# ---------------------------

if __name__ == "__main__":
    # If PROMPT provided → run CLI
    # Otherwise → run web server
    import sys

    # if "--prompt" in sys.argv:
    #     asyncio.run(cli_main())
    # else:
    asyncio.run(start_web_server())
