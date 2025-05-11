import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import pickle
import os

class MovieRecommender:
    def __init__(self, data_path='data'):
        """
        Инициализация рекомендательной системы
        :param data_path: путь к директории с данными
        """
        self.data_path = data_path
        self.movies = None
        self.movies_data = None
        self.similarity_matrix = None
        self.ps = PorterStemmer()
        nltk.download('stopwords')
        
    def _preprocess_text(self, text):
        """Предобработка текста"""
        if pd.isna(text):
            return ''
            
        # Разбиваем текст на слова
        words = text.split()
        
        # Стемминг
        stemmed = [self.ps.stem(word) for word in words]
        
        # Удаление стоп-слов
        stop_words = set(stopwords.words('english'))
        filtered = [word.lower() for word in stemmed if word.lower() not in stop_words]
        
        # Удаление пунктуации и коротких слов
        result = []
        for word in filtered:
            word = word.translate(str.maketrans('', '', string.punctuation))
            if len(word) > 2:
                result.append(word)
        
        return ' '.join(result)

    def load_data(self, credits_path, movies_path):
        """
        Загрузка и подготовка данных
        :param credits_path: путь к файлу с данными о создателях фильмов
        :param movies_path: путь к файлу с данными о фильмах
        """
        # Загружаем данные
        self.movies_data = pd.read_csv(movies_path)
        
        # Создаем признаки для рекомендаций
        self.movies_data['tags'] = self.movies_data.apply(
            lambda row: ' '.join(filter(None, [
                str(row['overview']) if pd.notna(row['overview']) else '',
                str(row['genres']) if pd.notna(row['genres']) else '',
                str(row['top_cast']) if pd.notna(row['top_cast']) else '',
                str(row['directors']) if pd.notna(row['directors']) else '',
                str(row['production_countries']) if pd.notna(row['production_countries']) else '',
                str(row['keywords']) if pd.notna(row['keywords']) else ''
            ])),
            axis=1
        )
        
        # Предобработка текста
        self.movies_data['tags'] = self.movies_data['tags'].apply(self._preprocess_text)
        
        # Сохранение нужных колонок
        self.movies = self.movies_data[['id', 'title', 'original_title', 'tags']]

    def create_similarity_matrix(self):
        """Создание матрицы схожести фильмов"""
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(self.movies['tags']).toarray()
        self.similarity_matrix = cosine_similarity(vectors)

    def save_model(self, filename='movie_recommender.pkl'):
        """Сохранение модели"""
        model_data = {
            'movies': self.movies,
            'similarity_matrix': self.similarity_matrix
        }
        with open(os.path.join(self.data_path, filename), 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filename='movie_recommender.pkl'):
        """Загрузка модели"""
        with open(os.path.join(self.data_path, filename), 'rb') as f:
            model_data = pickle.load(f)
        self.movies = model_data['movies']
        self.similarity_matrix = model_data['similarity_matrix']

    def get_recommendations(self, movie_ids, n_recommendations=10):
        """
        Получение рекомендаций на основе ID фильмов
        :param movie_ids: список ID фильмов (от 1 до 3)
        :param n_recommendations: количество рекомендаций
        :return: список ID рекомендованных фильмов
        """
        if isinstance(movie_ids, int):
            movie_ids = [movie_ids]
        
        if not 1 <= len(movie_ids) <= 3:
            raise ValueError("Количество фильмов должно быть от 1 до 3")
        
        # Получение индексов фильмов
        movie_indices = []
        for movie_id in movie_ids:
            try:
                idx = self.movies[self.movies['id'] == movie_id].index[0]
                movie_indices.append(idx)
            except IndexError:
                print(f"Фильм с ID {movie_id} не найден в базе данных")
                continue
        
        if not movie_indices:
            return []
        
        # Расчет суммарной схожести
        similarity_scores = np.zeros(len(self.movies))
        for idx in movie_indices:
            similarity_scores += self.similarity_matrix[idx]
        
        # Получение индексов рекомендаций
        movie_indices = list(enumerate(similarity_scores))
        movie_indices = sorted(movie_indices, key=lambda x: x[1], reverse=True)
        movie_indices = [i[0] for i in movie_indices if i[0] not in movie_indices]
        
        # Возврат ID рекомендованных фильмов
        recommendations = self.movies.iloc[movie_indices[:n_recommendations]]
        return recommendations['id'].tolist() 