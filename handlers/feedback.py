from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)
from config import config
import logging
from datetime import datetime
import aiohttp

logger = logging.getLogger(__name__)

WAITING_FEEDBACK = "WAITING_FEEDBACK"

async def start_feedback(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['user_id'] = user_id
    await update.message.reply_text(
        "💬 Напишите ваш отзыв или предложение:",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FEEDBACK

async def save_feedback(update: Update, context: CallbackContext):
    try:
        telegram_id = update.message.from_user.id
        feedback_text = update.message.text.strip()

        if not feedback_text:
            await update.message.reply_text("⚠️ Отзыв не может быть пустым")
            return WAITING_FEEDBACK

        # Получаем user_id из public.users
        user_data = config.supabase.table('users') \
            .select('user_id') \
            .eq('telegram_id', telegram_id) \
            .limit(1) \
            .execute()
        
        if not user_data.data:
            await update.message.reply_text("⚠️ Пользователь не найден")
            return ConversationHandler.END
            
        user_id = user_data.data[0]['user_id']

        # Сохраняем отзыв через RPC
        response = config.supabase.rpc(
            'add_feedback_safe',
            {
                'p_user_id': user_id,
                'p_text': feedback_text[:1000]
            }
        ).execute()

        await update.message.reply_text("✅ Отзыв сохранён!")
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Ошибка сервера")
        return ConversationHandler.END

def setup_feedback_handlers(app):
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(["💬 Оставить отзыв"]), start_feedback)],
        states={WAITING_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)]},
        fallbacks=[],
        conversation_timeout=300
    )
    app.add_handler(conv_handler)