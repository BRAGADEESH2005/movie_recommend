import streamlit as st 
import pickle
import pandas as pd 
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variable
api_key = os.getenv('API_KEY')


def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,api_key))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx status codes)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        return None




def recommend(movie):
    movie_index = movies[movies.title == movie].index[0]
    distances =similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    recommended_movies=[]
    posters=[]
    for i in movies_list:
        movie_id =movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies,posters
    
    

movies_dict = pickle.load(open('movie_dictf.pkl','rb'))
movies=pd.DataFrame(movies_dict)
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Which movie do you like?',movies['title'].values)
similarity = pickle.load(open('similarity.pkl','rb'))

if st.button('Recommend'):
    reco,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(reco[0])
        st.image(posters[0])
    with col2:
        st.text(reco[1])
        st.image(posters[1])
    with col3:
        st.text(reco[2])
        st.image(posters[2])
    with col4:
        st.text(reco[3])
        st.image(posters[3])
    with col5:
        st.text(reco[4])
        st.image(posters[4])
    
    