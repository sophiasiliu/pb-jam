import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components
import openai
import os
import traceback
import re
import numpy as np

st.set_page_config(
    page_title="PB & Jam",
    page_icon="🍞",
)

st.title("Create Your Own Jam")

df = pd.read_csv("spotify_songs1.csv", sep=',')
df = df[['track_id', 'track_name', 'track_artist', 'energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].dropna()
df.drop_duplicates(subset = ['track_name', 'track_artist'], inplace = True)
X = df[['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_feature_estimates(prompt):
    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content.strip()
        #print(f"Raw GPT-3 Response: {response}")  # Print raw response for debugging
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def parse_features(response):
    features = {}

    feature_pattern = r"(energy|tempo|danceability|valence|instrumentalness)\s*[:=]?\s*([0-1](?:\.\d*)?)"

    matches = re.findall(feature_pattern, response, flags=re.IGNORECASE)
    #st.write(matches)
    if matches:
        for feature, value in matches:
            features[feature.lower()] = float(value)
    else:
        print(traceback.format_exc())
        return {"error": traceback.format_exc()}
    return features

user_input = st.text_area("Describe the jam you'd like!")

if st.button("Get my playlist"):
    if user_input.strip():
        prompt = f"Given the song description '{user_input}', estimate the following song features as a range between 0 and 1: energy, tempo, danceability, valence, instrumentalness."

        gpt_response = get_feature_estimates(prompt)
        #print(gpt_response)

        feature_values = parse_features(gpt_response)

        if "error" in feature_values:
            st.error(feature_values["error"])
        else:
            songvector = [np.array([
                        np.float64(feature_values.get('energy', 'N/A')),
                        np.float64(feature_values.get('tempo', 'N/A') * 240),
                        np.float64(feature_values.get('danceability', 'N/A')),
                        np.float64(feature_values.get('valence', 'N/A')),
                        np.float64(feature_values.get('instrumentalness', 'N/A'))
                    ], dtype=object)
                ]
            similarityScores = cosine_similarity(songvector, X)
            similarIndices = similarityScores.argsort()[0][::-1]
            topN = 10

            if ('n' not in st.session_state):
                st.session_state['n'] = -9

            if ('topN' not in st.session_state):
                st.session_state['topN'] = 0

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
    else:
        st.warning("Please enter a jam description.")
