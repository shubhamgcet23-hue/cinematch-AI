from flask import Flask, render_template, request

from utils.data_loader import DataLoader
from models.collaborative import CollaborativeFiltering
from models.content_based import ContentBasedFiltering
from models.hybrid import HybridRecommender

from utils.tmdb import get_movie_details

app = Flask(__name__)

# -----------------------------
# Load Dataset
# -----------------------------
loader = DataLoader()
data = loader.preprocess()

movies = data["movies"]
ratings = data["ratings"]
ratings_matrix = data["ratings_matrix"]
genre_matrix = data["genre_matrix"]

# -----------------------------
# Initialize Models
# -----------------------------
collab = CollaborativeFiltering(ratings_matrix)
content = ContentBasedFiltering(movies, genre_matrix)
hybrid = HybridRecommender(collab, content)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    movie_list = sorted(movies["title"].unique())
    return render_template(
        "index.html",
        movies=movie_list
    )


# -----------------------------
# Recommendations
# -----------------------------
@app.route("/recommend", methods=["POST"])
def recommend():

    selected_movie = request.form["movie"]

    recommendations = hybrid.recommend(selected_movie)

    if recommendations is None or recommendations.empty:
        return render_template(
            "recommend.html",
            movie=selected_movie,
            recommendations=[]
        )

    recommendation_list = []

    for _, row in recommendations.iterrows():

        movie_info = movies[movies["title"] == row["title"]].iloc[0]

        tmdb = get_movie_details(row["title"])

        recommendation_list.append({

            "movieId": int(movie_info["movieId"]),

            "title": row["title"],

            "genres": movie_info["genres"],

            # Confidence Percentage
            "score": round(float(row["final_score"]) * 100, 1),

            "poster": tmdb["poster"] if tmdb else None,

            "rating": float(tmdb["rating"]) if tmdb and tmdb["rating"] else 0,

            "overview": tmdb["overview"] if tmdb else "Overview not available.",

            "release_date": tmdb["release_date"] if tmdb else "Unknown",

            "popularity": tmdb["popularity"] if tmdb else 0,

            "reason": "Similar genres and similar user preferences"

        })

    return render_template(
        "recommend.html",
        movie=selected_movie,
        recommendations=recommendation_list
    )


# -----------------------------
# Movie Details
# -----------------------------
@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):

    movie = movies[movies["movieId"] == movie_id]

    if movie.empty:
        return "Movie not found", 404

    movie = movie.iloc[0]

    tmdb = get_movie_details(movie["title"])

    return render_template(
        "movie.html",
        movie=movie,
        tmdb=tmdb
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)