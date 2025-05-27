from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
import logging

logger = logging.getLogger(__name__)

def student_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if not context.user_data.get('authenticated'):
            await update.message.reply_text("🔒 Требуется авторизация")
            return
        if context.user_data.get('role_id') != 3:  # 3 - роль студента
            await update.message.reply_text("🚫 Доступ только для студентов")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper