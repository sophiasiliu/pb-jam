import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import streamlit.components.v1 as components



st.title("Welcome to PB & Jam!")

df= pd.read_csv("spotify_songs.csv").dropna()
#unique_tracks = [df['track_name'].drop_duplicates().reset_index(drop=True)]

df.drop_duplicates(subset = ['track_name'], inplace = True)

X = df[['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values

song = "Shake It Off" #input("Enter song name: ")
artist = "Taylor Swift" #input("Enter song artist: ")
#trackexists = ((df['track_name'] == song) & (df['track_artist'] == artist)).any()

songfeatures = df[(df['track_name'].str.lower() == song.lower()) & (df['track_artist'].str.lower() == artist.lower())][["track_name", "track_artist", "energy", "tempo", "danceability", "valence", "instrumentalness"]].head(1)

if songfeatures.empty:
    st.subheader("We're still cooking, stay tuned!")
else:
    songvector = [songfeatures.iloc[0][['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values]
    similarityScores = cosine_similarity(songvector, X)
    similarIndices = similarityScores.argsort()[0][::-1]
    topN = 10
    n = 1
    while True: 
        topSongs = df.iloc[similarIndices[n:topN+1]]
        print(topSongs)
        songNames = list(dict.fromkeys(topSongs['track_name'].values))
        artistNames = list(dict.fromkeys(topSongs['track_artist'].values))
        trackIDs = list(dict.fromkeys(topSongs['track_id'].values))
        st.subheader("Playlist Bot: Here's your jam, enjoy!")
        for i in range(len(trackIDs)):
            link = "https://open.spotify.com/embed/track/" + str(trackIDs[i])
            iframe_src = link
            components.iframe(iframe_src, height=175, scrolling=True)
        refresh = st.button("refresh")
        if not refresh: 
            break
        else:
            n = 11
