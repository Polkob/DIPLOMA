import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from app.models import Movie, Genre, Actor, Country
from app import db

class HybridRecommender:
    def __init__(self, app=None):
        self.app = app
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.content_similarity_matrix = None
        self.movie_id_to_index = {}
        self.index_to_movie_id = {}
        
    def init_app(self, app):
        self.app = app

    def _get_movie_features(self, movie):
        """Извлечение признаков фильма для контентных рекомендаций"""
        features = []
        
        # Добавляем жанры
        genres = [genre.name for genre in movie.genres]
        features.extend(genres)
        
        # Добавляем актеров
        actors = [actor.name for actor in movie.actors]
        features.extend(actors)
        
        # Добавляем страны
        countries = [country.name for country in movie.countries]
        features.extend(countries)
        
        # Добавляем описание
        if movie.overview:
            features.append(movie.overview)
            
        return ' '.join(features)
    
    def build_content_similarity_matrix(self):
        """Построение матрицы схожести фильмов на основе контента"""
        with self.app.app_context():
            movies = Movie.query.all()
            print(f"\nBuilding content similarity matrix for {len(movies)} movies")
            
            # Получаем признаки для каждого фильма
            movie_features = [self._get_movie_features(movie) for movie in movies]
            
            print("\nMovie features extracted")
            
            # Создаем TF-IDF матрицу
            tfidf_matrix = self.tfidf.fit_transform(movie_features)
            print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
            
            # Вычисляем косинусное сходство
            self.content_similarity_matrix = cosine_similarity(tfidf_matrix)
            print(f"Content similarity matrix shape: {self.content_similarity_matrix.shape}")
            
            # Сохраняем соответствие индексов и ID фильмов
            self.movie_id_to_index = {movie.id: idx for idx, movie in enumerate(movies)}
            self.index_to_movie_id = {idx: movie.id for idx, movie in enumerate(movies)}
            print("Movie indices mapping created")
    
    def get_content_based_recommendations(self, movie_id, n_recommendations=10):
        """Получение рекомендаций на основе контента"""
        print(f"\nGetting content-based recommendations for movie_id={movie_id}")
        print(f"Available movie indices: {self.movie_id_to_index}")
        
        if movie_id not in self.movie_id_to_index:
            print(f"Movie ID {movie_id} not found in index mapping")
            return []
        
        movie_idx = self.movie_id_to_index[movie_id]
        print(f"Movie index in similarity matrix: {movie_idx}")
        
        similarity_scores = self.content_similarity_matrix[movie_idx]
        print(f"Similarity scores shape: {similarity_scores.shape}")
        print(f"Top 5 similarity scores: {sorted(similarity_scores, reverse=True)[:5]}")
        
        # Получаем индексы фильмов, отсортированные по схожести
        similar_indices = np.argsort(similarity_scores)[::-1][1:n_recommendations+1]
        print(f"Similar movie indices: {similar_indices}")
        
        # Преобразуем индексы обратно в ID фильмов
        similar_movie_ids = [self.index_to_movie_id[idx] for idx in similar_indices]
        print(f"Similar movie IDs: {similar_movie_ids}")
        
        return similar_movie_ids 