import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px #need to pip install plotly

#page set up with icon
st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)
st.title("Find a Song With a Similar Vibe")

#dataset from new csv file
df = pd.read_csv("/Users/sophiasliu/Downloads/QHacks/pages/spotify_songs1.csv", sep=',')
df = df[['track_id', 'track_name', 'track_artist', 'Popularity', 'energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].dropna()
df.drop_duplicates(subset = ['track_name', 'track_artist'], inplace = True)
X = df[['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values

#get song as user input
song = st.selectbox(label='Input Your Song Here!', options=df[['track_name']], index=None)

#for when the user hasn't input anything, playlist button
if song == None:
    refresh = st.button("create new playlist", type="secondary", icon=':material/refresh:', use_container_width=True)
else:
    #create songfeatures for user input
    songfeatures = df[(df['track_name'].str.lower() == song.lower())][["track_name", "track_artist", "energy", "tempo", "danceability", "valence", "instrumentalness"]].head(1)

    #if songfeatures empty, display loading message
    if songfeatures.empty:
        st.subheader("We're still cooking, stay tuned!")
    else:
        #obtain info and compolete cosine comparision
        songvector = [songfeatures.iloc[0][['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values]
        similarityScores = cosine_similarity(songvector, X)
        similarIndices = similarityScores.argsort()[0][::-1]

        #if not in state, set to negative (before user interaction)
        if ('n' not in st.session_state):
            st.session_state['n'] = -9
        #if not in state, set to 0 (before user interaction)
        if ('topN' not in st.session_state):
            st.session_state['topN'] = 0
        
        #create playlist button again
        refresh = st.button("create new playlist", type="secondary", icon=':material/refresh:', use_container_width=True)
        #if clicked
        if (refresh):
            #st.balloons()
            #for each click of refresh, add 10 to n and topN (to cycle through new songs)
            st.session_state['n'] += 10
            n = st.session_state['n']
            st.session_state['topN'] += 10
            topN = st.session_state['topN']

            #top n songs from cosine comparision
            topSongs = df.iloc[similarIndices[n:topN+1]]
            #define vars (may not be needed)
            songNames = list(dict.fromkeys(topSongs['track_name'].values))
            artistNames = list(dict.fromkeys(topSongs['track_artist'].values))
            trackIDs = list(dict.fromkeys(topSongs['track_id'].values))

            #display playlist
            st.subheader("Playlist Bot: Here's your jam, enjoy!")
            #loop through given ids for cosine similar topN songs, and embed them with spotify
            for i in range(len(trackIDs)):
                link = "https://open.spotify.com/embed/track/" + str(trackIDs[i])
                iframe_src = link
                components.iframe(iframe_src, height=175, scrolling=True)
            #st.toast('Done!',icon=':material/check_box:')

            #display visual representation of cosine comparision (eg. energy for each song given)
            st.subheader("Our Secret Recipe for Your Jam:")
            #tabs to switch between representations (like switch statement)
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Energy", "Tempo", "Danceability", "Valence", "Instrumentalness"])
            with tab1:
                #figure for energy
                fig = px.scatter(topSongs,x='track_name',y="energy", color="Popularity", labels={"track_name": "Track Name", "energy": "Energy", "playlist_genre": "Playlist Genre"})
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                #figure for tempo
                fig = px.scatter(topSongs,x='track_name',y="tempo", color="Popularity", labels={"track_name": "Track Name", "tempo": "Tempo", "playlist_genre": "Playlist Genre"})
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab3:
                #figure for danceability
                fig = px.scatter(topSongs,x='track_name',y="danceability", color="Popularity", labels={"track_name": "Track Name", "danceability": "Danceability", "playlist_genre": "Playlist Genre"})
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab4:
                #figure for valence
                fig = px.scatter(topSongs,x='track_name',y="valence", color="Popularity", labels={"track_name": "Track Name", "valence": "Valence", "playlist_genre": "Playlist Genre"})
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab5:
                #figure for intrumentalness
                fig = px.scatter(topSongs,x='track_name',y="instrumentalness", color="Popularity", labels={"track_name": "Track Name", "instrumentalness": "Instrumentalness", "playlist_genre": "Playlist Genre"})
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# Sidebar image
st.sidebar.image("PJ-main.PNG")
