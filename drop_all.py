from sqlalchemy import create_engine, text
from config import Config

def drop_all_tables():
    # Создаем подключение к базе данных
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    # SQL для удаления всех таблиц
    sql = """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
        print("All tables have been dropped.")

if __name__ == '__main__':
    drop_all_tables() 