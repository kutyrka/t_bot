from telegram import Update
from telegram.ext import CallbackContext
from keyboards import get_main_menu

async def logout(update: Update, context: CallbackContext):
    """Очищаем данные сессии и показываем главное меню"""
    context.user_data.clear()
    await update.message.reply_text(
        "Вы вышли из системы. Чтобы снова войти, нажмите «🔐 Войти в систему»",
        reply_markup=get_main_menu()
    )