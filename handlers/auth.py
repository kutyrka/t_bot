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
        # Получение данных из сообщения
        credentials = update.message.text.strip().split(maxsplit=1)
        if len(credentials) != 2:
            logger.error("Неверный формат ввода логина/пароля")
            await update.message.reply_text("❌ Неверный формат. Введите: логин пароль")
            return AWAITING_CREDENTIALS
        
        username, password = credentials
        logger.info(f"Получены учетные данные: username={username}")
        logger.debug(f"Trying to authenticate user: {username}")

        # Запрос к таблице users
        user_response = config.supabase.table('users') \
            .select('*') \
            .eq('username', username) \
            .execute()
        
        logger.debug(f"User response: {user_response}")

        if not user_response.data:
            logger.warning("Пользователь не найден")
            await update.message.reply_text("❌ Пользователь не найден")
            return AWAITING_CREDENTIALS

        user = user_response.data[0]
        logger.info(f"Пользователь найден: {user['user_id']}, роль: {user['role_id']}")

        # Проверка пароля
        if user.get('password_hash') != password:
            logger.warning("Неверный пароль")
            await update.message.reply_text("❌ Неверный пароль")
            return AWAITING_CREDENTIALS

        # Получение данных студента, если role_id == 3
        student_data = None
        if user['role_id'] == 3:  # Для студентов
            if user['user_id'] < 3:  # Проверяем соответствие ID
                logger.error(f"Invalid student_id: {user['user_id']}")
                await update.message.reply_text("❌ Ошибка доступа к данным студента")
                return AWAITING_CREDENTIALS
            
            logger.debug(f"Fetching student data for user_id: {user['user_id']}")
            try:
                # Используем хранимую процедуру вместо прямого запроса
                student_response = config.supabase.rpc(
                    'get_student_data',
                    {'p_user_id': user['user_id']}
                ).execute()
                
                logger.debug(f"Student response: {student_response}")
                
                if student_response.data:
                    student_data = student_response.data
                    logger.info(f"Данные студента: {student_data}")
                else:
                    logger.warning("Нет данных для студента")
                    student_data = None
            except Exception as e:
                logger.error(f"Ошибка при получении данных студента: {str(e)}")
                student_data = None

        # Сохранение данных в контексте
        context.user_data.update({
            'authenticated': True,
            'user_id': user['user_id'],
            'role_id': user['role_id'],
            'full_name': f"{user['first_name']} {user['last_name']}",
            'group_id': student_data['group_id'] if student_data else None,
            'group_name': student_data['group_name'] if student_data else None,
            'schedule_id': student_data['schedule_id'] if student_data else None
        })
        
        logger.info(f"Сохранены данные в user_data: {context.user_data}")

        # Выбор меню в зависимости от роли
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

    except ValueError as ve:
        logger.error(f"Неверный формат ввода: {str(ve)}")
        await update.message.reply_text("❌ Неверный формат. Введите: логин пароль")
        return AWAITING_CREDENTIALS
    except Exception as e:
        logger.error(f"Ошибка авторизации: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Ошибка авторизации. Попробуйте позже")
        return AWAITING_CREDENTIALS

def setup_auth_handlers(app):
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(["🔐 Войти в систему"]), start_login)],
        states={
            AWAITING_CREDENTIALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_credentials)]
        },
        fallbacks=[],
        conversation_timeout=300  # Таймаут 5 минут
    )
    app.add_handler(conv_handler)