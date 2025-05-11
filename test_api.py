import requests
import json

def test_recommendations():
    url = "http://localhost:5000/api/recommendations/by-movies"
    headers = {"Content-Type": "application/json"}
    
    # Тест 1: один фильм
    data = {
        "movies": ["Вне юрисдикции"],
        "n": 5
    }
    print("\nТест 1: Рекомендации на основе одного фильма")
    response = requests.post(url, headers=headers, json=data)
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        print("\nРекомендации:")
        for movie in recommendations:
            print(f"- {movie['title']} ({movie['original_title']})")
            print(f"  Жанры: {', '.join(movie['genres'])}")
            print(f"  Актеры: {', '.join(movie['actors'][:3])}")
            print()
    else:
        print(f"Ошибка: {response.text}")
    
    # Тест 2: два фильма
    data = {
        "movies": ["Вне юрисдикции", "Exterritorial"],
        "n": 5
    }
    print("\nТест 2: Рекомендации на основе двух фильмов")
    response = requests.post(url, headers=headers, json=data)
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        print("\nРекомендации:")
        for movie in recommendations:
            print(f"- {movie['title']} ({movie['original_title']})")
            print(f"  Жанры: {', '.join(movie['genres'])}")
            print(f"  Актеры: {', '.join(movie['actors'][:3])}")
            print()
    else:
        print(f"Ошибка: {response.text}")

if __name__ == "__main__":
    test_recommendations() 