from flask import Blueprint, jsonify, request
from app.services.movie_picker import MoviePicker

bp = Blueprint('movie_picker', __name__)

@bp.route('/pick', methods=['GET'])
def pick_movies():
    """Подбор фильмов по параметрам"""
    try:
        # Получаем параметры
        genre = request.args.get('genre')
        year_start = request.args.get('year_start', type=int)
        year_end = request.args.get('year_end', type=int)
        country = request.args.get('country')
        limit = request.args.get('limit', 20, type=int)
        
        # Создаем экземпляр MoviePicker и применяем фильтры
        picker = MoviePicker()
        movies = (picker
                 .by_genre(genre)
                 .by_years(year_start, year_end)
                 .by_country(country)
                 .sort_by_rating()
                 .get_movies(limit))
        
        # Форматируем результат
        return jsonify({
            'movies': [MoviePicker.format_movie(movie) for movie in movies]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/genres', methods=['GET'])
def get_genres():
    """Получение списка доступных жанров"""
    try:
        genres = MoviePicker.get_available_genres()
        return jsonify({'genres': genres}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/countries', methods=['GET'])
def get_countries():
    """Получение списка доступных стран"""
    try:
        countries = MoviePicker.get_available_countries()
        return jsonify({'countries': countries}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 