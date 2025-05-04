from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from app.resources import UserListResource, UserResource, MovieListResource, MovieResource, \
    FavoriteListResource, GenreListResource, ActorListResource, DirectorListResource, CountryListResource, \
    MovieGenreResource, MovieActorResource, MovieDirectorResource, MovieCountryResource, FavoritesResource, SimilarMoviesResource
# Инициализация приложения и расширений
app = Flask(__name__)

# Конфигурация приложения
app.config.from_object('config.Config')

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация RESTful API
api = Api(app)

# Ресурсы для API
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(MovieListResource, '/movies')
api.add_resource(MovieResource, '/movies/<int:movie_id>')

# Добавление маршрутов для других сущностей
api.add_resource(FavoriteListResource, '/favorites/<int:user_id>')
api.add_resource(GenreListResource, '/genres')
api.add_resource(ActorListResource, '/actors')
api.add_resource(DirectorListResource, '/directors')
api.add_resource(CountryListResource, '/countries')

# Ресурсы для связи фильмов с жанрами, актерами, режиссерами и странами
api.add_resource(MovieGenreResource, '/movies/<int:movie_id>/genres')
api.add_resource(MovieActorResource, '/movies/<int:movie_id>/actors')
api.add_resource(MovieDirectorResource, '/movies/<int:movie_id>/directors')
api.add_resource(MovieCountryResource, '/movies/<int:movie_id>/countries')

api.add_resource(FavoritesResource, '/favorites/<int:user_id>')
api.add_resource(SimilarMoviesResource, '/similars/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
