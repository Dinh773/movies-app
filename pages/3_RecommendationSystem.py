import streamlit as st
import pickle 
import requests

def fetch_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=b7fd7209a587422f2b3000c0875d3a95".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    if poster_path:
        full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Image"  
    return full_path
movies=pickle.load(open("movies_list.pkl",'rb'))
similarity=pickle.load(open("similarity.pkl",'rb'))
movies_list=movies['title'].values

st.header("AI Recommendation System")

selected_movie=st.selectbox("Select a movie:",movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda vector: vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if st.button("Recommend"):
    movie_name,movie_poster=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:  
        st.image(movie_poster[0])
        st.text(movie_name[0])
    with col2:
        st.image(movie_poster[1])
        st.text(movie_name[1])
    with col3:
        st.image(movie_poster[2])
        st.text(movie_name[2])
    with col4: 
        st.image(movie_poster[3])
        st.text(movie_name[3])
    with col5:
        st.image(movie_poster[4])
        st.text(movie_name[4])