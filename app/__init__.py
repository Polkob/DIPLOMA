from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
import sys
import os

# Добавляем корневую директорию проекта в путь импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрируем ресурсы и маршруты
    from app.resources import UserListResource, UserResource, MovieListResource, MovieResource
    api = Api(app)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(MovieListResource, '/movies')
    api.add_resource(MovieResource, '/movies/<int:movie_id>')

    return app
