import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedFiltering:

    def __init__(self, movies, genre_matrix):

        self.movies = movies
        self.genre_matrix = genre_matrix

        self.similarity = cosine_similarity(genre_matrix)

        # Create a unique mapping from movie title to index
        self.indices = (
            movies.reset_index()
            .drop_duplicates(subset="title")
            .set_index("title")["index"]
)

    def recommend(self, movie_title, top_n=10):

        if movie_title not in self.indices:
            return None

        idx = int(self.indices.loc[movie_title])

        similarity_scores = [
            (i, float(score))
            for i, score in enumerate(self.similarity[idx])
        ]

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        similarity_scores = similarity_scores[1:top_n + 1]

        movie_indices = [i[0] for i in similarity_scores]

        recommendations = self.movies.iloc[movie_indices][["title"]].copy()

        recommendations["score"] = [
            score for _, score in similarity_scores
        ]

        return recommendations.reset_index(drop=True)