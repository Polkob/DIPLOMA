import pandas as pd
from app import create_app, db
from app.models import Movie, Genre, Actor, Director, Country
from datetime import datetime
import os

def get_or_create(model, name, cache):
    """Получает существующую запись или создает новую"""
    if name not in cache:
        # Проверяем, существует ли запись в базе
        existing = model.query.filter_by(name=name).first()
        if existing:
            cache[name] = existing
        else:
            # Создаем новую запись
            new_record = model(name=name)
            db.session.add(new_record)
            db.session.flush()
            cache[name] = new_record
    return cache[name]

def get_or_create_movie(tmdb_id, title, overview, poster_url, release_date, rating):
    """Получает существующий фильм или создает новый"""
    existing = Movie.query.filter_by(tmdb_id=tmdb_id).first()
    if existing:
        return existing
    
    movie = Movie(
        tmdb_id=tmdb_id,
        title=title,
        overview=overview,
        poster_url=poster_url,
        release_date=release_date,
        rating=rating
    )
    db.session.add(movie)
    db.session.flush()
    return movie

def load_movies_to_db():
    """Загружает данные о фильмах из CSV в базу данных"""
    app = create_app()
    
    with app.app_context():
        try:
            # Читаем CSV файл
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file = os.path.join(script_dir, 'data', 'movies.csv')
            
            print("Чтение CSV файла...")
            df = pd.read_csv(csv_file)
            
            # Создаем словари для кэширования
            genres_cache = {}
            actors_cache = {}
            directors_cache = {}
            countries_cache = {}
            
            total_movies = len(df)
            print(f"Начинаем загрузку {total_movies} фильмов...")
            
            # Обрабатываем каждый фильм
            for index, row in df.iterrows():
                if index % 100 == 0:
                    print(f"Обработано {index}/{total_movies} фильмов")
                
                # Создаем или получаем фильм
                movie = get_or_create_movie(
                    tmdb_id=int(row['id']),
                    title=row['title'],
                    overview=row['overview'],
                    poster_url=f"https://image.tmdb.org/t/p/w500{row['poster_path']}" if pd.notna(row['poster_path']) else None,
                    release_date=datetime.strptime(row['release_date'], '%Y-%m-%d').date() if pd.notna(row['release_date']) else None,
                    rating=float(row['vote_average']) if pd.notna(row['vote_average']) else None
                )
                
                # Обрабатываем жанры
                if pd.notna(row['genres']):
                    for genre_name in row['genres'].split('|'):
                        genre = get_or_create(Genre, genre_name, genres_cache)
                        if genre not in movie.genres:
                            movie.genres.append(genre)
                
                # Обрабатываем актеров
                if pd.notna(row['top_cast']):
                    for actor_name in row['top_cast'].split('|'):
                        actor = get_or_create(Actor, actor_name, actors_cache)
                        if actor not in movie.actors:
                            movie.actors.append(actor)
                
                # Обрабатываем режиссеров
                if pd.notna(row['directors']):
                    for director_name in row['directors'].split('|'):
                        director = get_or_create(Director, director_name, directors_cache)
                        if director not in movie.directors:
                            movie.directors.append(director)
                
                # Обрабатываем страны
                if pd.notna(row['production_countries']):
                    for country_name in row['production_countries'].split('|'):
                        country = get_or_create(Country, country_name, countries_cache)
                        if country not in movie.countries:
                            movie.countries.append(country)
                
                # Сохраняем каждые 100 фильмов
                if (index + 1) % 100 == 0:
                    db.session.commit()
                    print(f"Сохранено {index + 1} фильмов")
            
            # Сохраняем оставшиеся изменения
            db.session.commit()
            print("Загрузка завершена!")
            
            # Выводим статистику
            print("\nСтатистика загрузки:")
            print(f"Всего фильмов: {Movie.query.count()}")
            print(f"Всего жанров: {Genre.query.count()}")
            print(f"Всего актеров: {Actor.query.count()}")
            print(f"Всего режиссеров: {Director.query.count()}")
            print(f"Всего стран: {Country.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Произошла ошибка: {str(e)}")
            raise

if __name__ == '__main__':
    load_movies_to_db() 