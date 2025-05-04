from flask_restful import Resource
from flask import request
from app import db
from app.models import User, Movie, Favorite, Genre, Actor, Director, Country, MovieGenre, MovieActor, MovieDirector, MovieCountry

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        result = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return {'users': result}, 200

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], password_hash=data['password_hash'], email=data.get('email'))
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created', 'user': {'id': new_user.id, 'username': new_user.username}}, 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email}, 200
        return {'message': 'User not found'}, 404

class MovieListResource(Resource):
    def get(self):
        movies = Movie.query.all()
        result = [{'id': movie.id, 'title': movie.title, 'rating': movie.rating} for movie in movies]
        return {'movies': result}, 200

    def post(self):
        data = request.get_json()
        new_movie = Movie(
            tmdb_id=data['tmdb_id'],
            title=data['title'],
            overview=data.get('overview'),
            poster_url=data.get('poster_url'),
            release_date=data.get('release_date'),
            rating=data.get('rating')
        )
        db.session.add(new_movie)
        db.session.commit()
        return {'message': 'Movie created', 'movie': {'id': new_movie.id, 'title': new_movie.title}}, 201


class MovieResource(Resource):
    def get(self, movie_id):
        # Получаем фильм по ID
        movie = Movie.query.get_or_404(movie_id)

        # Загружаем все жанры фильма
        genres = [genre.name for genre in movie.genres]

        # Загружаем всех актеров фильма
        actors = [actor.name for actor in movie.actors]

        # Загружаем всех режиссеров фильма
        directors = [director.name for director in movie.directors]

        # Загружаем все страны производства фильма
        countries = [country.name for country in movie.countries]

        # Формируем полный ответ
        movie_data = {
            'id': movie.id,
            'tmdb_id': movie.tmdb_id,
            'title': movie.title,
            'overview': movie.overview,
            'poster_url': movie.poster_url,
            'release_date': movie.release_date,
            'rating': movie.rating,
            'genres': genres,
            'actors': actors,
            'directors': directors,
            'countries': countries
        }

        return movie_data, 200

class FavoriteListResource(Resource):
    def get(self, user_id):
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        result = [{'movie_id': favorite.movie_id, 'added_at': favorite.added_at} for favorite in favorites]
        return {'favorites': result}, 200

    def post(self, user_id):
        data = request.get_json()
        favorite_movie = Favorite(user_id=user_id, movie_id=data['movie_id'])
        db.session.add(favorite_movie)
        db.session.commit()
        return {'message': 'Movie added to favorites'}, 201

class FavoriteListResource(Resource):
    def get(self, user_id):
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        result = [{'movie_id': favorite.movie_id, 'added_at': favorite.added_at} for favorite in favorites]
        return {'favorites': result}, 200

    def post(self, user_id):
        data = request.get_json()
        favorite_movie = Favorite(user_id=user_id, movie_id=data['movie_id'])
        db.session.add(favorite_movie)
        db.session.commit()
        return {'message': 'Movie added to favorites'}, 201

class FavoritesResource(Resource):
    def get(self, user_id):
        # Получаем все избранные фильмы пользователя
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        movie_ids = [fav.movie_id for fav in favorites]

        # Загружаем информацию о каждом фильме
        movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
        movies_data = [{
            'id': movie.id,
            'title': movie.title,
            'overview': movie.overview,
            'poster_url': movie.poster_url
        } for movie in movies]

        return movies_data, 200

    def post(self, user_id):
        # Добавляем фильм в избранное
        movie_id = request.json.get('movie_id')

        if not movie_id:
            return {'message': 'Movie ID is required'}, 400

        # Проверяем, не добавлен ли уже фильм
        existing_fav = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_fav:
            return {'message': 'Movie already in favorites'}, 400

        # Добавляем в таблицу favorites
        favorite = Favorite(user_id=user_id, movie_id=movie_id)
        db.session.add(favorite)
        db.session.commit()

        return {'message': 'Movie added to favorites'}, 201

    def delete(self, user_id):
        # Удаляем фильм из избранного
        movie_id = request.json.get('movie_id')

        if not movie_id:
            return {'message': 'Movie ID is required'}, 400

        favorite = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if not favorite:
            return {'message': 'Movie not found in favorites'}, 404

        db.session.delete(favorite)
        db.session.commit()

        return {'message': 'Movie removed from favorites'}, 200
# Ресурс для получения всех жанров
class GenreListResource(Resource):
    def get(self):
        genres = Genre.query.all()
        result = [{'id': genre.id, 'name': genre.name} for genre in genres]
        return {'genres': result}, 200

# Ресурс для получения всех актеров
class ActorListResource(Resource):
    def get(self):
        actors = Actor.query.all()
        result = [{'id': actor.id, 'name': actor.name} for actor in actors]
        return {'actors': result}, 200

# Ресурс для получения всех режиссеров
class DirectorListResource(Resource):
    def get(self):
        directors = Director.query.all()
        result = [{'id': director.id, 'name': director.name} for director in directors]
        return {'directors': result}, 200

# Ресурс для получения всех стран
class CountryListResource(Resource):
    def get(self):
        countries = Country.query.all()
        result = [{'id': country.id, 'name': country.name} for country in countries]
        return {'countries': result}, 200

# Ресурсы для связи фильмов с жанрами, актерами, режиссерами, странами
class MovieGenreResource(Resource):
    def get(self, movie_id):
        genres = MovieGenre.query.filter_by(movie_id=movie_id).all()
        result = [{'genre_id': genre.genre_id} for genre in genres]
        return {'genres': result}, 200

class MovieActorResource(Resource):
    def get(self, movie_id):
        actors = MovieActor.query.filter_by(movie_id=movie_id).all()
        result = [{'actor_id': actor.actor_id} for actor in actors]
        return {'actors': result}, 200

class MovieDirectorResource(Resource):
    def get(self, movie_id):
        directors = MovieDirector.query.filter_by(movie_id=movie_id).all()
        result = [{'director_id': director.director_id} for director in directors]
        return {'directors': result}, 200

class MovieCountryResource(Resource):
    def get(self, movie_id):
        countries = MovieCountry.query.filter_by(movie_id=movie_id).all()
        result = [{'country_id': country.country_id} for country in countries]
        return {'countries': result}, 200

class SimilarMoviesResource(Resource):
    def get(self):
        movie_ids = request.args.get('movie_ids', '').split(',')
        if not movie_ids:
            return {'message': 'At least one movie ID is required'}, 400

        # Получаем похожие фильмы из базы данных
        similar_movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()

        movies_data = []
        for movie in similar_movies:
            # Загружаем актеров
            actors = [actor.name for actor in movie.actors]
            # Загружаем режиссеров
            directors = [director.name for director in movie.directors]
            # Загружаем жанры
            genres = [genre.name for genre in movie.genres]
            # Загружаем страны
            countries = [country.name for country in movie.countries]

            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_url': movie.poster_url,
                'release_date': movie.release_date,
                'rating': movie.rating,
                'actors': actors,
                'directors': directors,
                'genres': genres,
                'countries': countries
            }
            movies_data.append(movie_data)

        return movies_data, 200