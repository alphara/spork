# Spork

```
███████╗██████╗  ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
███████╗██████╔╝██║   ██║██████╔╝█████╔╝ 
╚════██║██╔═══╝ ██║   ██║██╔══██╗██╔═██╗ 
███████║██║     ╚██████╔╝██║  ██║██║  ██╗
╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

Meet Spork, the world’s first utensil-inspired meta-agent. Forged in the digital kitchens of SpoonOS, Spork is a hybrid wonder: part spoon, part fork, and 100% dedicated to creating agents that are smarter, faster, and occasionally confused about why a piece of cutlery is in charge.

![Sporkitect](./sporkitect.png)

## 🥄 Sporkitecht — The Agent-Architect for SpoonOS

**Spork** is a project that implements **Sporkitecht**, an autonomous agent-architect designed for **SpoonOS**, an agentic AI operating system.

Its purpose is simple but ambitious:

> **Sporkitecht creates other agents. Automatically. Reliably. From a short prompt.**

This project explores how AI can generate functional agent code by understanding the full agent-architecture defined in SpoonOS and applying it to user-defined specifications.

---

## Spork Video Intro

[![Spork for SpoonOS by Artem Arakcheev](https://img.youtube.com/vi/j8XBc6Y5auk/0.jpg)](https://youtu.be/j8XBc6Y5auk)

---

## 🌍 Why This Project Exists

Modern AI platforms rely on agents that interact with tools, data, APIs, and networks.
But **designing and coding these agents is still a manual, error-prone process.**

Developers must:

* Understand a specific agent framework
* Scan fragmented documentation
* Wire up tools and I/O
* Follow strict architectural patterns
* Ensure outputs follow exact format requirements

This becomes even harder when the ecosystem (like SpoonOS) grows—multiple agent types, dozens of tools, special prompts, graph workflows, memory modules, etc.

**Sporkitecht solves this by turning agent creation into a natural-language request.**
You describe the agent.
Sporkitecht writes the code.

---

## 🚀 What Problems It Solves

### 1. **Agent Development Is Slow**

Normally, building a correct agent requires reading multiple documents, examples, and conventions.

Sporkitecht **automates this entirely**, generating ready-to-run code in seconds.

---

### 2. **Architecture Consistency**

Human-written agents often drift from official architecture guidelines.

Sporkitecht uses **the actual SpoonOS Agent Creation Guide**, loaded dynamically from local files, ensuring:

* Correct structure
* Correct use of ToolCallAgent
* Correct tool definitions
* Proper system prompts
* Uniform coding style

It becomes a *living compiler* for the SpoonOS agent ecosystem.

---

### 3. **Integrating Tools Is Hard**

Agents usually need access to custom tools.

This project demonstrates:

* How to define a custom tool (`GreetingTool`)
* How to inject it into an agent via `ToolManager`
* How to make it available for LLM tool-calling

Sporkitecht can then use the tool automatically when generating agent code.

---

### 4. **Developers Often Forget Critical Context**

Sporkitecht loads:

```
spoon-core/doc/agent.md
spoon-core/doc/builtin_tools.md
spoon-core/doc/graph_agent.md
spoon-core/examples/...
```

It merges them into a unified **Agent Creation Guide** the LLM always sees.
This ensures the agent:

* Has full documentation during generation
* Generates code consistent with the entire ecosystem
* Learns from real examples, not theory

---

### 5. **Cross-Provider LLM Flexibility Is Usually Painful**

Because it wraps everything inside a simple configuration (`ChatBot`), the system can switch:

* OpenAI (default)
* Anthropic
* Gemini
* DeepSeek
* OpenRouter

…all with the same agent code.

---

## 🧠 How It Works

### **1. Loads the entire SpoonOS agent manual**

It reads documentation and example scripts from `spoon-core/`, joins them into a single text, and injects it into the system prompt.

### **2. Defines a meta-agent: Sporkitecht**

Sporkitecht is not an operational agent itself—
it is an **agent-creator**.

Its system prompt clearly states:

* “Your name is Spork.”
* “You develop agents.”
* “You output only Python code.”
* “Follow the Agent Creation Guide.”

This makes it deterministic and architecture-aligned.

### **3. Accepts a natural-language prompt**

Example:

```
Generate me a web3 agent that helps with finance customer support
```

No conventions, no boilerplate — just description.

### **4. Generates full Python agent code**

The output is:

* Syntactically correct
* Conforms to SpoonOS architecture
* Ready to run or embed
* Automatically uses tools when appropriate

### **5. Runs entirely from command-line**

Using `--prompt "..."`, developers can create agents from scripts, automation pipelines, CI/CD, or other agent builders.

---

## 🔮 Vision

Sporkitecht aims to become **the compiler, architect, and mentor** of a fully agentic AI operating system.

Instead of manually designing dozens of agents, developers will describe behavior at a high level—and Sporkitecht will consistently generate correct implementations.

This project demonstrates:

* How agent-architect agents work
* How SpoonOS agent generation is automated
* How to create meta-agents that shape other agents
* How to integrate documentation-aware LLM workflows

---

## Prerequisites

* Python 3.12+
* pip package manager (or uv as a faster alternative)
* [SpoonOS Core](https://github.com/XSpoonAi/spoon-core)

```bash
git submodule update --init
cd spoon-core/

# Create a virtual environment
python -m venv spoon-env
source spoon-env/bin/activate  # For macOS/Linux

# Install dependencies
pip install -r requirements.txt
cd ../
```

## Install

```bash
# Make sure you are in a spork directory, e.g., with `pwd`
pip install -r requirements.txt

cp env.example .env
# Set your keys in the .env:
# * OPENAI_API_KEY

# verify configuration
python -c "from spoon_ai.utils.config_manager import ConfigManager; print('✅ Configuration loaded successfully')"
```

## Run

```bash
source spoon-core/spoon-env/bin/activate

python spork.py --prompt "Hello world agent"
```

## Examples

### Hello World Agent for SpoonOS

```bash
python spork.py --prompt "Hello world agent"
```
Response:
```python
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
```

```bash
python examples/hello-world.py

Hello, World!
```

### Web3 Support Agent for SpoonOS

```bash
python spork.py --prompt "Generate me a web3 agent that helps with finance customer support"
```
Response:
```python
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
```

## Web App

You can run web app with the chat window.

```bash
python soup.py
# Web server running on http://localhost:8183
```

## Team

The project was initiated to participate in a Neo x DeFrens event (SpoonOS Hackathon + Demo Day).

We are the team Snoop-Soup consisting of the following members:

* Ekaterina Melnikova
* Artem Arakcheev
* Pavel Gembarzhevsky

We look for a front-end contributor.

Thanks!
