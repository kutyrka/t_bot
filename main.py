from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from config import Config  # Исправлено: Config вместо config
from keyboards import get_main_menu
from handlers.schedule import show_schedule_options, handle_week_choice
from handlers.grades import show_grades
from handlers.feedback import start_feedback, save_feedback
from handlers.news import show_news
import logging

async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    message = await update.message.reply_text(
        "Добро пожаловать в бот колледжа!",
        reply_markup=get_main_menu()
    )
    context.user_data['last_bot_message_id'] = message.message_id  # Исправлено: квадратные скобки

async def error_handler(update: object, context: CallbackContext):
    """Глобальный обработчик ошибок"""
    logging.error(f'Ошибка: {context.error}', exc_info=True)
    if update and isinstance(update, Update):
        await update.message.reply_text('⚠️ Произошла ошибка. Попробуйте позже.')

def main():
    """Точка входа приложения"""
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        app = ApplicationBuilder() \
            .token(Config.TOKEN) \
            .build()

        # Регистрация обработчиков
        handlers = [
            CommandHandler("start", start),
            MessageHandler(filters.Text(["📅 Расписание"]), show_schedule_options),
            MessageHandler(filters.Text(["📊 Оценки"]), show_grades),
            MessageHandler(filters.Text(["💬 Обращение"]), start_feedback),
            MessageHandler(filters.Text(["📢 Новости"]), show_news),
            MessageHandler(
                filters.Text(["Текущая неделя", "Следующая неделя"]),  # Исправлено: список кнопок
                handle_week_choice
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                save_feedback
            )
        ]

        for handler in handlers:
            app.add_handler(handler)

        app.add_error_handler(error_handler)

        logging.info("Бот успешно запущен")
        app.run_polling()

    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}", exc_info=True)

if __name__ == "__main__":
    main()