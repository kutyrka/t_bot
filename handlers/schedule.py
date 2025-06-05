from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from services.decorators import student_required
from services.parser import parser
from services.schedule_generator import generate_schedule_image
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

@student_required
async def handle_schedule(update: Update, context: CallbackContext):
    try:
        logger.info("Вызвана функция handle_schedule")
        schedule_id = context.user_data.get('schedule_id')
        if not schedule_id:
            logger.warning("schedule_id не найден в user_data")
            await update.message.reply_text("⚠️ Не удалось определить вашу группу. Обратитесь к администратору.")
            return

        # Получаем расписание
        schedule = await parser.parse_schedule(schedule_id)
        logger.info(f"Получено расписание: {schedule}")
        if not schedule:
            logger.warning("Расписание не найдено")
            await update.message.reply_text("⚠️ Расписание не найдено. Попробуйте позже.")
            return

        # Генерируем изображения
        image_buffers = generate_schedule_image(schedule, days_limit=7)
        
        # Отправляем каждое изображение
        for idx, image_buffer in enumerate(image_buffers, 1):
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_buffer,
                caption=f"📅 Расписание для группы {context.user_data.get('group_name', 'неизвестной группы')} (Часть {idx})"
            )
            image_buffer.close()  # Закрываем буфер после отправки

    except Exception as e:
        logger.error(f"Schedule error: {e}")
        await update.message.reply_text("⚠️ Ошибка загрузки расписания. Проверьте логи.")

def setup_schedule_handlers(app):
    app.add_handler(MessageHandler(
        filters.Regex(r'📅\s*Расписание'),
        handle_schedule
    ))