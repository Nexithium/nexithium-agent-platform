import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from core.agent import Agent
from core.memory import MemoryManager
from core.tools import load_all_tools, get_tool

from dotenv import load_dotenv
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# === Load environment ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# === Init agent ===
tools = load_all_tools()
memory = MemoryManager()

agent = Agent(
    name="CryptoVision",
    system_prompt=\"\"\"You are CryptoVision, an expert crypto analyst. Answer clearly, avoid hype, use tools when asked about tokens or prices. Always say 'This is not financial advice.' when giving analysis or forecasts.\"\"\",
    tools=list(tools.values()),
)

# === Telegram Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to CryptoVision Bot! Type something like 'price solana' or 'analyze bitcoin'.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = str(update.message.chat_id)

    mem = memory.get_memory(user_id)
    agent.memory = mem.get()

    response = agent.run(user_input)

    # Save to memory
    mem.add("user", user_input)
    mem.add("assistant", response)

    await update.message.reply_text(response)

# === Start Bot ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
