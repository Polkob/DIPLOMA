from sqlalchemy import create_engine, MetaData, text
from config import Config
from app import create_app, db
from app.models import User, Movie, Genre, Actor, Director, Country, MovieGenre, MovieActor, MovieDirector, MovieCountry, Favorite, SearchHistory, RecommendationLog

def init_db():
    # Создаем приложение
    app = create_app()
    
    with app.app_context():
        try:
            # Удаляем все существующие таблицы
            db.drop_all()
            print("Existing tables dropped successfully")
            
            # Создаем все таблицы заново
            db.create_all()
            print("New tables created successfully")
            
            # Проверяем созданные таблицы
            engine = db.engine
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """))
                tables = result.fetchall()
                if tables:
                    print("\nCreated tables:")
                    for table in tables:
                        print(f"- {table[0]}")
                else:
                    print("\nNo tables found in the database.")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    init_db() 