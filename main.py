from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.auth import setup_auth_handlers  # Импорт функции настройки аутентификации
from handlers.logout import logout  # Импорт обработчика выхода
from keyboards import get_main_menu  # Импорт клавиатур
from config import config  # Импорт конфигурации
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    """Обработчик команды /start - первое сообщение при запуске бота"""
    await update.message.reply_text(
        "🎓 Добро пожаловать в бот колледжа!\n"
        "Для начала работы нажмите «🔐 Войти в систему»",
        reply_markup=get_main_menu()
    )

def main():
    try:
        # Создаем приложение бота
        app = ApplicationBuilder().token(config.TOKEN).build()
        
        # Регистрируем обработчики команд
        app.add_handler(CommandHandler("start", start))
        
        # Настраиваем обработчики аутентификации (из auth.py)
        setup_auth_handlers(app)
        
        # Обработчик выхода из аккаунта
        app.add_handler(MessageHandler(filters.Text(["🚪 Выйти из аккаунта"]), logout))
        
        # Запускаем бота
        logger.info("Бот успешно запущен")
        app.run_polling()
        
    except Exception as e:
        logger.critical(f"Ошибка запуска бота: {e}")
        raise

if __name__ == "__main__":
    main()