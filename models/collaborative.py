import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFiltering:

    def __init__(self, ratings_matrix):
        """
        ratings_matrix:
        Rows = Users
        Columns = Movies
        """

        self.ratings_matrix = ratings_matrix

        # Replace NaN with 0
        self.movie_matrix = ratings_matrix.fillna(0).T

        # Calculate cosine similarity between movies
        similarity = cosine_similarity(self.movie_matrix)

        self.similarity_df = pd.DataFrame(
            similarity,
            index=self.movie_matrix.index,
            columns=self.movie_matrix.index
        )

    def recommend(self, movie_title, top_n=10):

        if movie_title not in self.similarity_df.index:
            return None

        recommendations = (
            self.similarity_df[movie_title]
            .sort_values(ascending=False)
            .drop(movie_title)
            .head(top_n)
            .reset_index()
        )

        recommendations.columns = ["title", "score"]

        return recommendations