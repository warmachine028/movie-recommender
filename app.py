import streamlit as st
import pickle
import requests

from os import environ as env

from dotenv import load_dotenv

load_dotenv()

data = pickle.load(open('movies.pkl', 'rb'))
similarities = pickle.load(open('similarity.pkl', 'rb'))
api = (
    'https://api.themoviedb.org/3/movie/{}'
    f'?api_key={env["API_KEY"]}&language=en-US'
)
image_base_url = 'https://image.tmdb.org/t/p/w500/{}'


def fetch_poster(_id):
    result = requests.get(api.format(_id))
    _data = result.json()
    return image_base_url.format(_data['poster_path'])


def recommend(movie):
    movie_index = data[data['title'] == movie].index[0]
    distances = similarities[movie_index]
    movies = enumerate(distances)
    recommended_movies = sorted(movies, reverse=True, key=lambda m: m[1])
    top_5_recommendations = recommended_movies[1:6]

    return [
        (
            fetch_poster(data.iloc[_id].id), data.iloc[_id].title
        ) for _id, _ in top_5_recommendations
    ]


st.title('Movie Recommender')
selected_movie = st.selectbox('Select a movie', data['title'].values)
if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    for (poster, title), column in zip(recommendations, st.columns(5)):
        with column:
            st.text(title)
            st.image(poster)
