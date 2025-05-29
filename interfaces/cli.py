#!/usr/bin/env python3
"""
CLI interface for Nexithium Agent Platform.
Allows interactive chat with any registered AI agent and its tools.
Usage:
  python cli.py [--agent AGENT_NAME] [--memory short|long] [--model MODEL] [--verbose]
"""
import argparse
import logging
import sys

from core.agent import Agent
from core.memory import ShortTermMemory, PersistentMemory, MemoryManager
from core.tools import load_all_tools, get_tool, list_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CLI")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Nexithium AI Agent CLI Interface"
    )
    parser.add_argument(
        "--agent", type=str, default="CryptoVision",
        help="Name of the agent to use (default: CryptoVision)"
    )
    parser.add_argument(
        "--memory", choices=["short", "long"], default="short",
        help="Memory type: short (session) or long (persistent)"
    )
    parser.add_argument(
        "--user", type=str, default="cli_user",
        help="User ID for persistent memory (if --memory long)"
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4",
        help="OpenAI model name to use (e.g. gpt-4, gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose (debug) logging"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    logger.info(f"Starting CLI Agent with model={args.model}, memory={args.memory}")

    # Load all tools
    tools = load_all_tools()
    tool_names = list_tools()
    logger.debug(f"Available tools: {tool_names}")

    # Initialize memory
    if args.memory == "short":
        memory = ShortTermMemory(window_size=10)
    else:
        memory = PersistentMemory(user_id=args.user)

    # Setup agent
    # For demonstration, using a basic system prompt; can be customized per agent
    system_prompt = (
        "You are {agent_name}, a professional AI crypto analyst. "
        "Answer clearly, use tools when appropriate, and never provide financial advice."
    ).format(agent_name=args.agent)
    agent = Agent(
        name=args.agent,
        system_prompt=system_prompt,
        tools=list(tools.values()),
        memory=memory.get(),
        model=args.model
    )

    # Interactive loop
    print("\n=== Nexithium CLI Agent ===")
    print("Type 'help' for commands, 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if user_input.lower() == "help":
            print("Commands:")
            print("  help                 Show this help message")
            print("  exit, quit           Exit the CLI")
            print("  tools                List available tools")
            print("  use <tool> [args]    Invoke a tool with arguments")
            print("  <any other text>     Chat with the AI agent")
            continue
        if user_input.lower() == "tools":
            print("Available tools:")
            for name in tool_names:
                print(f"  - {name}")
            continue

        parts = user_input.split()
        if parts[0] == "use":
            tool_name = parts[1]
            args = parts[2:]
            try:
                tool_func = get_tool(tool_name)
                result = tool_func(*args)
                print(f"[Tool:{tool_name}]> {result}")
            except Exception as e:
                print(f"Error invoking tool '{tool_name}': {e}")
            continue

        # Default: send to agent
        memory.add("user", user_input)
        agent.memory = memory.get()
        response = agent.run(user_input)
        print(f"Agent> {response}\n")
        memory.add("assistant", response)


if __name__ == "__main__":
    main()
