from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
import logging

logger = logging.getLogger(__name__)

async def handle_news(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📢 Последние новости:\n"
        "https://t.me/ваш_канал"
    )

def setup_news_handlers(app):
    app.add_handler(MessageHandler(
        filters.Text(["📢 Новости колледжа"]) & ~filters.COMMAND,
        handle_news
    ))