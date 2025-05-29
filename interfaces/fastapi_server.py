#!/usr/bin/env python3
"""
FastAPI server for Nexithium Agent Platform.
Provides REST endpoints to interact with AI agents and their tools.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Dict
import os
from dotenv import load_dotenv

from core.agent import Agent
from core.memory import MemoryManager, PersistentMemory
from core.tools import load_all_tools, get_tool, list_tools

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEXITHIUM_API_KEY = os.getenv("NEXITHIUM_API_KEY", "secret-key")

# API key security
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != NEXITHIUM_API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

# Initialize FastAPI app
app = FastAPI(
    title="Nexithium Agent API",
    description="REST API for interacting with AI agents and crypto tools.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Load tools and memory manager
tool_registry = load_all_tools()
memory_manager = MemoryManager()

# Define system prompt
SYSTEM_PROMPT = """
You are CryptoVisionAPI — a professional crypto market analysis assistant.
Provide clear, accurate, and neutral answers. Use your tools when needed.
Never provide investment advice.
"""

# Initialize agent
agent = Agent(
    name="CryptoVisionAPI",
    system_prompt=SYSTEM_PROMPT,
    tools=list(tool_registry.values()),
    memory=[]
)

# Pydantic schema for chat
class ChatRequest(BaseModel):
    input: str

# Root endpoint
@app.get("/", tags=["Meta"])
async def root():
    """Health check endpoint."""
    return {"message": "Nexithium Agent API is up and running!"}

# List available tools
@app.get("/tools", tags=["Meta"], dependencies=[Depends(verify_api_key)])
async def get_tools() -> Dict[str, str]:
    """Return available tool names."""
    return {"tools": list_tools()}

# Chat endpoint
@app.post("/chat", tags=["Agent"], dependencies=[Depends(verify_api_key)])
async def chat_endpoint(request: ChatRequest):
    """
    Interact with the AI agent. 
    Supported commands:
    - `price <TOKEN>`: get real-time price
    - `trend <TOKEN>`: short-term trend
    - `analyze <TOKEN>`: detailed analysis
    - `forecast <TOKEN>`: scenario forecast
    - `tools`: list tools
    Any other text is treated as free-form chat.
    """
    user_input = request.input.strip()
    user_id = "api_user"
    mem = memory_manager.get_memory(user_id)

    # Save user message
    mem.add("user", user_input)
    agent.memory = mem.get()

    parts = user_input.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    # Handle built-in tool commands
    if cmd == "price" and arg:
        response = get_tool("get_price")(arg)
    elif cmd == "trend" and arg:
        response = get_tool("token_trend")(arg)
    elif cmd == "analyze" and arg:
        response = agent.run(f"Analyze {arg}. Include overview, strengths, risks, use cases, outlook.")
    elif cmd == "forecast" and arg:
        response = agent.run(f"Forecast scenarios for {arg}. Hypothetical scenario, not financial advice.")
    elif cmd == "tools":
        response = ", ".join(list_tools())
    else:
        # Free-form chat
        response = agent.run(user_input)

    # Save assistant message
    mem.add("assistant", response)

    return {"response": response}
