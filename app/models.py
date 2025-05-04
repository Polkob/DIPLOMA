from sqlalchemy.dialects.postgresql import JSONB
import json
from . import db

# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    favorites = db.relationship('Favorite', backref='user', lazy=True)
    search_history = db.relationship('SearchHistory', backref='user', lazy=True)
    recommendation_logs = db.relationship('RecommendationLog', backref='user', lazy=True)


# Модель фильма
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    poster_url = db.Column(db.String(255))
    release_date = db.Column(db.Date)
    rating = db.Column(db.Float)

    genres = db.relationship('Genre', secondary='movies_genres', back_populates="movies")
    actors = db.relationship('Actor', secondary='movies_actors', back_populates="movies")
    directors = db.relationship('Director', secondary='movies_directors', back_populates="movies")
    countries = db.relationship('Country', secondary='movies_countries', back_populates="movies")

    favorites = db.relationship('Favorite', backref='movie', lazy=True)
    recommendation_logs = db.relationship('RecommendationLog', backref='movie', lazy=True)


# Модель жанра
class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    movies = db.relationship('Movie', secondary='movies_genres', back_populates="genres")


# Модель актера
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', secondary='movies_actors', back_populates="actors")


# Модель режиссёра
class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', secondary='movies_directors', back_populates="directors")


# Модель страны
class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    movies = db.relationship('Movie', secondary='movies_countries', back_populates="countries")


# Таблица связи для фильмов и жанров
class MovieGenre(db.Model):
    __tablename__ = 'movies_genres'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)


# Таблица связи для фильмов и актёров
class MovieActor(db.Model):
    __tablename__ = 'movies_actors'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)


# Таблица связи для фильмов и режиссёров
class MovieDirector(db.Model):
    __tablename__ = 'movies_directors'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), primary_key=True)


# Таблица связи для фильмов и стран
class MovieCountry(db.Model):
    __tablename__ = 'movies_countries'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), primary_key=True)


# Модель избранных фильмов
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# Модель истории поиска
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())


# Модель логов рекомендаций
class RecommendationLog(db.Model):
    __tablename__ = 'recommendation_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    based_on_movies = db.Column(JSONB)
    recommended_ids = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
