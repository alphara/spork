from spoon_ai.agents.spoon_react_mcp import SpoonReactMCP
from spoon_ai.tools.tool_manager import ToolManager


class HelloWorldAgent(SpoonReactMCP):
    name: str = "HelloWorldAgent"
    system_prompt: str = (
        '''You are a simple agent that greets the world. Your task is to
        print "Hello, World!" and indicate when the task is complete.'''
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avaliable_tools = ToolManager([])

    async def run(self, query: str) -> str:
        print("Hello, World!")
        return "Task complete: Hello, World! printed."


async def main():
    agent = HelloWorldAgent()
    response = await agent.run("")
    print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
