from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Movie, Favorite
from app import db

bp = Blueprint('favorites', __name__)

@bp.route('/', methods=['GET'])
@login_required
def get_favorites():
    """Получение списка избранных фильмов пользователя"""
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    movies = [fav.movie for fav in favorites]
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'genres': [genre.name for genre in movie.genres],
        'actors': [actor.name for actor in movie.actors],
        'countries': [country.name for country in movie.countries]
    } for movie in movies]), 200

@bp.route('/<int:movie_id>', methods=['POST'])
@login_required
def add_to_favorites(movie_id):
    """Добавление фильма в избранное"""
    movie = Movie.query.get_or_404(movie_id)
    
    # Проверяем, не добавлен ли фильм уже в избранное
    if Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first():
        return jsonify({'error': 'Movie already in favorites'}), 400
    
    favorite = Favorite(user_id=current_user.id, movie_id=movie_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Movie added to favorites'}), 201

@bp.route('/<int:movie_id>', methods=['DELETE'])
@login_required
def remove_from_favorites(movie_id):
    """Удаление фильма из избранного"""
    favorite = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Movie removed from favorites'}), 200
