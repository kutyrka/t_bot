from telegram import Update
from telegram.ext import CallbackContext
import matplotlib.pyplot as plt
from services.chat_cleaner import clean_chat
from io import BytesIO  # Добавить в импорты
import matplotlib.pyplot as plt

async def show_grades(update: Update, context: CallbackContext):
    try:
        # Создаём график
        fig, ax = plt.subplots()
        grades = [5, 4, 5, 3]
        subjects = ["Математика", "Физика", "Программирование", "История"]
        
        ax.bar(subjects, grades, color=['green', 'green', 'green', 'red'])
        ax.set_title("Ваши текущие оценки")
        
        # Конвертируем в изображение
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Отправляем
        await update.message.reply_photo(
            photo=buf,
            caption="📊 Успеваемость:",
            reply_markup=get_main_menu()  # Импортировать из keyboards
        )
        buf.close()
        plt.close()
        
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")