from openai import OpenAI
import openai
import os
import traceback

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
import re

def get_feature_estimates(prompt):
    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content.strip()
        print(f"Raw GPT-3 Response: {response}")  # Print raw response for debugging
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def parse_features(response):
    features = {}

    feature_pattern = r"(energy|danceability|valence|tempo|instrumentalness)\s*[:=]?\s*([0-1](?:\.\d*)?)"

    matches = re.findall(feature_pattern, response, flags=re.IGNORECASE)
    st.write(matches)
    if matches:
        for feature, value in matches:
            features[feature.lower()] = float(value)
    else:
        print(traceback.format_exc())
        return {"error": traceback.format_exc()}
    return features
st.title("Song Feature Estimation with OpenAI GPT-3")

user_input = st.text_area("Describe a song (e.g., its mood, tempo, or feel)")

if st.button("Get Song Features"):
    if user_input.strip():
        prompt = f"Given the song description '{user_input}', estimate the following song features as a range between 0 and 1: energy, danceability, valence, tempo, instrumentalness."

        gpt_response = get_feature_estimates(prompt)
        print(gpt_response)

        feature_values = parse_features(gpt_response)

        if "error" in feature_values:
            st.error(feature_values["error"])
        else:
            st.subheader("Estimated Song Features")
            st.write(f"**Energy**: {feature_values.get('energy', 'N/A')}")
            st.write(f"**Danceability**: {feature_values.get('danceability', 'N/A')}")
            st.write(f"**Valence**: {feature_values.get('valence', 'N/A')}")
            st.write(f"**Tempo**: {feature_values.get('tempo', 'N/A')}")
            st.write(f"**Instrumentalness**: {feature_values.get('instrumentalness', 'N/A')}")
    else:
        st.warning("Please enter a song description.")

