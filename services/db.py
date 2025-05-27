import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('DB_URL'), os.getenv('DB_KEY'))

try:
    # Запрос с явным указанием столбцов
    response = supabase.table('users').select("id, username, email").limit(2).execute()
    
    print("=== Тестовые пользователи ===")
    for user in response.data:
        print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")
    
    print(f"\nУспешно! Получено записей: {len(response.data)}")
    
except Exception as e:
    print(f"\n❌ Ошибка: {str(e)}")
    print("\nЕсли ошибка сохраняется:")
    print("1. В Supabase: Settings -> Database")
    print("2. Включите 'Enable Row Level Security (RLS)'")
    print("3. Создайте политику для таблицы users")