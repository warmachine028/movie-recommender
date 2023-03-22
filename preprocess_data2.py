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
    movies["Genres"] = movies["Genres"].apply(convert_to_list)
    movies["Keywords"] = movies["Keywords"].apply(convert_to_list)
    movies["Cast"] = movies["Cast"].apply(lambda casts: convert_to_list(casts)[:3])
    movies["Crew"] = movies["Crew"].apply(
        lambda crews: [
            crew["name"]
            for crew in ast.literal_eval(crews)
            if crew["job"] == "Director"
        ]
    )
    movies["overview"] = movies["overview"].apply(lambda text: text.split())


def apply_concatenate(movies: pd.DataFrame) -> None:
    movies["Genres"] = movies["Genres"].apply(concatenate_words)
    movies["Keywords"] = movies["Keywords"].apply(concatenate_words)
    movies["Cast"] = movies["Cast"].apply(concatenate_words)
    movies["Crew"] = movies["Crew"].apply(concatenate_words)


def apply_stemming(movies: pd.DataFrame) -> None:
    ps = PorterStemmer()
    movies["tags"] = movies["tags"].apply(
        lambda tags: " ".join(map(ps.stem, tags.split()))
    )


def vectorize(movies: pd.DataFrame):
    cv = CountVectorizer(max_features=10_000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"]).toarray()
    return vectors


def calculate_cosine_similarity(vectors) -> None:
    similarity = cosine_similarity(vectors)
    create_file(similarity, "similarity.pkl")


def create_file(data, filename: str) -> None:
    pickle.dump(data, open(f"data/{filename}", "wb"))


def create_new_df(movies: pd.DataFrame) -> None:
    data = pd.DataFrame(movies[["id", "title", "tags"]])
    data["tags"] = data["tags"].apply(lambda tags: " ".join(map(str.lower, tags)))
    apply_stemming(data)
    create_file(data, "movies.pkl")
    vectors = vectorize(data)
    calculate_cosine_similarity(vectors)


def main():
    credits = pd.read_csv("data/10000 Credits Data.csv")
    movies = pd.read_csv("data/10000 Movies Data.csv")
    data = movies.merge(credits, on="Movie_id")
    data = data.loc[:, ("Movie_id", "title_x", "overview", "Genres", "Keywords", "Cast", "Crew")]
    data.rename(columns={'Movie_id': 'id', 'title_x': 'title'}, inplace=True)
    data.dropna(inplace=True)
    apply_function(data)
    apply_concatenate(data)
    data["tags"] = (
        data["overview"]
        + data["Genres"]
        + data["Keywords"]
        + data["Cast"]
        + data["Crew"]
    )
    create_new_df(data)

main()