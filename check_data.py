from sqlalchemy import create_engine, text
from config import Config

def check_data():
    # Создаем подключение к базе данных
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    try:
        with engine.connect() as conn:
            # Проверяем пользователей
            print("\nUsers:")
            result = conn.execute(text("SELECT * FROM users"))
            for row in result:
                print(f"- {row.username} ({row.email})")
            
            # Проверяем фильмы
            print("\nMovies:")
            result = conn.execute(text("""
                SELECT m.*, 
                    string_agg(DISTINCT g.name, ', ') as genres,
                    string_agg(DISTINCT a.name, ', ') as actors,
                    string_agg(DISTINCT d.name, ', ') as directors,
                    string_agg(DISTINCT c.name, ', ') as countries
                FROM movies m
                LEFT JOIN movies_genres mg ON m.id = mg.movie_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                LEFT JOIN movies_actors ma ON m.id = ma.movie_id
                LEFT JOIN actors a ON ma.actor_id = a.id
                LEFT JOIN movies_directors md ON m.id = md.movie_id
                LEFT JOIN directors d ON md.director_id = d.id
                LEFT JOIN movies_countries mc ON m.id = mc.movie_id
                LEFT JOIN countries c ON mc.country_id = c.id
                GROUP BY m.id
            """))
            for row in result:
                print(f"\nMovie: {row.title}")
                print(f"Overview: {row.overview}")
                print(f"Rating: {row.rating}")
                print(f"Genres: {row.genres or 'None'}")
                print(f"Actors: {row.actors or 'None'}")
                print(f"Directors: {row.directors or 'None'}")
                print(f"Countries: {row.countries or 'None'}")
            
            # Проверяем жанры
            print("\nGenres:")
            result = conn.execute(text("SELECT * FROM genres"))
            for row in result:
                print(f"- {row.name}")
            
            # Проверяем актеров
            print("\nActors:")
            result = conn.execute(text("SELECT * FROM actors"))
            for row in result:
                print(f"- {row.name}")
            
            # Проверяем режиссеров
            print("\nDirectors:")
            result = conn.execute(text("SELECT * FROM directors"))
            for row in result:
                print(f"- {row.name}")
            
            # Проверяем страны
            print("\nCountries:")
            result = conn.execute(text("SELECT * FROM countries"))
            for row in result:
                print(f"- {row.name}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_data() 