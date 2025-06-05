import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ScheduleParser:
    """Парсер расписания с сайта колледжа"""
    
    def __init__(self):
        self.base_url = "https://rpcollege.ru/internal/timetable/list/group/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    async def parse_schedule(self, schedule_id: int) -> Dict[str, List[Dict]]:
        """Основной метод парсинга, возвращает расписание на 14 дней с текущей даты"""
        try:
            url = f"{self.base_url}{schedule_id}"
            logger.info(f"Отправка запроса на: {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    logger.info(f"Статус ответа: {response.status}")
                    response.raise_for_status()
                    text = await response.text()
            
            soup = BeautifulSoup(text, 'html.parser')
            table = soup.find('table', {'class': 'table table-main table-bordered'})
            
            if not table:
                logger.error("Таблица расписания не найдена")
                return {}

            schedule = {}
            current_day = ""
            end_date = datetime.now() + timedelta(days=13)  # 14 дней, включая сегодня
            
            for row in table.find_all('tr'):
                if day_header := row.find('th', {'class': 'td-left'}):
                    current_day = day_header.get_text(strip=True)
                    # Преобразуем строку даты в объект datetime
                    try:
                        day_date = datetime.strptime(current_day.split(' – ')[0], '%d.%m.%Y')
                        if day_date < datetime.now() or day_date > end_date:
                            current_day = None  # Пропускаем дни вне диапазона
                    except ValueError:
                        logger.warning(f"Некорректный формат даты: {current_day}")
                        current_day = None
                    if current_day:
                        schedule[current_day] = []
                    continue
                
                if current_day and (cols := row.find_all('td')):  # Проверяем, что cols — список тегов
                    if len(cols) >= 5:
                        # Проверяем, что каждый элемент cols — тег, а не строка
                        lesson = {
                            'time': cols[0].get_text(strip=True) if hasattr(cols[0], 'get_text') else cols[0],
                            'subject': cols[2].get_text(strip=True) if hasattr(cols[2], 'get_text') else cols[2],
                            'teacher': cols[3].get_text(strip=True) if hasattr(cols[3], 'get_text') else cols[3],
                            'room': cols[4].get_text(strip=True) if hasattr(cols[4], 'get_text') else cols[4]
                        }
                        logger.debug(f"Обнаружен урок: {lesson}")
                        schedule[current_day].append(lesson)

            logger.info(f"Сформировано расписание на 14 дней: {schedule}")
            return schedule

        except aiohttp.ClientError as e:
            logger.error(f"Ошибка запроса: {e}", exc_info=True)
            return {}
        except Exception as e:
            logger.error(f"Ошибка парсинга: {e}", exc_info=True)
            return {}

# Глобальный экземпляр
parser = ScheduleParser()
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from typing import Dict, List

# def parse_schedule(url: str, week_type: str = "current") -> Dict[str, List[Dict]]:
#     """
#     Парсит расписание и возвращает данные только для указанной недели.
    
#     Параметры:
#         url: URL страницы с расписанием
#         week_type: "current" - текущая неделя, "next" - следующая неделя
    
#     Возвращает:
#         Словарь с расписанием для запрошенной недели в формате:
#         {
#             "Понедельник": [
#                 {"time": "09:00", "subject": "Математика", "room": "304"},
#                 ...
#             ],
#             ...
#         }
#     """
#     try:
#         # Загружаем страницу
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.text, 'html.parser')
#         table = soup.find('table', {'class': 'table table-main table-bordered'})
        
#         if not table:
#             print("Таблица расписания не найдена!")
#             return {}

#         # Получаем все дни из расписания
#         all_days = []
#         current_day = ""
        
#         for row in table.find_all('tr'):
#             date_header = row.find('th', {'class': 'td-left'})
#             if date_header:
#                 current_day = date_header.get_text(strip=True)
#                 all_days.append(current_day)
#                 continue

#         if not all_days:
#             return {}

#         # Определяем дни для текущей и следующей недели
#         middle_index = len(all_days) // 2
#         current_week_days = all_days[:middle_index]
#         next_week_days = all_days[middle_index:]

#         # Парсим данные и фильтруем по неделям
#         schedule = {}
#         current_day = ""
        
#         for row in table.find_all('tr'):
#             date_header = row.find('th', {'class': 'td-left'})
#             if date_header:
#                 current_day = date_header.get_text(strip=True)
#                 if (week_type == "current" and current_day in current_week_days) or \
#                    (week_type == "next" and current_day in next_week_days):
#                     schedule[current_day] = []
#                 continue
            
#             cols = row.find_all('td')
#             if len(cols) >= 6 and current_day:
#                 if (week_type == "current" and current_day in current_week_days) or \
#                    (week_type == "next" and current_day in next_week_days):
#                     schedule[current_day].append({
#                         'time': cols[0].get_text(strip=True),
#                         'subject': cols[2].get_text(strip=True),
#                         'room': cols[4].get_text(strip=True),
#                         'teacher': cols[3].get_text(strip=True)
#                     })

#         return schedule

#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе: {e}")
#         return {}
#     except Exception as e:
#         print(f"Неожиданная ошибка: {e}")
#         return {}

# # Тестирование
# if __name__ == "__main__":
#     test_url = "https://rpcollege.ru/internal/timetable/list/group/1246"
    
#     print("=== Текущая неделя ===")
#     current_week = parse_schedule(test_url, "current")
#     for day, lessons in current_week.items():
#         print(f"\n{day}:")
#         for lesson in lessons:
#             print(f"  {lesson['time']} - {lesson['subject']} ({lesson['room']})")
    
#     print("\n=== Следующая неделя ===")
#     next_week = parse_schedule(test_url, "next")
#     for day, lessons in next_week.items():
#         print(f"\n{day}:")
#         for lesson in lessons:
#             print(f"  {lesson['time']} - {lesson['subject']} ({lesson['room']})")