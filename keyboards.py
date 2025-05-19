from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["📅 Расписание", "📊 Оценки"],
        ["📢 Новости", "💬 Обращение"]
    ], resize_keyboard=True, one_time_keyboard=True)

def remove_keyboard():
    return ReplyKeyboardRemove()
