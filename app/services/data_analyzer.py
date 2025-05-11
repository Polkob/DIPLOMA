from app import db
from app.models import User, Movie, Favorite, SearchHistory, RecommendationLog
from sqlalchemy import func, desc
from collections import Counter
import numpy as np

class DataAnalyzer:
    def __init__(self):
        self.db = db

    def analyze_user_preferences(self, user_id):
        """Анализ предпочтений пользователя"""
        try:
            # Получаем избранные фильмы пользователя
            favorites = Favorite.query.filter_by(user_id=user_id).all()
            favorite_movies = [fav.movie for fav in favorites]

            # Анализируем жанры
            genres = []
            for movie in favorite_movies:
                genres.extend([genre.name for genre in movie.genres])
            genre_preferences = Counter(genres).most_common()

            # Анализируем актеров
            actors = []
            for movie in favorite_movies:
                actors.extend([actor.name for actor in movie.actors])
            actor_preferences = Counter(actors).most_common(10)

            # Анализируем страны
            countries = []
            for movie in favorite_movies:
                countries.extend([country.name for country in movie.countries])
            country_preferences = Counter(countries).most_common()

            # Анализируем годы выпуска
            years = [movie.release_date.year for movie in favorite_movies if movie.release_date]
            year_preferences = Counter(years).most_common()

            return {
                'genre_preferences': genre_preferences,
                'actor_preferences': actor_preferences,
                'country_preferences': country_preferences,
                'year_preferences': year_preferences
            }
        except Exception as e:
            raise Exception(f"Error analyzing user preferences: {str(e)}")

    def analyze_movie_patterns(self):
        """Анализ паттернов в фильмах"""
        try:
            # Анализ популярных жанров
            genre_counts = db.session.query(
                Genre.name, func.count(Movie.id)
            ).join(Movie.genres).group_by(Genre.name).all()

            # Анализ популярных актеров
            actor_counts = db.session.query(
                Actor.name, func.count(Movie.id)
            ).join(Movie.actors).group_by(Actor.name).all()

            # Анализ популярных стран
            country_counts = db.session.query(
                Country.name, func.count(Movie.id)
            ).join(Movie.countries).group_by(Country.name).all()

            # Анализ распределения рейтингов
            rating_stats = db.session.query(
                func.avg(Movie.rating),
                func.min(Movie.rating),
                func.max(Movie.rating)
            ).first()

            return {
                'genre_patterns': genre_counts,
                'actor_patterns': actor_counts,
                'country_patterns': country_counts,
                'rating_statistics': {
                    'average': rating_stats[0],
                    'minimum': rating_stats[1],
                    'maximum': rating_stats[2]
                }
            }
        except Exception as e:
            raise Exception(f"Error analyzing movie patterns: {str(e)}")

    def generate_insights(self, user_id=None):
        """Генерация инсайтов на основе анализа данных"""
        try:
            insights = {
                'global_patterns': self.analyze_movie_patterns()
            }

            if user_id:
                insights['user_preferences'] = self.analyze_user_preferences(user_id)

            # Генерация рекомендаций на основе инсайтов
            if user_id:
                user_prefs = insights['user_preferences']
                global_patterns = insights['global_patterns']

                # Находим пересечение предпочтений пользователя с глобальными паттернами
                recommended_genres = [
                    genre for genre, _ in user_prefs['genre_preferences']
                    if genre in [g[0] for g in global_patterns['genre_patterns']]
                ]

                recommended_actors = [
                    actor for actor, _ in user_prefs['actor_preferences']
                    if actor in [a[0] for a in global_patterns['actor_patterns']]
                ]

                insights['recommendations'] = {
                    'genres': recommended_genres,
                    'actors': recommended_actors
                }

            return insights
        except Exception as e:
            raise Exception(f"Error generating insights: {str(e)}")

    def get_trending_movies(self, limit=10):
        """Получение трендовых фильмов на основе анализа данных"""
        try:
            # Анализируем популярность фильмов на основе избранного и просмотров
            trending = db.session.query(
                Movie,
                func.count(Favorite.id).label('favorite_count')
            ).outerjoin(Favorite).group_by(Movie.id).order_by(
                desc('favorite_count')
            ).limit(limit).all()

            return [movie for movie, _ in trending]
        except Exception as e:
            raise Exception(f"Error getting trending movies: {str(e)}") 