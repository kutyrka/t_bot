from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)
import logging

logger = logging.getLogger(__name__)

async def start_feedback(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💬 Введите ваш отзыв:",
        reply_markup=ReplyKeyboardRemove()
    )
    return "WAITING_FEEDBACK"

async def save_feedback(update: Update, context: CallbackContext):
    feedback = update.message.text
    # Сохранение в БД
    await update.message.reply_text(
        "✅ Спасибо за отзыв!",
        reply_markup=context.user_data.get('menu')
    )
    return ConversationHandler.END

def setup_feedback_handlers(app):
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text(["💬 Оставить отзыв"]), start_feedback)
        ],
        states={
            "WAITING_FEEDBACK": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)
            ]
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)