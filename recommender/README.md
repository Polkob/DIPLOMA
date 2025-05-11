# Система рекомендаций фильмов

Система рекомендаций фильмов на основе контентной фильтрации. Система анализирует различные аспекты фильмов (жанры, актеров, режиссеров, описание) и рекомендует похожие фильмы.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Поместите файлы с данными в директорию `data`:
- `tmdb_5000_credits.csv`
- `tmdb_5000_movies.csv`

## Использование

### Базовое использование

```python
from movie_recommender import MovieRecommender

# Инициализация рекомендательной системы
recommender = MovieRecommender(data_path='data')

# Загрузка или обучение модели
try:
    recommender.load_model()
except FileNotFoundError:
    recommender.load_data(
        credits_path='data/tmdb_5000_credits.csv',
        movies_path='data/tmdb_5000_movies.csv'
    )
    recommender.create_similarity_matrix()
    recommender.save_model()

# Получение рекомендаций
recommendations = recommender.get_recommendations(
    movie_titles=["Avatar", "The Dark Knight"],  # от 1 до 3 фильмов
    n_recommendations=5  # количество рекомендаций
)
```

### Интеграция с API

Для интеграции с API вы можете использовать класс `MovieRecommender` как сервис:

```python
from flask import Flask, request, jsonify
from movie_recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender(data_path='data')
recommender.load_model()

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie_titles = data.get('movies', [])
    n_recommendations = data.get('n_recommendations', 10)
    
    try:
        recommendations = recommender.get_recommendations(
            movie_titles=movie_titles,
            n_recommendations=n_recommendations
        )
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

## Особенности

- Поддерживает рекомендации на основе 1-3 фильмов
- Учитывает различные аспекты фильмов:
  - Жанры
  - Актерский состав
  - Режиссеры
  - Описание фильма
- Использует TF-IDF векторизацию и косинусное сходство
- Сохраняет обученную модель для быстрой загрузки 