import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedFiltering:

    def __init__(self, movies, genre_matrix):

        self.movies = movies
        self.genre_matrix = genre_matrix

        self.indices = (
            movies.reset_index()
            .drop_duplicates(subset="title")
            .set_index("title")["index"]
        )

    def recommend(self, movie_title, top_n=10):

        if movie_title not in self.indices.index:
            return None

        idx = int(self.indices.loc[movie_title])

        # Compute similarity ONLY for the selected movie
        similarity = cosine_similarity(
            self.genre_matrix[idx],
            self.genre_matrix
        ).flatten()

        similarity_scores = list(enumerate(similarity))

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:top_n + 1]

        movie_indices = [i for i, _ in similarity_scores]

        recommendations = self.movies.iloc[movie_indices][["title"]].copy()

        recommendations["score"] = [
            float(score)
            for _, score in similarity_scores
        ]

        return recommendations.reset_index(drop=True)