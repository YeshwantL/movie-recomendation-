from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import requests
import os

app = Flask(__name__)
CORS(app) # Enable CORS for your entire app

# Your TMDb API key (store securely in environment variables recommended)
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '14a28bbe51139037bdb77720e4e3f694')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# A mapping from genre names to TMDb genre IDs
GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Horror": 27,
    "Romance": 10749,
    "Sci-Fi": 878
}

def format_movie_data(movie):
    """Helper function to format movie data consistently."""
    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "genre_ids": movie.get("genre_ids"),
        "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None
    }

def tmdb_get(endpoint, params=None):
    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    try:
        response = requests.get(f"{TMDB_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from TMDb: {e}")
        return None

@app.route('/movies/popular')
def popular_movies():
    data = tmdb_get('movie/popular')
    if not data or 'results' not in data:
        return jsonify([])
    movies = [format_movie_data(movie) for movie in data.get('results', [])]
    return jsonify(movies)

@app.route('/movies/search')
def search_movies():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    data = tmdb_get('search/movie', params={"query": query})
    if not data or 'results' not in data:
        return jsonify([])
    movies = [format_movie_data(movie) for movie in data.get('results', [])]
    return jsonify(movies)

# --- THIS IS THE NEW, FIXED ENDPOINT ---
@app.route('/recommend')
def recommend_by_genre():
    genre_name = request.args.get('genre')
    if not genre_name:
        return jsonify({"error": "Genre parameter is required"}), 400

    genre_id = GENRE_MAP.get(genre_name)
    if not genre_id:
        return jsonify({"error": "Invalid genre specified"}), 400

    # Use TMDb's 'discover' endpoint to find movies by genre
    data = tmdb_get('discover/movie', params={"with_genres": genre_id, "sort_by": "popularity.desc"})
    if not data or 'results' not in data:
        return jsonify([])

    movies = [format_movie_data(movie) for movie in data.get('results', [])]
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True, port=5000)