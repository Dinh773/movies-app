import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
# Initialize Firebase Admin SDK

if not firebase_admin._apps:
    # Charger les secrets depuis Streamlit
    key_dict = dict(st.secrets["firebase_key"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("My Watchlist")

# Function to get the watchlist from Firestore
def get_watchlist_from_firebase():
    docs = db.collection("watchlist").stream()
    watchlist = []
    for doc in docs:
        movie = doc.to_dict()
        movie["id"] = doc.id  # Store Firestore document ID
        watchlist.append(movie)
    return watchlist

# Function to delete movie from Firestore
def remove_from_firestore(movie_id):
    db.collection("watchlist").document(movie_id).delete()

# Fetch watchlist from Firebase Firestore
watchlist = get_watchlist_from_firebase()

if not watchlist:
    st.warning("Your watchlist is empty.")
else:
    for index, item in enumerate(watchlist):
        title = item.get("title", "Unknown Title")
        poster = item.get("poster", "")
        vote = item.get("vote", "N/A")
        overview = item.get("overview", "No overview available.")
        trailer_url = item.get("trailer_url", "")
        movie_id = item.get("id")  # Fetch Firestore document ID

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if poster.startswith("http"):  
                st.image(poster, width=200)
            else:
                st.warning(f"⚠️ No image available for {title}")        

        with col2:
            st.write(f"### {title}")
            st.write(f"⭐ Rating: **{vote}**")
            st.write(f"📖 Overview: {overview}")
            if trailer_url:
                st.markdown(f"[🎬 Watch Trailer]({trailer_url})", unsafe_allow_html=True)

        with col3:
            if st.button("❌ Remove", key=f"remove_{index}"):
                remove_from_firestore(movie_id)  # Remove movie from Firestore
                st.success(f"✅ {title} removed from Watchlist!")
                st.rerun()

        st.divider()
