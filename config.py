import os
from dotenv import load_dotenv
import logging
from supabase import create_client

class Config:
    def __init__(self):
        try:
            load_dotenv()
            self.TOKEN = os.getenv('TOKEN')
            self.DB_URL = os.getenv('DB_URL')
            self.DB_KEY = os.getenv('DB_KEY')
            
            if not all([self.TOKEN, self.DB_URL, self.DB_KEY]):
                raise ValueError("Не все переменные окружения установлены")
                
            self.supabase = create_client(self.DB_URL, self.DB_KEY)
            
        except Exception as e:
            logging.critical(f"Ошибка конфигурации: {e}")
            raise

# Создаем экземпляр конфига
config = Config()

if __name__ == "__main__":
    # Тестовый вывод (только при прямом запуске config.py)
    print("Конфигурация успешно загружена")
    print("Supabase URL:", config.DB_URL)