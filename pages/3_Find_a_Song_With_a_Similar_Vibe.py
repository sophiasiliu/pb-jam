import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)

st.title("Find a Song With a Similar Vibe")

df= pd.read_csv("spotify_songs.csv").dropna()
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

    if ('n' not in st.session_state):
        st.session_state['n'] = -9

    if ('topN' not in st.session_state):
        st.session_state['topN'] = 0
    
    refresh = st.button("refresh", type="secondary", icon=':material/refresh:', use_container_width=True)
    if (refresh):
        #st.balloons()
        st.session_state['n'] += 10
        n = st.session_state['n']
        st.session_state['topN'] += 10
        topN = st.session_state['topN']
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
        #st.toast('Done!',icon=':material/check_box:')
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Energy", "Tempo", "Danceability", "Valence", "Instrumentalness"])
        with tab1:
            fig = px.scatter(topSongs,x='track_name',y="energy")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab2:
            fig = px.scatter(topSongs,x='track_name',y="tempo")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab3:
            fig = px.scatter(topSongs,x='track_name',y="danceability")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab4:
            fig = px.scatter(topSongs,x='track_name',y="valence")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab5:
            fig = px.scatter(topSongs,x='track_name',y="instrumentalness")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
