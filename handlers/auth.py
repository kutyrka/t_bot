from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters
from keyboards import get_student_menu
from config import config
import logging

logger = logging.getLogger(__name__)

async def start_login(update: Update, context: CallbackContext):
    """Запрашиваем логин и пароль"""
    await update.message.reply_text(
        "🔐 Введите ваш логин и пароль через пробел:\n"
        "Пример: ivanov 123456",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['auth_stage'] = 'awaiting_credentials'

async def handle_credentials(update: Update, context: CallbackContext):
    if context.user_data.get('auth_stage') != 'awaiting_credentials':
        return
    
    try:
        username, password = update.message.text.strip().split(maxsplit=1)
        
        # Ищем пользователя в Supabase
        response = config.supabase.table('users') \
            .select('user_id, role_id, first_name, last_name') \
            .eq('username', username) \
            .eq('password_hash', password) \
            .maybe_single() \
            .execute()

        if not response.data:
            await update.message.reply_text("❌ Неверные логин или пароль")
            return

        user = response.data
        
        # Проверяем, что это студент (role_id = 3)
        if user['role_id'] != 3:
            await update.message.reply_text("🚫 Доступ только для студентов")
            return

        # Сохраняем данные в user_data
        context.user_data.update({
            'authenticated': True,
            'user_id': user['user_id'],
            'role': 'student',
            'full_name': f"{user['first_name']} {user['last_name']}"
        })
        
        # Получаем group_id из таблицы students
        student_data = config.supabase.table('students') \
            .select('group_id') \
            .eq('student_id', user['user_id']) \
            .single() \
            .execute()
        
        if student_data.data:
            context.user_data['group_id'] = student_data.data['group_id']

        # Показываем меню студента
        await update.message.reply_text(
            f"👋 Добро пожаловать, {user['first_name']}!\n"
            "Вы успешно авторизовались как студент.",
            reply_markup=get_student_menu()
        )
        
        # Сбрасываем stage авторизации
        context.user_data.pop('auth_stage', None)

    except ValueError:
        await update.message.reply_text("❌ Неверный формат. Введите: логин пароль")
    except Exception as e:
        logger.error(f"Auth error: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Произошла ошибка при авторизации")

def setup_auth_handlers(app):
    app.add_handler(MessageHandler(filters.Text(["🔐 Войти в систему"]), start_login))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_credentials))