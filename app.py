from flask import Flask, request, jsonify
from recommender import recommend_movies
from tmdb_api import get_movie_by_title

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    selected_movies = request.json.get("movies", [])
    recommendations = recommend_movies(selected_movies)
    return jsonify(recommendations)

@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    return jsonify(get_movie_by_title(title))

if __name__ == "__main__":
    app.run(debug=True)
