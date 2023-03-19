import streamlit as st
import pickle
import requests
import os
from os import environ as env
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
DATA = "data/movies.pkl"
SIMILARITIES = "data/similarity.pkl"

if not os.path.isfile(DATA) and not os.path.isfile(SIMILARITIES):
    os.system("echo Hello")
    os.system("pip install pandas")
    os.system("python preprocess_data.py")

data, similarities = pickle.load(open(DATA, "rb")), pickle.load(open(SIMILARITIES, "rb"))
api = (
    "https://api.themoviedb.org/3/movie/{}" f'?api_key={env["API_KEY"]}&language=en-US'
)
image_base_url = "https://image.tmdb.org/t/p/w500/{}"


def fetch_poster(_id):
    result = requests.get(api.format(_id))
    _data = result.json()
    return image_base_url.format(_data["poster_path"])


def recommend(movie):
    movie_index = data[data["title"] == movie].index[0]
    distances = similarities[movie_index]
    movies = enumerate(distances)
    recommended_movies = sorted(movies, reverse=True, key=lambda m: m[1])
    top_5_recommendations = recommended_movies[1:6]

    return [
        (fetch_poster(data.iloc[_id].id), data.iloc[_id].title)
        for _id, _ in top_5_recommendations
    ]


def main():
    st.set_page_config(
        page_title="Movies Recommender", 
        page_icon=Image.open("assets/logo.png"),
        layout='wide',

    )
    st.title("Movie Recommender")
    selected_movie = st.selectbox("Select a movie", data["title"].values)
    recommendations = recommend(selected_movie)
    for (poster, title), column in zip(recommendations, st.columns(5)):
        with column:
            st.text(title)
            st.image(poster)


if __name__ == "__main__":
    main()
