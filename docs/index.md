# Nexithium Agent Platform Documentation

Welcome to the official documentation for **Nexithium Agent Platform**, your go‑to framework for building, deploying, and extending AI agents.

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
3. [Architecture](#architecture)
   - [Core Components](#core-components)
   - [Tools](#tools)
   - [Interfaces](#interfaces)
4. [Using the CLI](#using-the-cli)
5. [Telegram Bot Interface](#telegram-bot-interface)
6. [REST API](#rest-api)
7. [Writing New Agents](#writing-new-agents)
8. [Registering Custom Tools](#registering-custom-tools)
9. [Memory Management](#memory-management)
10. [Contributing](#contributing)
11. [License](#license)
12. [Whitepaper](whitepaper.md)


---

## Overview

Nexithium Agent Platform is a modular Python framework that lets you:
- Create LLM‑driven agents with custom system prompts
- Integrate external APIs (CoinGecko, Google Search, Tavily, etc.) as "tools"
- Manage conversation memory (short‑term or persistent)
- Expose agents via CLI, Telegram, or REST API (FastAPI)

Use it for crypto analysis, customer support, research assistants, and more.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- API keys for OpenAI and any desired tools (CoinGecko doesn’t require a key)

### Installation

```bash
git clone https://github.com/nexithium/nexithium-agent-platform.git
cd nexithium-agent-platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy the example and fill in your environment variables:
```bash
cp config.env.example .env
```
Edit `.env`:
```dotenv
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=12345:abcde
NEXITHIUM_API_KEY=your-secret-key
SERPER_API_KEY=your-serper-api-key
# REDIS_URL=redis://:pass@host:6379/0
```

---

## Architecture

### Core Components

- **Agent** (`core/agent.py`): runs the LLM, manages messages, and calls tools
- **Memory** (`core/memory.py`): short‑term buffer and persistent JSON/Redis storage
- **Tools** (`core/tools.py`): registry for API wrappers and custom functions

### Tools

Located in `tools/`, each tool is a simple function registered via `@register_tool`:
- `coingecko.get_price` — fetches USD price
- `token_trend` — analyzes 2‑day trend
- `token_description` — retrieves project description
- `token_market_data` — market cap & volume
- `google_search` — web search via Serper.dev
- `tavily_news` — news summary fallback

### Interfaces

- **CLI** (`interfaces/cli.py`) — interactive terminal interface
- **Telegram** (`interfaces/telegram_bot.py`) — bot with inline menu & commands
- **REST API** (`interfaces/fastapi_server.py`) — `/chat` and `/tools` endpoints

---

## Using the CLI

```bash
python interfaces/cli.py --memory short --model gpt-4
```

**Commands:**
- `help` — show commands
- `tools` — list available tools
- `use <tool> [args]` — invoke a specific tool
- free text — chat with the AI agent
- `exit`/`quit` — stop

---

## Telegram Bot Interface

Start the bot:
```bash
python interfaces/telegram_bot.py
```

**Commands:**
- `/start` — show menu
- `/help` — usage guide
- `/tools` — list tools
- `price <symbol>`, `trend <symbol>`, `analyze <symbol>`, `forecast <symbol>`
- free chat — general questions

---

## REST API

Run server:
```bash
uvicorn interfaces.fastapi_server:app --reload --port 8000
```

**Endpoints:**
- `GET /` — health check
- `GET /tools` — list tools (requires `X-API-Key`)
- `POST /chat` — agent interaction (requires `X-API-Key`)

Use Swagger UI at `/docs`.

---

## Writing New Agents

Create an agent in `agents/`:
```python
from core.agent import Agent
from core.tools import load_all_tools
from core.memory import ShortTermMemory

my_agent = Agent(
    name="MyCustomAgent",
    system_prompt="You are...",
    tools=list(load_all_tools().values()),
    memory=ShortTermMemory().get()
)
```

---

## Registering Custom Tools

In `tools/`, create a new file with a function:
```python
# tools/my_tool.py
def my_tool(arg1: str, arg2: int) -> str:
    return f"Received {arg1} and {arg2}"
```

Then register in `core/tools.py`:
```python
from tools.my_tool import my_tool
register_tool("my_tool")(my_tool)
```

---

## Memory Management

- **ShortTermMemory**: retains last N exchanges in memory buffer
- **PersistentMemory**: saves full conversation per user in `memory_logs/`
- Access via `MemoryManager.get_memory(user_id)`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on coding standards, testing, and pull requests.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---


## Whitepaper

Read the full project whitepaper [here](whitepaper.md).

---
*Documentation generated by Nexithium Agent Platform.*

