from flask import Flask, request, jsonify
from movie_recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender(data_path='data')

# Загрузка модели при старте
try:
    recommender.load_model()
    print("Модель успешно загружена")
except FileNotFoundError:
    print("Модель не найдена. Пожалуйста, сначала запустите example.py для обучения модели")
    exit(1)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """
    Получение рекомендаций фильмов
    Пример запроса:
    {
        "movies": ["Avatar", "The Dark Knight"],
        "n_recommendations": 5
    }
    """
    data = request.get_json()
    movie_titles = data.get('movies', [])
    n_recommendations = data.get('n_recommendations', 10)
    
    try:
        recommendations = recommender.get_recommendations(
            movie_titles=movie_titles,
            n_recommendations=n_recommendations
        )
        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/movies', methods=['GET'])
def get_available_movies():
    """Получение списка доступных фильмов"""
    try:
        movies = recommender.movies['title'].tolist()
        return jsonify({
            'status': 'success',
            'movies': movies
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 