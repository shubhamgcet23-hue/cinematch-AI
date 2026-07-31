import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


class DataLoader:

    def __init__(self):
        self.movies = pd.read_csv("data/movies.csv")
        self.ratings = pd.read_csv("data/ratings.csv")

    def preprocess(self):

        merged = pd.merge(
            self.ratings,
            self.movies,
            on="movieId"
        )

        ratings_matrix = merged.pivot_table(
            index="userId",
            columns="title",
            values="rating"
        )

        tfidf = TfidfVectorizer(stop_words="english")

        genre_matrix = tfidf.fit_transform(
            self.movies["genres"].fillna("")
        )

        return {
            "movies": self.movies,
            "ratings": self.ratings,
            "merged": merged,
            "ratings_matrix": ratings_matrix,
            "genre_matrix": genre_matrix,
        }