from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler
from config import config
from keyboards import get_student_menu, get_teacher_menu, get_admin_menu
import logging

logger = logging.getLogger(__name__)

AWAITING_CREDENTIALS = range(1)

async def start_login(update: Update, context: CallbackContext):
    logger.info("Начало процесса авторизации")
    await update.message.reply_text(
        "🔐 Введите ваш логин и пароль через пробел:\nПример: ivanov 12345",
        reply_markup=ReplyKeyboardRemove()
    )
    return AWAITING_CREDENTIALS

async def handle_credentials(update: Update, context: CallbackContext):
    try:
        username, password = update.message.text.strip().split(maxsplit=1)
        logger.info(f"Получены учетные данные: username={username}")

        user_response = config.supabase.table('users') \
            .select('*') \
            .eq('username', username) \
            .eq('password_hash', password) \
            .execute()

        if not user_response.data:
            logger.warning("Неверные логин или пароль")
            await update.message.reply_text("❌ Неверные логин или пароль")
            return AWAITING_CREDENTIALS

        user = user_response.data[0]
        logger.info(f"Пользователь найден: {user}")

        student_data = None
        if user['role_id'] == 3:
            student_response = config.supabase.table('students') \
                .select('group_id, groups(group_name, schedule_id)') \
                .eq('student_id', user['user_id']) \
                .execute()
            logger.info(f"Ответ от Supabase (students): {student_response.data}")
            student_data = student_response.data[0] if student_response.data else None
            logger.info(f"Данные студента: {student_data}")

        context.user_data.update({
            'authenticated': True,
            'user_id': user['user_id'],
            'role_id': user['role_id'],
            'full_name': f"{user['first_name']} {user['last_name']}",
            'group_id': student_data['group_id'] if student_data else None,
            'group_name': student_data['groups']['group_name'] if student_data else None,
            'schedule_id': student_data['groups']['schedule_id'] if student_data else None
        })
        logger.info(f"Сохранены данные в user_data: {context.user_data}")

        if user['role_id'] == 3:
            await update.message.reply_text(
                f"👋 Добро пожаловать, {user['first_name']}!",
                reply_markup=get_student_menu()
            )
        elif user['role_id'] == 2:
            await update.message.reply_text(
                f"👨‍🏫 Здравствуйте, {user['first_name']}!",
                reply_markup=get_teacher_menu()
            )
        else:
            await update.message.reply_text(
                f"🛠 Добро пожаловать, {user['first_name']}!",
                reply_markup=get_admin_menu()
            )

        return ConversationHandler.END

    except ValueError:
        logger.error("Неверный формат ввода логина/пароля")
        await update.message.reply_text("❌ Неверный формат. Введите: логин пароль")
        return AWAITING_CREDENTIALS
    except Exception as e:
        logger.error(f"Auth error: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Ошибка авторизации. Попробуйте позже")
        return AWAITING_CREDENTIALS

def setup_auth_handlers(app):
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(["🔐 Войти в систему"]), start_login)],
        states={
            AWAITING_CREDENTIALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_credentials)]
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)