from telegram import ReplyKeyboardMarkup

def get_student_menu():
    return ReplyKeyboardMarkup([
        ["📅 Расписание", "📊 Мои оценки"],
        ["📢 Новости колледжа", "💬 Оставить отзыв"],
        ["🚪 Выйти из аккаунта"]  # Измененная кнопка
    ], resize_keyboard=True)

def get_main_menu():
    """Главное меню для неавторизованных пользователей"""
    return ReplyKeyboardMarkup([
        ["🔐 Войти в систему"]
    ], resize_keyboard=True)

def get_teacher_menu():
    return ReplyKeyboardMarkup([
        ["📝 Проставить оценки", "📚 Учебные материалы"],
        ["🚪 Выйти"]
    ], resize_keyboard=True)

def get_admin_menu():
    return ReplyKeyboardMarkup([
        ["📝 Модерация отзывов"],
        ["🚪 Выйти"]
    ], resize_keyboard=True)