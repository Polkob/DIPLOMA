import json
import pandas as pd
import os
from typing import Dict, Any

def flatten_movie_data(movie: Dict[str, Any]) -> Dict[str, Any]:
    """Преобразует вложенные данные фильма в плоскую структуру"""
    flat_data = {
        'id': movie.get('id'),
        'title': movie.get('title'),
        'original_title': movie.get('original_title'),
        'overview': movie.get('overview'),
        'release_date': movie.get('release_date'),
        'runtime': movie.get('runtime'),
        'vote_average': movie.get('vote_average'),
        'vote_count': movie.get('vote_count'),
        'popularity': movie.get('popularity'),
        'poster_path': movie.get('poster_path'),
        'backdrop_path': movie.get('backdrop_path'),
        'budget': movie.get('budget'),
        'revenue': movie.get('revenue'),
        'status': movie.get('status'),
        'tagline': movie.get('tagline'),
        'imdb_id': movie.get('external_ids', {}).get('imdb_id'),
        'homepage': movie.get('homepage'),
        'adult': movie.get('adult'),
    }
    
    # Добавляем жанры
    genres = movie.get('genres', [])
    flat_data['genres'] = '|'.join([genre['name'] for genre in genres])
    
    # Добавляем страны производства
    production_countries = movie.get('production_countries', [])
    flat_data['production_countries'] = '|'.join([country['name'] for country in production_countries])
    
    # Добавляем компании
    production_companies = movie.get('production_companies', [])
    flat_data['production_companies'] = '|'.join([company['name'] for company in production_companies])
    
    # Добавляем языки
    spoken_languages = movie.get('spoken_languages', [])
    flat_data['spoken_languages'] = '|'.join([lang['name'] for lang in spoken_languages])
    
    # Добавляем ключевые слова
    keywords = movie.get('keywords', {}).get('keywords', [])
    flat_data['keywords'] = '|'.join([keyword['name'] for keyword in keywords])
    
    # Добавляем актеров (топ-5)
    cast = movie.get('credits', {}).get('cast', [])[:5]
    flat_data['top_cast'] = '|'.join([actor['name'] for actor in cast])
    
    # Добавляем режиссеров
    directors = [crew['name'] for crew in movie.get('credits', {}).get('crew', []) 
                if crew.get('job') == 'Director']
    flat_data['directors'] = '|'.join(directors)
    
    return flat_data

def convert_json_to_csv():
    """Конвертирует JSON файл с фильмами в CSV"""
    # Пути к файлам
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'data', 'movies_data.json')
    csv_file = os.path.join(script_dir, 'data', 'movies.csv')
    
    print("Чтение JSON файла...")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)
    except Exception as e:
        print(f"Ошибка при чтении JSON файла: {str(e)}")
        return
    
    print(f"Обработка {len(movies_data)} фильмов...")
    
    # Преобразуем данные в плоскую структуру
    flat_movies = [flatten_movie_data(movie) for movie in movies_data]
    
    # Создаем DataFrame
    df = pd.DataFrame(flat_movies)
    
    # Сохраняем в CSV
    print("Сохранение в CSV...")
    df.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"Готово! Данные сохранены в {csv_file}")
    print(f"Количество фильмов: {len(df)}")
    print("\nСтолбцы в CSV файле:")
    for col in df.columns:
        print(f"- {col}")

if __name__ == "__main__":
    convert_json_to_csv() 