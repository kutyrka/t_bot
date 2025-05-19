from telegram import Update
from telegram.ext import CallbackContext

CHANNEL_LINK = "https://t.me/your_college_channel"

async def show_news(update: Update, context: CallbackContext):
    await update.message.reply_text(
        f"Последние новости колледжа: {CHANNEL_LINK}",
        disable_web_page_preview=True
    )