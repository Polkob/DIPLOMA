from app import db
from app.models import Movie, Genre, Actor, Director, Country
import pandas as pd
import numpy as np
from datetime import datetime
import re
import logging

class DataPreprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_external_data(self, movies_path, credits_path):
        """Загрузка данных из внешних источников"""
        try:
            # Загружаем данные из CSV файлов
            movies_df = pd.read_csv(movies_path)
            credits_df = pd.read_csv(credits_path)
            
            return {
                'movies': movies_df,
                'credits': credits_df
            }
        except Exception as e:
            self.logger.error(f"Error loading external data: {str(e)}")
            raise

    def preprocess_data(self, data):
        """Предобработка данных"""
        try:
            movies_df = data['movies']
            credits_df = data['credits']
            
            # Очистка данных
            movies_df = self._clean_movie_data(movies_df)
            credits_df = self._clean_credits_data(credits_df)
            
            # Объединение данных
            merged_df = self._merge_data(movies_df, credits_df)
            
            # Трансформация данных
            processed_data = self._transform_data(merged_df)
            
            return processed_data
        except Exception as e:
            self.logger.error(f"Error preprocessing data: {str(e)}")
            raise

    def validate_data(self, data):
        """Валидация данных"""
        try:
            validation_results = {
                'movies': self._validate_movies(data['movies']),
                'credits': self._validate_credits(data['credits'])
            }
            
            # Проверяем результаты валидации
            if not all(validation_results.values()):
                self.logger.warning("Data validation failed")
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Error validating data: {str(e)}")
            raise

    def _clean_movie_data(self, movies_df):
        """Очистка данных о фильмах"""
        try:
            # Удаление дубликатов
            movies_df = movies_df.drop_duplicates()
            
            # Обработка пропущенных значений
            movies_df['overview'] = movies_df['overview'].fillna('')
            movies_df['poster_path'] = movies_df['poster_path'].fillna('')
            
            # Преобразование дат
            movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
            
            # Очистка жанров
            movies_df['genres'] = movies_df['genres'].apply(self._parse_json_list)
            
            return movies_df
        except Exception as e:
            self.logger.error(f"Error cleaning movie data: {str(e)}")
            raise

    def _clean_credits_data(self, credits_df):
        """Очистка данных о кредитах"""
        try:
            # Удаление дубликатов
            credits_df = credits_df.drop_duplicates()
            
            # Обработка пропущенных значений
            credits_df['cast'] = credits_df['cast'].fillna('[]')
            credits_df['crew'] = credits_df['crew'].fillna('[]')
            
            # Очистка актеров и режиссеров
            credits_df['cast'] = credits_df['cast'].apply(self._parse_json_list)
            credits_df['crew'] = credits_df['crew'].apply(self._parse_json_list)
            
            return credits_df
        except Exception as e:
            self.logger.error(f"Error cleaning credits data: {str(e)}")
            raise

    def _merge_data(self, movies_df, credits_df):
        """Объединение данных о фильмах и кредитах"""
        try:
            # Объединение по ID фильма
            merged_df = pd.merge(movies_df, credits_df, on='id', how='left')
            
            return merged_df
        except Exception as e:
            self.logger.error(f"Error merging data: {str(e)}")
            raise

    def _transform_data(self, merged_df):
        """Трансформация данных"""
        try:
            # Извлечение актеров
            merged_df['actors'] = merged_df['cast'].apply(
                lambda x: [actor['name'] for actor in x[:5]] if isinstance(x, list) else []
            )
            
            # Извлечение режиссеров
            merged_df['directors'] = merged_df['crew'].apply(
                lambda x: [crew['name'] for crew in x if crew.get('job') == 'Director'] if isinstance(x, list) else []
            )
            
            # Очистка названий
            merged_df['title'] = merged_df['title'].apply(self._clean_title)
            
            return merged_df
        except Exception as e:
            self.logger.error(f"Error transforming data: {str(e)}")
            raise

    def _validate_movies(self, movies_df):
        """Валидация данных о фильмах"""
        try:
            # Проверка обязательных полей
            required_fields = ['id', 'title', 'release_date']
            if not all(field in movies_df.columns for field in required_fields):
                return False
            
            # Проверка типов данных
            if not pd.api.types.is_numeric_dtype(movies_df['id']):
                return False
            
            # Проверка дат
            if not pd.api.types.is_datetime64_any_dtype(movies_df['release_date']):
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating movies: {str(e)}")
            return False

    def _validate_credits(self, credits_df):
        """Валидация данных о кредитах"""
        try:
            # Проверка обязательных полей
            required_fields = ['id', 'cast', 'crew']
            if not all(field in credits_df.columns for field in required_fields):
                return False
            
            # Проверка типов данных
            if not pd.api.types.is_numeric_dtype(credits_df['id']):
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating credits: {str(e)}")
            return False

    def _parse_json_list(self, json_str):
        """Парсинг JSON строки в список"""
        try:
            if pd.isna(json_str) or json_str == '[]':
                return []
            return eval(json_str)
        except:
            return []

    def _clean_title(self, title):
        """Очистка названия фильма"""
        try:
            # Удаление специальных символов
            title = re.sub(r'[^\w\s]', '', title)
            # Удаление лишних пробелов
            title = ' '.join(title.split())
            return title
        except:
            return title 