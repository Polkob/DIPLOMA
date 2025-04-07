import httpx
from dotenv import load_dotenv

# Можно оставить на будущее, если решишь всё-таки использовать .env
# load_dotenv()

API_KEY = "54a2541709252b5e3de68b7642666940"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_by_title(title):
    params = {"api_key": API_KEY, "query": title}
    try:
        response = httpx.get(f"{BASE_URL}/search/movie", params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return []

def get_similar_movies(movie_id):
    params = {"api_key": API_KEY}
    try:
        response = httpx.get(f"{BASE_URL}/movie/{movie_id}/similar", params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return []
