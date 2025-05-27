from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove  # Добавить в импорты

from decorators import student_required

@student_required
async def start_feedback(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📝 Введите ваш отзыв или обращение (анонимно):",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['awaiting_feedback'] = True

@student_required
async def save_feedback(update: Update, context: CallbackContext):
    if 'awaiting_feedback' in context.user_data:
        # Сохраняем в БД без привязки к пользователю
        feedback = update.message.text
        supabase.table('feedbacks').insert({
            'text': feedback,
            'date': 'now()'
        }).execute()
        
        await update.message.reply_text(
            "✅ Ваш отзыв сохранен анонимно",
            reply_markup=get_main_menu()
        )