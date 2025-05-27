import matplotlib.pyplot as plt
from io import BytesIO

def generate_schedule_image(schedule_data):
    """Генерация изображения расписания с базовым стилем"""
    try:
        # Создаем фигуру
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('off')
        
        # Подготовка данных для таблицы
        table_data = [["День", "Время", "Предмет", "Аудитория"]]
        
        for day, lessons in schedule_data.items():
            table_data.append([day, "", "", ""])
            for lesson in lessons:
                table_data.append([
                    "",
                    lesson.get('time', ''),
                    lesson.get('subject', ''),
                    lesson.get('room', '')
                ])
        
        # Создаем таблицу
        table = ax.table(
            cellText=table_data,
            loc='center',
            cellLoc='center',
            colWidths=[0.2, 0.2, 0.4, 0.2]
        )
        
        # Базовое форматирование
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        
        # Сохранение в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
        buf.seek(0)
        plt.close()
        return buf
        
    except Exception as e:
        plt.close()
        raise RuntimeError(f"Ошибка генерации изображения: {str(e)}")