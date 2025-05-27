from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from services.decorators import student_required  # Исправленный импорт
import logging

logger = logging.getLogger(__name__)

@student_required
async def handle_grades(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text(
            f"📊 Оценки для группы {context.user_data.get('group_name', 'неизвестной группы')}\n"
            "Функция в разработке..."
        )
    except Exception as e:
        logger.error(f"Grades error: {e}")
        await update.message.reply_text("⚠️ Ошибка загрузки оценок")

def setup_grades_handlers(app):
    app.add_handler(MessageHandler(
        filters.Text(["📊 Мои оценки"]) & ~filters.COMMAND,
        handle_grades
    ))