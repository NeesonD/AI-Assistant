from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, ContextTypes
from telegram import Update
import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)
from config import TOKEN
from coder import SystemMsg


chat = ChatOpenAI(temperature=0)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

messages = [
    SystemMessage(content=SystemMsg)
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="init bot success")


async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages.append(HumanMessage(content=update.message.text))
    result = chat(messages)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result.content)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    code_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), code)

    application.add_handler(start_handler)
    application.add_handler(code_handler)

    application.run_polling()
