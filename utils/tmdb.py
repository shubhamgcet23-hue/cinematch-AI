import os
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def split_title_year(movie_title):
    """
    Converts:
        Toy Story (1995)

    Into:
        title = Toy Story
        year = 1995
    """

    match = re.search(r"\((\d{4})\)$", movie_title)

    if match:
        year = match.group(1)
        title = movie_title[:match.start()].strip()
    else:
        title = movie_title
        year = None

    return title, year


def get_movie_details(movie_title):
    """
    Fetch movie information from TMDb.

    Returns:
    {
        poster,
        rating,
        overview,
        release_date,
        popularity
    }
    """

    if not API_KEY:
        print("TMDB API Key not found.")
        return None

    title, year = split_title_year(movie_title)

    params = {
        "api_key": API_KEY,
        "query": title,
        "include_adult": False
    }

    if year:
        params["year"] = year

    try:

        response = requests.get(
            SEARCH_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        movie = results[0]

        poster = None

        if movie.get("poster_path"):
            poster = IMAGE_BASE_URL + movie["poster_path"]

        return {
            "poster": poster,
            "rating": movie.get("vote_average", "N/A"),
            "overview": movie.get(
                "overview",
                "Overview not available."
            ),
            "release_date": movie.get(
                "release_date",
                "Unknown"
            ),
            "popularity": movie.get(
                "popularity",
                0
            )
        }

    except requests.exceptions.RequestException as e:

        print(f"TMDb API Error: {e}")

        return None