from app import db
from app.models import Movie, User, Favorite, RecommendationLog
from recommender.hybrid_recommender import HybridRecommender
from recommender.movie_recommender import MovieRecommender
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
import os
from datetime import datetime

class ModelTrainer:
    def __init__(self, model_path='recommender/data'):
        self.model_path = model_path
        self.hybrid_recommender = HybridRecommender()
        self.movie_recommender = MovieRecommender(data_path=model_path)
        self.metrics = {}

    def prepare_training_data(self):
        """Подготовка данных для обучения"""
        try:
            # Получаем все избранные фильмы пользователей
            favorites = Favorite.query.all()
            
            # Создаем матрицу пользователь-фильм
            user_movie_matrix = {}
            for fav in favorites:
                if fav.user_id not in user_movie_matrix:
                    user_movie_matrix[fav.user_id] = []
                user_movie_matrix[fav.user_id].append(fav.movie_id)
            
            return user_movie_matrix
        except Exception as e:
            raise Exception(f"Error preparing training data: {str(e)}")

    def train_recommendation_model(self):
        """Обучение модели рекомендаций"""
        try:
            # Подготавливаем данные
            training_data = self.prepare_training_data()
            
            # Обучаем гибридную модель
            self.hybrid_recommender.train(training_data)
            
            # Обучаем модель на основе контента
            self.movie_recommender.create_similarity_matrix()
            
            # Сохраняем модели
            self.save_models()
            
            # Оцениваем качество
            self.evaluate_model()
            
            return True
        except Exception as e:
            raise Exception(f"Error training recommendation model: {str(e)}")

    def update_model(self, new_data):
        """Обновление модели на основе новых данных"""
        try:
            # Обновляем данные для обучения
            training_data = self.prepare_training_data()
            training_data.update(new_data)
            
            # Переобучаем модель
            self.train_recommendation_model()
            
            # Логируем обновление
            self.log_model_update()
            
            return True
        except Exception as e:
            raise Exception(f"Error updating model: {str(e)}")

    def evaluate_model(self):
        """Оценка качества модели"""
        try:
            # Получаем тестовые данные
            test_data = self.prepare_training_data()
            
            # Оцениваем гибридную модель
            hybrid_metrics = self.hybrid_recommender.evaluate(test_data)
            
            # Оцениваем контентную модель
            content_metrics = self.movie_recommender.evaluate()
            
            self.metrics = {
                'hybrid': hybrid_metrics,
                'content': content_metrics,
                'timestamp': datetime.now().isoformat()
            }
            
            return self.metrics
        except Exception as e:
            raise Exception(f"Error evaluating model: {str(e)}")

    def save_models(self):
        """Сохранение обученных моделей"""
        try:
            # Создаем директорию, если её нет
            if not os.path.exists(self.model_path):
                os.makedirs(self.model_path)
            
            # Сохраняем гибридную модель
            self.hybrid_recommender.save_model(
                os.path.join(self.model_path, 'hybrid_model.pkl')
            )
            
            # Сохраняем контентную модель
            self.movie_recommender.save_model()
            
            return True
        except Exception as e:
            raise Exception(f"Error saving models: {str(e)}")

    def load_models(self):
        """Загрузка сохраненных моделей"""
        try:
            # Загружаем гибридную модель
            self.hybrid_recommender.load_model(
                os.path.join(self.model_path, 'hybrid_model.pkl')
            )
            
            # Загружаем контентную модель
            self.movie_recommender.load_model()
            
            return True
        except Exception as e:
            raise Exception(f"Error loading models: {str(e)}")

    def log_model_update(self):
        """Логирование обновления модели"""
        try:
            # Создаем запись в базе данных
            log = RecommendationLog(
                model_type='hybrid',
                metrics=self.metrics,
                created_at=datetime.now()
            )
            db.session.add(log)
            db.session.commit()
            
            return True
        except Exception as e:
            raise Exception(f"Error logging model update: {str(e)}")

    def get_model_metrics(self):
        """Получение метрик модели"""
        return self.metrics 