import streamlit as st
import time

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


