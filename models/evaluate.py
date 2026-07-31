import pandas as pd
from sklearn.model_selection import train_test_split

from utils.data_loader import DataLoader
from models.collaborative import CollaborativeFiltering
from models.content_based import ContentBasedFiltering
from models.hybrid import HybridRecommender


class Evaluator:

    def __init__(self):

        loader = DataLoader()

        data = loader.preprocess()

        self.movies = data["movies"]
        self.ratings = data["ratings"]

    def precision_at_k(self, k=5):

        train, test = train_test_split(
            self.ratings,
            test_size=0.2,
            random_state=42
        )

        merged = train.merge(
            self.movies,
            on="movieId"
        )

        ratings_matrix = merged.pivot_table(
            index="userId",
            columns="title",
            values="rating"
        )

        loader = DataLoader()

        genre_matrix = loader.preprocess()["genre_matrix"]

        collab = CollaborativeFiltering(
            ratings_matrix
        )

        content = ContentBasedFiltering(
            self.movies,
            genre_matrix
        )

        hybrid = HybridRecommender(
            collab,
            content,
            alpha=0.7
        )

        precisions = []

        users = test["userId"].unique()

        for user in users:

            liked = test[
                (test.userId == user) &
                (test.rating >= 4)
            ]

            if liked.empty:
                continue

            movie_id = liked.iloc[0]["movieId"]

            movie_title = self.movies[
                self.movies.movieId == movie_id
            ].iloc[0]["title"]

            recommendations = hybrid.recommend(
                movie_title,
                top_n=k
            )

            if recommendations is None:
                continue

            recommended_titles = set(
                recommendations["title"]
            )

            liked_titles = set(

                self.movies[
                    self.movies.movieId.isin(
                        liked.movieId
                    )
                ]["title"]

            )

            relevant = len(
                recommended_titles &
                liked_titles
            )

            precisions.append(
                relevant / k
            )

        return sum(precisions) / len(precisions)