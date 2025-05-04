from sqlalchemy import create_engine, text
from config import Config

def check_tables():
    # Создаем подключение к базе данных
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    try:
        with engine.connect() as conn:
            # Получаем список таблиц
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            tables = result.fetchall()
            
            print("Database structure:")
            print("===================")
            
            # Для каждой таблицы получаем структуру
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                print("-" * (len(table_name) + 7))
                
                # Получаем информацию о колонках
                result = conn.execute(text(f"""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """))
                columns = result.fetchall()
                
                for column in columns:
                    nullable = "NULL" if column[2] == "YES" else "NOT NULL"
                    default = f"DEFAULT {column[3]}" if column[3] else ""
                    print(f"- {column[0]}: {column[1]} {nullable} {default}".strip())
                
                # Получаем информацию о внешних ключах
                result = conn.execute(text(f"""
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                          AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                          AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_name = '{table_name}';
                """))
                foreign_keys = result.fetchall()
                
                if foreign_keys:
                    print("\nForeign Keys:")
                    for fk in foreign_keys:
                        print(f"- {fk[0]} -> {fk[1]}({fk[2]})")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_tables() 