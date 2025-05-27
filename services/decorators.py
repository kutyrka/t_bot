from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext

def student_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if not context.user_data.get('authenticated'):
            await update.message.reply_text("🔒 Требуется авторизация. Введите логин и пароль")
            return
        if context.user_data.get('role') != 'student':
            await update.message.reply_text("🚫 Доступ только для студентов")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper