import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
from core.agent import Agent
from tools.coingecko import get_price

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import openai
openai.api_key = OPENAI_API_KEY

crypto_agent = Agent(
    name="CryptoVision",
    system_prompt="""
You are CryptoVision — a professional crypto market analyst.
You answer clearly, concisely, and accurately. Use logic, token fundamentals, and macro context.
If the user asks about price, try to use your tools. Never provide financial advice.
""",
    tools=[get_price],
    memory=[]
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input.lower().startswith("price"):
        parts = user_input.split()
        if len(parts) >= 2:
            result = get_price(parts[1])
        else:
            result = "Please specify a token symbol, e.g. 'price BTC'"
    else:
        result = crypto_agent.run(user_input)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 CryptoVision Telegram bot is running...")
    app.run_polling()
