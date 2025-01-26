import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components

#page set up with item
st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)

st.title("Welcome to PB & Jam! 🥪🎶")

# Home page description
st.markdown(
    """
    Elevate your earbuds with our delectable mix! \n
    Playlist Bot & Jam (PB & Jam for short) helps find songs based on a carefully curated algo-rhythm.
    Our AI-powered app takes your musical cravings and serves up the perfect playlist or song with the same vibe as your favorite track. \n
    ### Our Recipe:
    - **Song Matching:** Search for a song from our database and we’ll find tracks that hit the same notes.
    - **Mood-Based Songs:** Prompt us anything and we'll find tracks that fit your description.
    \n
"""
)

st.write("Choose an option below to get started:")

# Create columns
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

# Add the PB Button (link) to the first column
with col2:
    st.image("PB.png")
    if st.button("Find Some Jams"):
        st.switch_page(page="pages/3_Find_a_Song_With_a_Similar_Vibe.py")

# Button in the second column
with col4:
    st.image("J.png")
    if st.button("Create Some Jams"):
        st.switch_page(page="pages/2_Create_Your_Own_Jam.py")

# Sidebar image
st.sidebar.image("PJ-main.PNG")

#load dataset
df = pd.read_csv("spotify_songs1.csv", sep=',')
df = df[['track_id', 'track_name', 'track_artist', 'energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].dropna()
df.drop_duplicates(subset = ['track_name', 'track_artist'], inplace = True)

#place subheader, get trackids
st.subheader("Our Available Ingredients:")
trackIDs = list(dict.fromkeys(df['track_id'].values))

#tabs for dataset viewing
tab1, tab2 = st.tabs(["Dataframe View", "Spotify View"])
with tab1:
    #tab for dataset viewing
    st.dataframe(df[["track_name", "track_artist", "energy", "tempo", "danceability", "valence", "instrumentalness"]])
with tab2:
    #tab for spotify viewing
    #set true to have initial 3 songs
    load_more = True

    #set n to 0 if not in session
    if ('n' not in st.session_state):
        st.session_state['n'] = 0

    #if load_more is clicked (or true)
    if(load_more):
        #n = session state
        st.session_state['n'] += 3
        n = st.session_state['n']
        #change existing 3 songs to new dataset (embedded spotify)
        for i in range(n,  n + 3): 
            link = "https://open.spotify.com/embed/track/" + str(trackIDs[i])
            iframe_src = link
            components.iframe(iframe_src, height=175, scrolling=True)

    #place load (under songs)
    load_more = st.button("Load More", type="secondary", icon=':material/refresh:', use_container_width=True)
    
