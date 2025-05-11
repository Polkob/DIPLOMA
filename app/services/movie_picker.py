from app import db
from app.models import Movie, Genre, Country
from sqlalchemy import and_, desc
from datetime import datetime

class MoviePicker:
    def __init__(self):
        self.query = Movie.query

    def by_genre(self, genre_name):
        """Фильтрация по жанру"""
        if genre_name:
            self.query = self.query.join(Movie.genres).filter(Genre.name == genre_name)
        return self

    def by_years(self, start_year, end_year):
        """Фильтрация по периоду лет"""
        if start_year:
            self.query = self.query.filter(Movie.release_date >= f"{start_year}-01-01")
        if end_year:
            self.query = self.query.filter(Movie.release_date <= f"{end_year}-12-31")
        return self

    def by_country(self, country_name):
        """Фильтрация по стране производства"""
        if country_name:
            self.query = self.query.join(Movie.countries).filter(Country.name == country_name)
        return self

    def sort_by_rating(self):
        """Сортировка по рейтингу"""
        self.query = self.query.order_by(desc(Movie.rating))
        return self

    def get_movies(self, limit=20):
        """Получение отфильтрованных фильмов"""
        return self.query.limit(limit).all()

    @staticmethod
    def get_available_genres():
        """Получение списка доступных жанров"""
        return [genre.name for genre in Genre.query.all()]

    @staticmethod
    def get_available_countries():
        """Получение списка доступных стран"""
        return [country.name for country in Country.query.all()]

    @staticmethod
    def format_movie(movie):
        """Форматирование информации о фильме"""
        return {
            'id': movie.id,
            'title': movie.title,
            'original_title': movie.original_title,
            'overview': movie.overview,
            'poster_url': movie.poster_url,
            'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
            'rating': movie.rating,
            'genres': [genre.name for genre in movie.genres],
            'actors': [actor.name for actor in movie.actors[:5]],  # Топ-5 актеров
            'countries': [country.name for country in movie.countries]
        } 