from movie_recommender import MovieRecommender

def main():
    # Инициализация рекомендательной системы
    recommender = MovieRecommender(data_path='data')
    
    try:
        # Попытка загрузить уже обученную модель
        recommender.load_model()
        print("Модель успешно загружена")
    except FileNotFoundError:
        print("Обучение новой модели...")
        # Загрузка и подготовка данных
        recommender.load_data(
            credits_path='data/tmdb_5000_credits.csv',
            movies_path='data/tmdb_5000_movies.csv'
        )
        # Создание матрицы схожести
        recommender.create_similarity_matrix()
        # Сохранение модели
        recommender.save_model()
        print("Модель успешно обучена и сохранена")

    # Пример получения рекомендаций
    test_movies = ["Avatar", "The Dark Knight"]
    recommendations = recommender.get_recommendations(test_movies, n_recommendations=5)
    
    print(f"\nРекомендации на основе фильмов: {', '.join(test_movies)}")
    for i, movie in enumerate(recommendations, 1):
        print(f"{i}. {movie}")

if __name__ == "__main__":
    main() 