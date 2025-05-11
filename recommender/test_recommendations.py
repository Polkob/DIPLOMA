import os
from movie_recommender import MovieRecommender

def main():
    # Получаем путь к директории скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    # Инициализируем рекомендательную систему
    recommender = MovieRecommender(data_path=data_dir)
    
    # Пытаемся загрузить существующую модель
    try:
        recommender.load_model()
        print("Модель успешно загружена")
    except FileNotFoundError:
        print("Обучение новой модели...")
        # Загружаем данные и создаем модель
        recommender.load_data(
            credits_path=os.path.join(data_dir, 'credits.csv'),
            movies_path=os.path.join(data_dir, 'movies.csv')
        )
        recommender.create_similarity_matrix()
        recommender.save_model()
        print("Модель успешно обучена и сохранена")

    # Тестируем рекомендации на основе одного фильма
    print("\nРекомендации на основе фильмов: Вне юрисдикции")
    recommendations = recommender.get_recommendations("Вне юрисдикции")
    for title, original_title in recommendations:
        print(f"{title} ({original_title})")

    # Тестируем рекомендации на основе двух фильмов
    print("\nРекомендации на основе фильмов: Вне юрисдикции, Exterritorial")
    recommendations = recommender.get_recommendations(["Вне юрисдикции", "Exterritorial"])
    for title, original_title in recommendations:
        print(f"{title} ({original_title})")

    # Тестируем рекомендации на основе трех фильмов
    print("\nРекомендации на основе фильмов: Вне юрисдикции, Exterritorial, Вне юрисдикции")
    recommendations = recommender.get_recommendations(["Вне юрисдикции", "Exterritorial", "Вне юрисдикции"])
    for title, original_title in recommendations:
        print(f"{title} ({original_title})")

if __name__ == "__main__":
    main() 