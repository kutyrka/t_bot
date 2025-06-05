from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from keyboards import get_main_menu

async def logout(update: Update, context: CallbackContext):
    """Очищаем данные сессии и показываем главное меню"""
    context.user_data.clear()
    await update.message.reply_text(
        "Вы вышли из системы. Чтобы снова войти, нажмите «🔐 Войти в систему»",
        reply_markup=get_main_menu()
    )

def setup_logout_handler(app):
    """Регистрируем обработчик для выхода из системы"""
    app.add_handler(MessageHandler(
        filters.Text(["🚪 Выйти из аккаунта", "🚪 Выйти"]) & ~filters.COMMAND,
        logout
    ))