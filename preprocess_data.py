"""
preprocess_data.py: Functions for pre_processing of data
"""

import pickle
import pandas as pd
import ast  # Abstract Syntax Tree
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def convert_to_list(column: str) -> list:
    return [item["name"] for item in ast.literal_eval(column)]


def concatenate_words(strings: list[str]) -> list[str]:
    return [string.replace(" ", "") for string in strings]


def apply_function(movies: pd.DataFrame) -> None:
    movies["genres"] = movies["genres"].apply(convert_to_list)
    movies["keywords"] = movies["keywords"].apply(convert_to_list)
    movies["cast"] = movies["cast"].apply(lambda casts: convert_to_list(casts)[:3])
    movies["crew"] = movies["crew"].apply(
        lambda crews: [
            crew["name"]
            for crew in ast.literal_eval(crews)
            if crew["job"] == "Director"
        ]
    )
    movies["overview"] = movies["overview"].apply(lambda text: text.split())


def apply_concatenate(movies: pd.DataFrame) -> None:
    movies["genres"] = movies["genres"].apply(concatenate_words)
    movies["keywords"] = movies["keywords"].apply(concatenate_words)
    movies["cast"] = movies["cast"].apply(concatenate_words)
    movies["crew"] = movies["crew"].apply(concatenate_words)


def apply_stemming(movies: pd.DataFrame) -> None:
    ps = PorterStemmer()
    movies["tags"] = movies["tags"].apply(
        lambda tags: " ".join(map(ps.stem, tags.split()))
    )


def vectorize(movies: pd.DataFrame):
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"]).toarray()
    return vectors


def calculate_cosine_similarity(vectors) -> None:
    similarity = cosine_similarity(vectors)
    create_file(similarity, "similarity.pkl")


def create_file(data, filename: str) -> None:
    pickle.dump(data, open(f"data\\{filename}", "wb"))


def create_new_df(movies: pd.DataFrame) -> None:
    data = pd.DataFrame(movies[["id", "title", "tags"]])
    data["tags"] = data["tags"].apply(lambda tags: " ".join(map(str.lower, tags)))
    apply_stemming(data)
    create_file(data, "movies.pkl")
    vectors = vectorize(data)
    calculate_cosine_similarity(vectors)


def main():
    credits = pd.read_csv("data/tmdb_5000_credits.csv")
    movies = pd.read_csv("data/tmdb_5000_movies.csv")
    data = movies.merge(credits, on="title")
    data = data[["id", "title", "overview", "genres", "keywords", "cast", "crew"]]
    data.dropna(inplace=True)
    apply_function(data)
    apply_concatenate(data)
    data["tags"] = (
        data["overview"]
        + data["genres"]
        + data["keywords"]
        + data["cast"]
        + data["crew"]
    )
    create_new_df(data)

main()