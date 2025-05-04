from sqlalchemy import create_engine, text
from config import Config

def create_tables():
    # Создаем подключение к базе данных
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    # SQL для создания таблиц
    sql = """
    -- Создаем таблицу пользователей
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Создаем таблицу фильмов
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        tmdb_id INTEGER UNIQUE NOT NULL,
        title VARCHAR(255) NOT NULL,
        overview TEXT,
        poster_url VARCHAR(255),
        release_date DATE,
        rating FLOAT
    );

    -- Создаем таблицу жанров
    CREATE TABLE IF NOT EXISTS genres (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );

    -- Создаем таблицу актеров
    CREATE TABLE IF NOT EXISTS actors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    );

    -- Создаем таблицу режиссеров
    CREATE TABLE IF NOT EXISTS directors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
    );

    -- Создаем таблицу стран
    CREATE TABLE IF NOT EXISTS countries (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );

    -- Создаем связующие таблицы
    CREATE TABLE IF NOT EXISTS movies_genres (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, genre_id)
    );

    CREATE TABLE IF NOT EXISTS movies_actors (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        actor_id INTEGER REFERENCES actors(id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, actor_id)
    );

    CREATE TABLE IF NOT EXISTS movies_directors (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        director_id INTEGER REFERENCES directors(id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, director_id)
    );

    CREATE TABLE IF NOT EXISTS movies_countries (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, country_id)
    );

    -- Создаем таблицу избранных фильмов
    CREATE TABLE IF NOT EXISTS favorites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Создаем таблицу истории поиска
    CREATE TABLE IF NOT EXISTS search_history (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        query TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Создаем таблицу логов рекомендаций
    CREATE TABLE IF NOT EXISTS recommendation_logs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
        based_on_movies JSONB,
        recommended_ids JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with engine.connect() as conn:
            # Удаляем все существующие таблицы
            conn.execute(text("""
                DROP SCHEMA public CASCADE;
                CREATE SCHEMA public;
            """))
            conn.commit()
            print("Existing tables dropped successfully")
            
            # Создаем таблицы
            conn.execute(text(sql))
            conn.commit()
            print("New tables created successfully")
            
            # Проверяем созданные таблицы
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
    create_tables() 