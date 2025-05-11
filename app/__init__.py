from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_login import LoginManager
import sys
import os

# Добавляем корневую директорию проекта в путь импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на реальный секретный ключ

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Регистрируем ресурсы и маршруты
    from app.resources import UserListResource, UserResource, MovieListResource, MovieResource
    api = Api(app)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(MovieListResource, '/movies')
    api.add_resource(MovieResource, '/movies/<int:movie_id>')
    
    with app.app_context():
        # Регистрируем blueprint для аутентификации
        from app.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        
        # Регистрируем blueprint для рекомендаций
        from app.routes.recommendations import bp as recommendations_bp, init_app as init_recommender
        app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
        init_recommender(app)

        # Регистрируем blueprint для подбора фильмов
        from app.routes.movie_picker import bp as movie_picker_bp
        app.register_blueprint(movie_picker_bp, url_prefix='/api/picker')

    @app.route('/health')
    def health_check():
        return {'status': 'ok'}, 200

    return app

from app import models
