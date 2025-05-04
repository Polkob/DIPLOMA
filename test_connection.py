from sqlalchemy import create_engine, text
from config import Config

def test_connection():
    try:
        # Создаем подключение к базе данных
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        
        # Пробуем выполнить простой запрос
        with engine.connect() as conn:
            # Проверяем версию PostgreSQL
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("Successfully connected to PostgreSQL!")
            print(f"PostgreSQL version: {version}")
            
            # Проверяем существование базы данных movieas
            result = conn.execute(text("SELECT datname FROM pg_database WHERE datname = 'movieas';"))
            db_exists = result.scalar()
            if db_exists:
                print("Database 'movieas' exists!")
            else:
                print("Database 'movieas' does not exist!")
            
            # Проверяем существующие таблицы
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            if tables:
                print("\nExisting tables:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("\nNo tables found in the database.")
            
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {str(e)}")

if __name__ == '__main__':
    test_connection() 