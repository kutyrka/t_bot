from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove  # Добавить в импорты

async def start_feedback(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📝 Опишите ваше обращение или проблему:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )
    context.user_data['awaiting_feedback'] = True

async def save_feedback(update: Update, context: CallbackContext):
    if 'awaiting_feedback' in context.user_data:
        feedback_text = update.message.text
        # Здесь сохраняем обращение (пока заглушка)
        await update.message.reply_text(
            "✅ Ваше обращение принято!",
            reply_markup=get_main_menu()  # Импортировать из keyboards
        )
        del context.user_data['awaiting_feedback']