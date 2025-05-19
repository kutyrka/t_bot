import requests
from bs4 import BeautifulSoup

def parse_schedule(url):
    try:
        # Загружаем страницу
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        
        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим таблицу с расписанием
        table = soup.find('table', {'class': 'table table-main table-bordered'})
        
        if not table:
            print("Таблица расписания не найдена!")
            return
        
        # Извлекаем данные
        schedule = []
        current_date = ""
        
        for row in table.find_all('tr'):
            # Проверяем, является ли строка заголовком с датой
            date_header = row.find('th', {'class': 'td-left'})
            if date_header:
                current_date = date_header.get_text(strip=True)
                continue
            
            # Извлекаем данные из обычной строки
            cols = row.find_all('td')
            if len(cols) >= 6:  # Проверяем, что строка содержит все нужные колонки
                time = cols[0].get_text(strip=True)
                form = cols[1].get_text(strip=True)
                subject = cols[2].get_text(strip=True)
                teacher = cols[3].get_text(strip=True)
                room = cols[4].get_text(strip=True)
                note = cols[5].get_text(strip=True)
                
                schedule.append({
                    'date': current_date,
                    'time': time,
                    'form': form,
                    'subject': subject,
                    'teacher': teacher,
                    'room': room,
                    'note': note
                })
        
        # Выводим результат в консоль
        for entry in schedule:
            print(f"{entry['date']} | {entry['time']} | {entry['subject']} | {entry['teacher']} | {entry['room']} | {entry['note']}")
            
    except Exception as e:
        print(f"Ошибка: {e}")

# URL страницы с расписанием (замените на реальный URL)
url = "https://rpcollege.ru/internal/timetable/list/group/1246"  # Пример для группы 1-Бух-48
parse_schedule(url)