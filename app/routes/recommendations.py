from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Movie, RecommendationLog
from recommender.hybrid_recommender import HybridRecommender
from recommender.movie_recommender import MovieRecommender
from flask_login import login_required, current_user
import os

bp = Blueprint('recommendations', __name__)
recommender = HybridRecommender()

# Получаем абсолютный путь к директории recommender/data
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(current_dir, 'recommender', 'data')

# Проверяем существование директории и создаем ее при необходимости
if not os.path.exists(data_path):
    os.makedirs(data_path)

movie_recommender = MovieRecommender(data_path=data_path)

def init_app(app):
    recommender.init_app(app)
    try:
        movie_recommender.load_model()
        print(f"Модель успешно загружена из {data_path}")
    except FileNotFoundError:
        print(f"Создание новой модели в {data_path}")
        # Если модель не найдена, создаем новую
        movie_recommender.load_data(
            credits_path=os.path.join(data_path, 'credits.csv'),
            movies_path=os.path.join(data_path, 'movies.csv')
        )
        movie_recommender.create_similarity_matrix()
        movie_recommender.save_model()
        print("Модель успешно создана и сохранена")

@bp.route('/build-matrices', methods=['POST'])
def build_matrices():
    """Построение матриц схожести"""
    try:
        recommender.build_content_similarity_matrix()
        return jsonify({'message': 'Matrices built successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """Получение рекомендаций для пользователя"""
    try:
        movie_id = request.args.get('movie_id', type=int)
        n_recommendations = request.args.get('n', 10, type=int)
        
        recommendations = recommender.get_hybrid_recommendations(
            user_id=current_user.id,
            movie_id=movie_id,
            n_recommendations=n_recommendations
        )
        
        return jsonify({
            'recommendations': [{
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_url': movie.poster_url,
                'rating': movie.rating,
                'genres': [genre.name for genre in movie.genres],
                'actors': [actor.name for actor in movie.actors[:5]],  # Топ-5 актеров
                'countries': [country.name for country in movie.countries]
            } for movie in recommendations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/similar-movies/<int:movie_id>', methods=['GET'])
def get_similar_movies(movie_id):
    """Получение похожих фильмов"""
    try:
        # Проверяем существование фильма
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404

        # Получаем рекомендации
        n_recommendations = request.args.get('n', default=10, type=int)
        similar_movie_ids = recommender.get_content_based_recommendations(movie_id, n_recommendations)
        
        # Получаем информацию о фильмах
        similar_movies = Movie.query.filter(Movie.id.in_(similar_movie_ids)).all()
        
        return jsonify({
            'movie': {
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_url': movie.poster_url
            },
            'similar_movies': [{
                'id': m.id,
                'title': m.title,
                'overview': m.overview,
                'poster_url': m.poster_url
            } for m in similar_movies]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/recommendations/by-movies', methods=['POST'])
def get_recommendations_by_movies():
    """Получение рекомендаций на основе списка фильмов"""
    try:
        data = request.get_json()
        if not data or 'movies' not in data:
            return jsonify({'error': 'No movies provided'}), 400
            
        movies = data['movies']
        if not isinstance(movies, list) or not 1 <= len(movies) <= 3:
            return jsonify({'error': 'Must provide 1-3 movies'}), 400
            
        n_recommendations = data.get('n', 10)
        
        # Получаем рекомендации
        recommendations = movie_recommender.get_recommendations(movies, n_recommendations)
        
        # Получаем полную информацию о фильмах из базы данных
        recommended_movies = []
        for title, original_title in recommendations:
            movie = Movie.query.filter(
                (Movie.title == title) | (Movie.original_title == original_title)
            ).first()
            
            if movie:
                recommended_movies.append({
                    'id': movie.id,
                    'title': movie.title,
                    'original_title': movie.original_title,
                    'overview': movie.overview,
                    'poster_url': movie.poster_url,
                    'rating': movie.rating,
                    'genres': [genre.name for genre in movie.genres],
                    'actors': [actor.name for actor in movie.actors[:5]],  # Топ-5 актеров
                    'countries': [country.name for country in movie.countries]
                })
        
        return jsonify({
            'recommendations': recommended_movies
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/by-movies', methods=['GET'])
def get_recommendations_by_movies_get():
    """Получение рекомендаций на основе списка ID фильмов (GET метод)"""
    try:
        # Получаем список ID фильмов из query параметров
        movies_str = request.args.get('movies', '')
        if not movies_str:
            return jsonify({'error': 'No movies provided'}), 400
            
        # Разбиваем строку с ID фильмов по запятой и конвертируем в числа
        try:
            movie_ids = [int(m.strip()) for m in movies_str.split(',')]
        except ValueError:
            return jsonify({'error': 'Invalid movie IDs provided'}), 400
            
        if not 1 <= len(movie_ids) <= 3:
            return jsonify({'error': 'Must provide 1-3 movies'}), 400
            
        n_recommendations = request.args.get('n', 10, type=int)
        
        # Получаем рекомендации
        recommended_ids = movie_recommender.get_recommendations(movie_ids, n_recommendations)
        
        # Получаем полную информацию о фильмах из базы данных
        recommended_movies = []
        for movie_id in recommended_ids:
            movie = Movie.query.get(movie_id)
            if movie:
                recommended_movies.append({
                    'id': movie.id,
                    'title': movie.title,
                    'original_title': movie.original_title,
                    'overview': movie.overview,
                    'poster_url': movie.poster_url,
                    'rating': movie.rating,
                    'genres': [genre.name for genre in movie.genres],
                    'actors': [actor.name for actor in movie.actors[:5]],  # Топ-5 актеров
                    'countries': [country.name for country in movie.countries]
                })
        
        return jsonify({
            'recommendations': recommended_movies
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 