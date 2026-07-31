import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class HybridRecommender:

    def __init__(self, collaborative_model, content_model, alpha=0.7):

        self.collaborative = collaborative_model
        self.content = content_model
        self.alpha = alpha

    def normalize(self, dataframe, column):

        scaler = MinMaxScaler()

        dataframe[column] = scaler.fit_transform(
            dataframe[[column]]
        )

        return dataframe

    def recommend(self, movie_title, top_n=10):

        collab = self.collaborative.recommend(
            movie_title,
            top_n=100
        )

        content = self.content.recommend(
            movie_title,
            top_n=100
        )

        if collab is None or content is None:
            return None

        collab = collab.rename(
            columns={"score": "collab_score"}
        )

        content = content.rename(
            columns={"score": "content_score"}
        )

        collab = self.normalize(
            collab,
            "collab_score"
        )

        content = self.normalize(
            content,
            "content_score"
        )

        merged = pd.merge(
            collab,
            content,
            on="title",
            how="outer"
        )

        merged.fillna(0, inplace=True)

        merged["final_score"] = (

            self.alpha * merged["collab_score"]

            +

            (1 - self.alpha) * merged["content_score"]

        )

        merged = merged.sort_values(
            "final_score",
            ascending=False
        )

        return merged.head(top_n)