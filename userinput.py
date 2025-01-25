import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


df= pd.read_csv("spotify_songs.csv").dropna()
#unique_tracks = [df['track_name'].drop_duplicates().reset_index(drop=True)]

df.drop_duplicates(subset = ['track_name'], inplace = True)

X = df[['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values

song = "She Looks So Perfect" #input("Enter song name: ")
artist = "5 Seconds of Summer" #input("Enter song artist: ")
#trackexists = ((df['track_name'] == song) & (df['track_artist'] == artist)).any()

songfeatures = df[(df['track_name'].str.lower() == song.lower()) & (df['track_artist'].str.lower() == artist.lower())][["track_name", "track_artist", "energy", "tempo", "danceability", "valence", "instrumentalness"]].head(1)

if songfeatures.empty:
    raise Exception("Still cooking, stay tuned!")
else:
    songvector = [songfeatures.iloc[0][['energy', 'tempo', 'danceability', 'valence', 'instrumentalness']].values]
    similarityScores = cosine_similarity(songvector, X)
    similarIndices = similarityScores.argsort()[0][::-1]
    topN = 20
    topSongs = df.iloc[similarIndices[1:topN+1]]
    print(topSongs)
    trackIDs = list(dict.fromkeys(topSongs['track_id'].values))
    links = []
    for trackID in trackIDs:
        link = 'https://open.spotify.com/track/' + str(trackID)
        print(link)
        links.append(link)
