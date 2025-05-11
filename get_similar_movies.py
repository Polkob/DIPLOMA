import requests
import json

def print_movie(movie):
    print(f"\nID: {movie['id']}")
    print(f"Title: {movie['title']}")
    print(f"Overview: {movie['overview']}")
    print(f"Poster: {movie['poster_url']}")

print("Starting script...")

# Создаем сессию для сохранения cookies
session = requests.Session()

print("\nTrying to login...")
# Логинимся
login_response = session.post(
    'http://localhost:5000/api/auth/login',
    json={
        'username': 'test_user',
        'password': 'test_password'  # Используем обычный пароль
    }
)
print(f"Login status: {login_response.status_code}")
print(f"Login response: {login_response.text}")

print("\nTrying to build matrices...")
# Строим матрицы схожести
build_response = session.post('http://localhost:5000/api/recommendations/build-matrices')
print(f"Build matrices status: {build_response.status_code}")
print(f"Build matrices response: {build_response.text}")

# Тестовые фильмы
test_movies = [
    {"id": 1, "title": "Forrest Gump"},
    {"id": 2, "title": "The Shawshank Redemption"},
    {"id": 3, "title": "Твоё имя"}
]

# Получаем похожие фильмы для каждого тестового фильма
for movie in test_movies:
    print(f"\n{'='*50}")
    print(f"Getting similar movies for: {movie['title']} (ID: {movie['id']})")
    
    try:
        response = session.get(f'http://localhost:5000/api/recommendations/similar-movies/{movie["id"]}')
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nOriginal movie:")
            print_movie(data['movie'])
            
            print("\nSimilar movies:")
            for similar_movie in data['similar_movies']:
                print_movie(similar_movie)
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error while processing movie {movie['id']}: {str(e)}") 