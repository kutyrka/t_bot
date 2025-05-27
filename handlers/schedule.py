from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from services.decorators import student_required  # Исправленный импорт
import logging

logger = logging.getLogger(__name__)

@student_required
async def handle_schedule(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text(
            f"📅 Расписание для группы {context.user_data.get('group_name', 'неизвестной группы')}\n"
            "Функция в разработке..."
        )
    except Exception as e:
        logger.error(f"Schedule error: {e}")
        await update.message.reply_text("⚠️ Ошибка загрузки расписания")

def setup_schedule_handlers(app):
    app.add_handler(MessageHandler(
        filters.Text(["📅 Расписание"]) & ~filters.COMMAND,
        handle_schedule
    ))