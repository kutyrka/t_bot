import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Config:
    def __init__(self):
        try:
            load_dotenv()
            self.TOKEN = self._get_env_var('TOKEN')
            self.ADMIN_CHAT_ID = self._get_env_var('ADMIN_CHAT_ID')
            self.DB_URL = self._get_env_var('DB_URL')
        except ValueError as e:
            logging.critical(f"Ошибка конфигурации: {e}")
            raise

    def _get_env_var(self, var_name):
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Переменная окружения {var_name} не установлена")
        return value

try:
    config = Config()
except ValueError as e:
    print(f"Не удалось загрузить конфигурацию: {e}")
    exit(1)
