import matplotlib.pyplot as plt
from io import BytesIO

def generate_schedule_image(week_data):
    """Генерация изображения расписания"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Пример данных (замените реальными)
    table_data = [["Время", "Предмет", "Аудитория"]]
    for day, lessons in week_data.items():
        table_data.append([f"📌 {day}", "", ""])
        for lesson in lessons:
            table_data.append([lesson['time'], lesson['subject'], lesson['room']])
    
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf