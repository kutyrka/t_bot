import matplotlib.pyplot as plt
from io import BytesIO
from typing import List

def generate_schedule_image(schedule_data, days_limit: int = 7) -> List[BytesIO]:
    """Генерация изображений расписания с ограничением по количеству дней"""
    try:
        if not schedule_data or not any(lessons for lessons in schedule_data.values()):
            raise ValueError("Нет данных для генерации расписания")

        # Разбиваем расписание на части по дням
        days = list(schedule_data.keys())
        images = []
        
        for start in range(0, len(days), days_limit):
            current_days = days[start:start + days_limit]
            current_schedule = {day: schedule_data[day] for day in current_days if schedule_data[day]}

            # Создаем фигуру для текущей части
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.axis('off')
            

            # Подготовка данных для таблицы
            table_data = [["День", "Время", "Предмет", "Аудитория"]]
            row_colors = ['lightgray']  # Цвет для заголовка таблицы
            current_color = 'lightgray'  # Цвет для заголовков дней
            
            for day, lessons in current_schedule.items():
                # Добавляем день как заголовок
                table_data.append([day, "", "", ""])
                row_colors.append(current_color)
                # Добавляем уроки
                for lesson in lessons:
                    table_data.append([
                        "",
                        lesson.get('time', ''),
                        lesson.get('subject', ''),
                        lesson.get('room', '')
                    ])
                    row_colors.append('white')  # Белый фон для строк с уроками
            
            if not table_data[1:]:  # Проверяем, есть ли данные после заголовка
                plt.close()
                continue

            # Создаем таблицу
            table = ax.table(
                cellText=table_data,
                loc='center',
                cellLoc='center',
                colWidths=[0.2, 0.2, 0.4, 0.2],
                cellColours=[[row_colors[i] if j == 0 else 'white' for j in range(4)] for i in range(len(table_data))]
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
            images.append(buf)
        
        if not images:
            raise ValueError("Не удалось сгенерировать ни одного изображения")
        
        return images
        
    except Exception as e:
        plt.close()
        raise RuntimeError(f"Ошибка генерации изображения: {str(e)}")