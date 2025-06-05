from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
import logging

logger = logging.getLogger(__name__)

def student_required(func):
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        logger.info(f"Проверка декоратора student_required для пользователя: {update.effective_user.id}")
        logger.info(f"Состояние user_data: {context.user_data}")
        
        if not context.user_data.get('authenticated'):
            logger.warning("Пользователь не авторизован")
            await update.message.reply_text("🔒 Требуется авторизация")
            return
        if context.user_data.get('role_id') != 3:  # 3 - роль студента
            logger.warning(f"Роль пользователя: {context.user_data.get('role_id')}, доступ запрещён")
            await update.message.reply_text("🚫 Доступ только для студентов")
            return
        
        logger.info("Проверка декоратора пройдена, вызываем функцию")
        return await func(update, context, *args, **kwargs)
    return wrapper