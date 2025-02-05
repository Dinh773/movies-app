import json
import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK

if not firebase_admin._apps:
    # Charger les secrets depuis Streamlit
    key_dict = st.secrets["firebase_key"]
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to save data to Firebase Firestore
def save_to_firebase(data):
    existing_movie = db.collection("watchlist").where("title", "==", data["title"]).where("poster", "==", data["poster"]).limit(1).get()

    if existing_movie:
        print(f"Movie '{data['title']}' is already in the watchlist.")
        return False
    else:
        # Add data to Firestore if not already present
        db.collection("watchlist").add(data)
        print(f"Document for '{data['title']}' added to Firestore.")
        return True

st.title("Search")

def fetch_movie(title):
    url=f"https://api.themoviedb.org/3/search/movie?api_key=b7fd7209a587422f2b3000c0875d3a95&query={title}"
    data=requests.get(url)
    data=data.json()
    movies = data.get('results', []) 

    movie_list = []
    for movie in movies[:10]:
        movie_id = movie["id"]
        title=movie['title']
        poster_path=movie['poster_path']
        overview=movie["overview"]
        vote=movie["vote_average"]
        trailer_url = fetch_trailer(movie_id)
        if poster_path:
            full_path="https://image.tmdb.org/t/p/w500/"+poster_path
        else:
            full_path = "https://via.placeholder.com/500x750?text=No+Image"
        movie_list.append((title, full_path, overview, vote, trailer_url))
      
    return  movie_list

def fetch_trailer(movie_id):
    """Fetch trailer URL for a given movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=b7fd7209a587422f2b3000c0875d3a95"
    data = requests.get(url).json()
    
    for video in data.get("results", []):
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"  # 
    return None

movie_title = st.text_input("Enter a movie name:")
if movie_title:
    movies = fetch_movie(movie_title)
    if movies:
        st.subheader(f"Results for: **{movie_title}**")
        for index, (title, poster, overview, vote, trailer_url) in enumerate(movies):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(poster, width=200)
            with col2:
                st.write(f"### {title}")
                st.write(f"⭐ Rating: **{vote}**")
                st.write(f"📖 Overview: {overview}")
                if trailer_url:
                    st.markdown(f"[🎬 Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                else:
                    st.write("🚫 No trailer available.")
            with col3:
                if st.button("➕ Add to Watchlist", key=f"watchlist_{index}"):  
                    new_movie = {
                        "title": title,
                        "poster": poster,
                        "vote": vote,
                        "overview": overview,
                        "trailer_url": trailer_url
                    }
                    # Save the new movie to Firestore
                    movie_added = save_to_firebase(new_movie)
                    if movie_added:
                        st.success(f"✅ {title} added to Watchlist!")
                    else:
                        st.warning("🚫 Movie already in Watchlist.")
            st.divider()   
    else:
        st.warning("⚠️ No movies found. Try another title.")
