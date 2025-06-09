import logging
from telegram import Update
from telegram.ext import MessageHandler, filters, CallbackContext
from services.decorators import student_required
import aiohttp
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List
from config import config

logger = logging.getLogger(__name__)

async def fetch_subjects_for_group(group_id: int) -> List[str]:
    """Получение всех предметов группы из Supabase."""
    try:
        logger.debug(f"Fetching subjects for group {group_id}")
        
        # Вариант 1: Через хранимую функцию (рекомендуется)
        response = config.supabase.rpc(
            'get_group_subjects', 
            {'p_group_id': group_id}
        ).execute()
        
        # Или Вариант 2: Прямой запрос с явным указанием схемы
        # response = config.supabase.from_('public.group_subjects') \
        #     .select('subject:subjects(subject_name)') \
        #     .eq('group_id', group_id) \
        #     .execute()
        
        if not response.data:
            logger.warning(f"No subjects found for group {group_id}")
            return []
            
        subjects = [item['subject_name'] for item in response.data]
        logger.info(f"Found subjects: {subjects}")
        return subjects
        
    except Exception as e:
        logger.error(f"Error fetching subjects: {e}", exc_info=True)
        return []

async def fetch_grades(student_id: int) -> Dict[str, List[str]]:
    """Получение оценок студента из Supabase."""
    try:
        # Вариант 1: Через хранимую функцию (рекомендуется)
        response = config.supabase.rpc(
            'get_student_grades',
            {'p_student_id': student_id}
        ).execute()
        
        # Или Вариант 2: Прямой запрос с явным JOIN
        # response = config.supabase.from_('student_grades') \
        #     .select('grade_value, subjects!inner(subject_name)') \
        #     .eq('student_id', student_id) \
        #     .order('date') \
        #     .execute()
        
        grades_by_subject = {}
        for entry in response.data:
            subject_name = entry['subject_name']
            grade = str(entry['grade_value'])
            grades_by_subject.setdefault(subject_name, []).append(grade)
            
        logger.debug(f"Grades data: {grades_by_subject}")
        return grades_by_subject
        
    except Exception as e:
        logger.error(f"Error fetching grades: {e}", exc_info=True)
        return {}

def generate_grades_image(subjects: List[str], grades_data: Dict[str, List[str]]) -> List[BytesIO]:
    """Генерация изображения с таблицей оценок: все предметы группы, 15 оценок."""
    try:
        if not subjects:
            raise ValueError("Нет предметов для генерации таблицы оценок")

        # Подготовка данных для таблицы
        table_data = [["Предмет"] + [f"Оценка {i+1}" for i in range(15)]]
        for subject in subjects:
            grades = grades_data.get(subject, [])
            # Заполняем до 15 оценок, недостающие - "-"
            grades.extend(["-"] * (15 - len(grades)))
            table_data.append([subject] + grades[:15])

        # Создаём изображение
        fig, ax = plt.subplots(figsize=(15, len(table_data) * 0.5))
        ax.axis('off')

        # Создаём таблицу
        table = ax.table(
            cellText=table_data,
            loc='center',
            cellLoc='center',
            colWidths=[0.2] + [0.05] * 15,
            cellColours=[['lightgray'] * 16] + [['white'] * 16 for _ in range(len(table_data) - 1)]
        )

        # Настраиваем форматирование таблицы
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)

        # Настраиваем границы таблицы
        for (i, j), cell in table.get_celld().items():
            cell.set_edgecolor('black')
            cell.set_linewidth(0.5)

        # Сохранение в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        plt.close()
        return [buf]

    except Exception as e:
        plt.close()
        logger.error(f"Ошибка генерации изображения: {e}")
        raise RuntimeError(f"Ошибка генерации изображения: {str(e)}")

@student_required
async def handle_grades(update: Update, context: CallbackContext):
    """Обработчик команды '📊 Мои оценки'"""
    try:
        logger.info("Вызвана функция handle_grades")
        student_id = context.user_data.get('user_id')
        group_id = context.user_data.get('group_id')
        if not student_id or not group_id:
            logger.warning("student_id или group_id не найдены в user_data")
            await update.message.reply_text("⚠️ Не удалось определить ваш ID или группу. Обратитесь к администратору.")
            return

        # Получаем все предметы группы
        subjects = await fetch_subjects_for_group(group_id)
        if not subjects:
            logger.warning("Предметы для группы не найдены")
            await update.message.reply_text("⚠️ Предметы для вашей группы не найдены. Попробуйте позже.")
            return

        # Получаем оценки
        grades = await fetch_grades(student_id)
        if not grades:
            logger.info("Оценки не найдены, но предметы будут отображены")

        # Генерируем изображение
        image_buffers = generate_grades_image(subjects, grades)
        
        # Отправляем изображение
        for idx, image_buffer in enumerate(image_buffers, 1):
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_buffer,
                caption=f"📊 Ваши оценки"
            )
            image_buffer.close()

    except Exception as e:
        logger.error(f"Grades error: {e}")
        await update.message.reply_text("⚠️ Ошибка загрузки оценок. Проверьте логи.")

def setup_grades_handlers(app):
    """Настройка обработчиков для оценок"""
    app.add_handler(MessageHandler(
        filters.Regex(r'📊\s*Мои\s*оценки'),
        handle_grades
    ))