from flask import Blueprint, jsonify, request
from app.models import Movie, Genre, Actor, Country
from app import db

bp = Blueprint('movies', __name__)

@bp.route('/', methods=['GET'])
def get_movies():
    """Получение списка всех фильмов"""
    movies = Movie.query.all()
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'genres': [genre.name for genre in movie.genres],
        'actors': [actor.name for actor in movie.actors],
        'countries': [country.name for country in movie.countries]
    } for movie in movies]), 200

@bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Получение информации о конкретном фильме"""
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'genres': [genre.name for genre in movie.genres],
        'actors': [actor.name for actor in movie.actors],
        'countries': [country.name for country in movie.countries]
    }), 200

@bp.route('/', methods=['POST'])
def create_movie():
    """Создание нового фильма"""
    data = request.get_json()

    # Создаем или получаем жанры
    genres = []
    for genre_name in data.get('genres', []):
        genre = Genre.query.filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.session.add(genre)
        genres.append(genre)

    # Создаем или получаем актеров
    actors = []
    for actor_name in data.get('actors', []):
        actor = Actor.query.filter_by(name=actor_name).first()
        if not actor:
            actor = Actor(name=actor_name)
            db.session.add(actor)
        actors.append(actor)

    # Создаем или получаем страны
    countries = []
    for country_name in data.get('countries', []):
        country = Country.query.filter_by(name=country_name).first()
        if not country:
            country = Country(name=country_name)
            db.session.add(country)
        countries.append(country)

    # Создаем фильм
    movie = Movie(
        title=data['title'],
        overview=data.get('overview', ''),
        poster_path=data.get('poster_path', '')
    )
    movie.genres = genres
    movie.actors = actors
    movie.countries = countries

    db.session.add(movie)
    db.session.commit()

    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'genres': [genre.name for genre in movie.genres],
        'actors': [actor.name for actor in movie.actors],
        'countries': [country.name for country in movie.countries]
    }), 201
