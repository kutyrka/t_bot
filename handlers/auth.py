from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters
from config import config
from keyboards import get_student_menu, get_teacher_menu, get_admin_menu
import logging

logger = logging.getLogger(__name__)

async def start_login(update: Update, context: CallbackContext):
    """Запрос логина и пароля"""
    await update.message.reply_text(
        "🔐 Введите ваш логин и пароль через пробел:\nПример: ivanov 12345",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['auth_stage'] = 'awaiting_credentials'

async def handle_credentials(update: Update, context: CallbackContext):
    """Обработка введенных данных"""
    if context.user_data.get('auth_stage') != 'awaiting_credentials':
        return

    try:
        username, password = update.message.text.strip().split(maxsplit=1)
        
        # Получаем данные пользователя
        user_response = config.supabase.table('users') \
            .select('*') \
            .eq('username', username) \
            .eq('password_hash', password) \
            .execute()

        if not user_response.data:
            await update.message.reply_text("❌ Неверные логин или пароль")
            return

        user = user_response.data[0]
        
        # Получаем данные студента (если есть)
        student_data = None
        if user['role_id'] == 3:  # Только для студентов
            student_response = config.supabase.table('students') \
                .select('group_id, groups(group_name, schedule_id)') \
                .eq('student_id', user['user_id']) \
                .execute()
            student_data = student_response.data[0] if student_response.data else None

        # Сохраняем данные в контекст
        context.user_data.update({
            'authenticated': True,
            'user_id': user['user_id'],
            'role_id': user['role_id'],
            'full_name': f"{user['first_name']} {user['last_name']}",
            'group_id': student_data['group_id'] if student_data else None,
            'group_name': student_data['groups']['group_name'] if student_data else None,
            'schedule_id': student_data['groups']['schedule_id'] if student_data else None
        })

        # Показываем соответствующее меню
        if user['role_id'] == 3:  # Студент
            await update.message.reply_text(
                f"👋 Добро пожаловать, {user['first_name']}!",
                reply_markup=get_student_menu()
            )
        elif user['role_id'] == 2:  # Преподаватель
            await update.message.reply_text(
                f"👨‍🏫 Здравствуйте, {user['first_name']}!",
                reply_markup=get_teacher_menu()
            )
        else:  # Админ
            await update.message.reply_text(
                f"🛠 Добро пожаловать, {user['first_name']}!",
                reply_markup=get_admin_menu()
            )

    except ValueError:
        await update.message.reply_text("❌ Неверный формат. Введите: логин пароль")
    except Exception as e:
        logger.error(f"Auth error: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Ошибка авторизации. Попробуйте позже")
    finally:
        context.user_data.pop('auth_stage', None)

def setup_auth_handlers(app):
    app.add_handler(MessageHandler(filters.Text(["🔐 Войти в систему"]), start_login))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_credentials))