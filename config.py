import os
from dotenv import load_dotenv
import logging
from supabase import create_client, Client

class Config:
    def __init__(self):
        try:
            load_dotenv()
            self.TOKEN = os.getenv('TOKEN')
            self.DB_URL = os.getenv('DB_URL')
            self.DB_KEY = os.getenv('DB_KEY')

            if not all([self.TOKEN, self.DB_URL, self.DB_KEY]):
                raise ValueError("Не все переменные окружения установлены")
            
            # Инициализация клиента
            self.supabase: Client = create_client(self.DB_URL, self.DB_KEY)
            
            # Тест подключения к Supabase (RLS отключён, заголовки не нужны)
            response = self.supabase.table('users').select('user_id').limit(1).execute()
            logging.info(f"Supabase connection test: {response.data}")
            
        except Exception as e:
            logging.critical(f"Ошибка конфигурации: {e}")
            raise

config = Config()

if __name__ == "__main__":
    print("Конфигурация успешно загружена")
    print("Supabase URL:", config.DB_URL)