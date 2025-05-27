from telegram import Update
from telegram.ext import CallbackContext
from services.schedule_generator import generate_schedule_image
from services.parser import parse_schedule
from io import BytesIO
from keyboards import get_main_menu
import logging
from decorators import student_required

@student_required
async def show_schedule(update: Update, context: CallbackContext):
    try:
        # Получаем расписание для студента
        schedule = config.supabase.table('schedule') \
            .select('*') \
            .eq('group_id', context.user_data['group_id']) \
            .execute()
        
        await update.message.reply_text("Ваше расписание на неделю...")
    except Exception as e:
        await update.message.reply_text("Ошибка загрузки расписания")