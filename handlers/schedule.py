from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from services.schedule_generator import generate_schedule_image
from io import BytesIO

async def show_schedule_options(update: Update, context: CallbackContext):
    message = await update.message.reply_text(
        "Выберите неделю:",
        reply_markup=schedule_keyboard
    )
    context.user_data['last_bot_message_id'] = message.message_id

async def handle_week_choice(update: Update, context: CallbackContext):
    week_type = update.message.text
    
    # Заглушка данных - замените реальными
    schedule_data = {
        "Понедельник": [{"time": "09:00", "subject": "Математика", "room": "304"}],
        "Вторник": [{"time": "10:00", "subject": "Физика", "room": "412"}]
    }
    
    image = generate_schedule_image(schedule_data)
    await update.message.reply_photo(
        photo=image,
        caption=f"Расписание на {week_type.lower()}",
        reply_markup=get_main_menu()  # Импортировать из keyboards
    )
    image.close()