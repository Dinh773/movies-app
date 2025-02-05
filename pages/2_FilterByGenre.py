import streamlit as st
import pickle 
import requests

def fetch_movies_by_genre(genre_id, num_results=5):
    url=f"https://api.themoviedb.org/3/discover/movie?api_key=b7fd7209a587422f2b3000c0875d3a95&with_genres={genre_id}"
    data=requests.get(url)
    data=data.json()
    movies = data.get('results', []) 

    movie_list = []
    for movie in movies[:num_results]:
        title=movie['title']
        poster_path=movie['poster_path']
        overview=movie["overview"]
        vote=movie["vote_average"]
        if poster_path:
            full_path="https://image.tmdb.org/t/p/w500/"+poster_path
        else:
            full_path = "https://via.placeholder.com/500x750?text=No+Image"
        movie_list.append((title, full_path,overview,vote))
      
    return  movie_list

GENRES = {
    "Action": 28,
    "Aventure": 12,
    "Animation": 16,
    "Comédie": 35,
    "Crime": 80,
    "Drame": 18,
    "Fantastic": 14,
    "Horror": 27,
    "Science-fiction": 878,
    "Thriller": 53
}

st.title("Filter by genre")

genre_buttons = [
    ("Horror", "horror_btn"),
    ("Action", "action_btn"),
    ("Thriller", "thriller_btn"),
    ("Science-fiction", "scifi_btn"),
    ("Aventure", "adventure_btn"),
    ("Animation", "animation_btn"),
    ("Crime", "crime_btn"),
    ("Fantastic", "fantastic_btn"),
]


with st.container():
    cols = st.columns(4)  
    
    
    clicked_genre = None
    for i, (genre, key) in enumerate(genre_buttons):
        with cols[i % 4]:  
            if st.button(genre, key=key):
                clicked_genre = genre  

st.divider()



if clicked_genre:
    st.subheader(f"🎬 {clicked_genre} movies")
    genre_id = GENRES[clicked_genre]
    movies = fetch_movies_by_genre(genre_id, num_results=20)
    
    for title, poster, overview, vote in movies:
        col1, col2, col3 = st.columns([1, 2, 1]) 
        
        with col1:
            st.image(poster, width=200)

        with col2:
            st.subheader(title)
            st.write("📖 **Overview**")
            st.write(overview)

        with col3:
            st.write("⭐ **Rating**")
            st.subheader(f"{vote}/10")

        st.divider()