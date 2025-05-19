from telegram import Update
from telegram.ext import CallbackContext

async def clean_chat(update: Update, context: CallbackContext):
    try:
        if 'last_bot_message_id' in context.user_data:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.user_data'last_bot_message_id'
            )
        await update.message.delete()
    except Exception as e:
        logging.error(f"Ошибка при очистке чата: {e}")
