import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeFiltering:

    def __init__(self, ratings_matrix):

        self.movie_matrix = ratings_matrix.fillna(0).T

    def recommend(self, movie_title, top_n=10):

        if movie_title not in self.movie_matrix.index:
            return None

        movie_vector = self.movie_matrix.loc[[movie_title]]

        similarity = cosine_similarity(
            movie_vector,
            self.movie_matrix
        ).flatten()

        similarity_df = pd.DataFrame({

            "title": self.movie_matrix.index,

            "score": similarity

        })

        similarity_df = similarity_df[
            similarity_df["title"] != movie_title
        ]

        similarity_df = similarity_df.sort_values(
            "score",
            ascending=False
        )

        return similarity_df.head(top_n).reset_index(drop=True)