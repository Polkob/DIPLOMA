from tmdb_api import get_similar_movies
from itertools import chain

def recommend_movies(movie_ids):
    all_recommendations = [get_similar_movies(mid) for mid in movie_ids]
    flat = list(chain.from_iterable(all_recommendations))
    seen = set()
    unique_recommendations = []
    for movie in flat:
        if movie["id"] not in seen:
            unique_recommendations.append(movie)
            seen.add(movie["id"])
    return unique_recommendations[:10]
