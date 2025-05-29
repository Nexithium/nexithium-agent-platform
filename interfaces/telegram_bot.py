#!/usr/bin/env python3
"""
Telegram Bot interface for Nexithium Agent Platform.
Enables users to chat with AI agent, invoke tools, and use inline menu.
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from dotenv import load_dotenv
from core.agent import Agent
from core.memory import MemoryManager
from core.tools import load_all_tools, list_tools, get_tool

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("NEXITHIUM_API_KEY", "secret-key")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize core components
tools = load_all_tools()
memory_manager = MemoryManager()

# System prompt template
SYSTEM_PROMPT = (
    "You are CryptoVision, a professional AI crypto analyst. "
    "Answer clearly, use tools when appropriate, and never provide financial advice."
)

# Instantiate Agent
agent = Agent(
    name="CryptoVision",
    system_prompt=SYSTEM_PROMPT,
    tools=list(tools.values()),
    memory=[]
)

# Inline menu keyboard
MENU_KEYBOARD = [
    [InlineKeyboardButton("📈 Price", callback_data='tool:get_price')],
    [InlineKeyboardButton("📊 Trend", callback_data='tool:token_trend')],
    [InlineKeyboardButton("🔍 Analyze", callback_data='analyze')],
    [InlineKeyboardButton("🔮 Forecast", callback_data='forecast')],
]
MENU_MARKUP = InlineKeyboardMarkup(MENU_KEYBOARD)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and menu."""
    await update.message.reply_text(
        "👋 Welcome to CryptoVision Bot! Use the menu or type commands.",
        reply_markup=MENU_MARKUP
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display help text."""
    help_text = (
        "/start - show menu
"        "help - show this message
"        "price <symbol> - get current price
"        "trend <symbol> - get 2-day trend
"        "analyze <symbol> - project analysis
"        "forecast <symbol> - future scenario
"        "tools - list available tools
"    )
    await update.message.reply_text(help_text)

async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List registered tools."""
    names = list_tools()
    await update.message.reply_text("Available tools: " + ", ".join(names))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main text handler: commands or free chat."""
    user_input = update.message.text.strip()
    user_id = str(update.message.chat_id)
    mem = memory_manager.get_memory(user_id)

    # Authentication stub (if needed)
    # if context.bot_data.get('api_key') != API_KEY:
    #     await update.message.reply_text("Unauthorized")
    #     return

    # Menu commands
    if user_input.lower() == 'menu':
        await update.message.reply_text("Select an option:", reply_markup=MENU_MARKUP)
        return
    if user_input.lower() == 'help':
        await help_command(update, context)
        return
    if user_input.lower() == 'tools':
        await tools_command(update, context)
        return

    parts = user_input.split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ''

    # Tool invocation
    if cmd in tools:
        result = get_tool(cmd)(arg)
        await update.message.reply_text(result)
        return

    # Predefined commands
    if cmd == 'price' and arg:
        result = get_tool('get_price')(arg)
    elif cmd == 'trend' and arg:
        result = get_tool('token_trend')(arg)
    elif cmd == 'analyze' and arg:
        # analysis via agent
        mem.add('user', user_input)
        agent.memory = mem.get()
        result = agent.run(f"Analyze {arg}. Include overview, strengths, risks, use cases, outlook.")
    elif cmd == 'forecast' and arg:
        mem.add('user', user_input)
        agent.memory = mem.get()
        result = agent.run(f"Forecast scenarios for {arg}. Hypothetical, not financial advice.")
    else:
        # free chat through agent
        mem.add('user', user_input)
        agent.memory = mem.get()
        result = agent.run(user_input)

    # Save memory and reply
    mem.add('assistant', result)
    await update.message.reply_text(result)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback for inline menu buttons."""
    query = update.callback_query
    await query.answer()
    data = query.data  # format 'tool:get_price' or 'analyze'

    if data.startswith('tool:'):
        tool_name = data.split(':',1)[1]
        content = ''
        if tool_name in tools:
            content = get_tool(tool_name)('')
        else:
            content = f"Tool {tool_name} not found."
    elif data == 'analyze':
        content = "Send 'analyze SOL' or /analyze to use analysis."
    elif data == 'forecast':
        content = "Send 'forecast ETH' or /forecast to get a forecast."
    else:
        content = "Unknown option."

    await query.edit_message_text(text=content)

# --- Main ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('tools', tools_command))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
