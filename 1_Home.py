import streamlit as st
import os
import pandas as pd
import streamlit.components.v1 as components

#page set up with item
st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)

st.title("Welcome to PB & Jam!")

# Home page description
st.markdown(
    """
    Elevate your earbuds with our delectable mix! \n
    Playlist Bot & Jam (PB & Jam for short) helps find songs based on a carefully curated algo-rhythm.
    Our AI-powered app takes your musical cravings and serves up the perfect playlist or song with the same vibe as your favorite track. \n
    ### Our Recipe:
    - 🎧 **Song Matching:** Search for a song from our database and we’ll find tracks that hit the same notes.
    - 🎵 **Mood-Based Songs:** Prompt us anything and we'll find tracks that fit your description.
    \n
"""
)

st.write("Choose an option below to get started:")

# Create empty columns on the sides and use the center columns for the buttons
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])  # Adjust ratios for centering

# Buttons in the center
with col2:
    st.image("PB.png")
    if st.button("Find Some Jams"):
        # Navigate to the "Find a Similar Song" page
        st.switch_page(page="pages/4_Find_Some_Jams.py")

with col4:
    st.image("J.png")
    if st.button("Create Your Own Jam"):
        # Navigate to the "Create Your Own Jam" page
        st.switch_page(page="pages/3_Create_Your_Own_Jam.py")

# Sidebar image
st.sidebar.image("PJ-main.PNG")

