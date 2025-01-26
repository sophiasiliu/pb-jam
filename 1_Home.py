import streamlit as st
import time
import pandas as pd
import streamlit.components.v1 as components

#page set up with item
st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)
st.title("Welcome to PB & Jam!")


_ABOUT_US = """ A bit about us... like... erm... stuff and... the like? yeah. that sounds legit. """
def stream_data():
    for character in _ABOUT_US:
        yield character 
        time.sleep(0.02)

st.write_stream(stream_data)
st.write("Choose an option below to get started:")

# Buttons for navigation
if st.button("Generate a Playlist Based on Your Mood"):
    # Navigate to the "Generate a Playlist" page
    st.switch_page(page="pages/2_Generate_a_Playlist_Based_on_Your_Mood.py")

if st.button("Find a Song With a Similar Vibe"):
    # Navigate to the "Find a Similar Song" page
    st.switch_page(page="pages/3_Find_a_Song_With_a_Similar_Vibe.py")


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
