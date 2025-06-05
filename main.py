from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)
from handlers import (
    setup_auth_handlers,
    setup_schedule_handlers,
    setup_grades_handlers,
    setup_news_handlers,
    setup_feedback_handlers,
    setup_logout_handler
)
from keyboards import get_main_menu
from config import config
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🎓 Добро пожаловать в бот колледжа!",
        reply_markup=get_main_menu()
    )

async def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.error(f"Произошла ошибка: {context.error}")

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()
    
    # Регистрация всех обработчиков
    app.add_handler(CommandHandler("start", start))
    setup_auth_handlers(app)
    setup_schedule_handlers(app)
    setup_grades_handlers(app)
    setup_news_handlers(app)
    setup_feedback_handlers(app)
    setup_logout_handler(app)
    
    # Обработчик ошибок
    app.add_error_handler(error_handler)
    
    logger.info("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()