import pickle
import os

import pandas as pd
import requests
import streamlit as st


POSTER_BASE_URL = "http://image.tmdb.org/t/p/w500/"


@st.cache_data
def load_data():
    movies_df = pd.DataFrame(pickle.load(open("movies_dict.pkl", "rb")))
    similarity_matrix = pickle.load(open("similarity_dict.pkl", "rb"))
    return movies_df, similarity_matrix


def get_tmdb_api_key():
    try:
        if "tmdb_api_key" in st.secrets:
            return st.secrets["tmdb_api_key"]
    except (FileNotFoundError, KeyError):
        pass
    return os.getenv("TMDB_API_KEY")


def fetch_poster(movie_id):
    api_key = get_tmdb_api_key()
    if not api_key:
        return None

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return POSTER_BASE_URL + poster_path
    except requests.RequestException:
        return None

    return None


def recommended(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1],
    )[1:6]

    names, posters = [], []
    for index, _score in movie_list:
        movie_id = movies.iloc[index].movie_id
        names.append(movies.iloc[index].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


movies, similarity = load_data()

st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a Movie", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommended(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.caption("Poster unavailable")
