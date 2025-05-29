# Nexithium Agent Platform

[![Build Status](https://img.shields.io/github/actions/workflow/status/nexithium/nexithium-agent-platform/ci.yml?branch=main)](https://github.com/nexithium/nexithium-agent-platform/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Package](https://img.shields.io/pypi/v/nexithium-agent-platform)](https://pypi.org/project/nexithium-agent-platform)

> A modular, extensible framework to build, run, and deploy LLM-based AI agents across Telegram, CLI, and REST APIs.

---

## 🚀 Features

- **AI Agents** with configurable system prompts and OpenAI/GPT-4 (or GPT-3.5)
- **Tool Integrations**: CoinGecko, Google Search, Tavily, and custom tools
- **Memory Modules**: Short-term (session) and persistent (Redis or file) memory
- **Multi-Interface Support**: Telegram bot, CLI, FastAPI REST API
- **Example Agents**: Crypto Analyst, Customer Support, Web Research
- **Plug & Play**: Easily add new tools or agents via decorators

---

## 📦 Repository Structure

```text
nexithium-agent-platform/
├── agents/                  Predefined agents configurations
│   └── crypto_analyst.py
├── core/                    Core engine components
│   ├── agent.py             Agent class and runner
│   ├── memory.py            Memory interfaces (ShortTerm, Persistent)
│   └── tools.py             Tool registry and loader
├── tools/                   External API wrappers and tools
│   ├── coingecko.py
│   ├── google_search.py
│   ├── tavily.py
│   ├── token_trend.py
│   ├── token_description.py
│   └── token_market_data.py
├── interfaces/              Interaction layers
│   ├── telegram_bot.py
│   ├── cli.py
│   └── fastapi_server.py
├── examples/                Example setups and launch scripts
│   └── crypto_telegram_bot.py
├── config.env.example       Template for environment variables
├── requirements.txt         Python dependencies
├── README.md                This documentation
└── LICENSE                  MIT License
```

---

## 🧰 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/nexithium/nexithium-agent-platform.git
cd nexithium-agent-platform
```

### 2. Create a virtual environment & install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the template and fill in your keys:

```bash
cp config.env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=sk-...
# TELEGRAM_BOT_TOKEN=12345:abcde
# NEXITHIUM_API_KEY=your-secret-key
# SERPER_API_KEY=your-serper-key
# REDIS_URL=redis://:password@host:6379/0
```

### 4. Run Example Telegram Bot

```bash
python examples/crypto_telegram_bot.py
```

- Open Telegram, start your bot, and try commands like `price btc`, `analyze sol`, or just say `hello`.

---

## 🖥️ Interfaces

### CLI

```bash
python interfaces/cli.py --memory long --user alice --model gpt-4 --verbose
```

- Type `help` for usage and `use get_price btc` to call tools directly.

### REST API (FastAPI)

```bash
uvicorn interfaces.fastapi_server:app --reload --port 8000
```

- Visit http://localhost:8000/docs for interactive Swagger UI.
- Use `X-API-Key: your-nexithium-api-key` header for `/chat` and `/tools` endpoints.

---

## 📖 Usage Examples

### Telegram Bot

```
You: price solana
Bot: Solana (SOL) is trading at $160.42 USD.

You: analyze eth
Bot:
Overview: Ethereum is...
Strengths: ...
Risks: ...
Use Cases: ...
Outlook: ...

This is not financial advice.
```

### CLI

```
$ python interfaces/cli.py
You> trend btc
Agent> Bitcoin trend: upward 📈 (2.34%)

You> use token_description sol
[Tool:token_description]> Solana is a high-performance blockchain...
```

### REST API

```bash
curl -X POST http://localhost:8000/chat \
  -H "X-API-Key: your-nexithium-api-key" \
  -H "Content-Type: application/json" \
  -d '{"input":"price btc"}'
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting pull requests and issues.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

© 2025 Nexithium. All rights reserved.
