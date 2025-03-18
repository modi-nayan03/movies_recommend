# # import streamlit as st
# # import pickle
# # import pandas as pd

# # # Load the movie data
# # movies_df = pickle.load(open('movies.pkl', 'rb'))  # Load as DataFrame
# # movies_list = movies_df['title'].tolist()  # Extract titles as a list

# # # Load similarity matrix
# # similarity = pickle.load(open('similarity.pkl', 'rb'))

# # def recommend(movie):
# #     # Get index of the selected movie
# #     if movie not in movies_df['title'].values:
# #         return ["Movie not found!"]
    
# #     movie_index = movies_df[movies_df['title'] == movie].index[0]

# #     # Find similar movies
# #     distance = similarity[movie_index]
# #     movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
# #     # Get movie titles
# #     reco_movies = [movies_df.iloc[i[0]]['title'] for i in movies_list]
    
# #     return reco_movies

# # # Streamlit UI
# # st.title('Movie Recommendation System')

# # select_movie_name = st.selectbox(
# #     'Select a movie:',
# #     movies_list  # Use the corrected list
# # )

# # if st.button("Recommend"):
# #     recommendations = recommend(select_movie_name)
# #     for i in recommendations:
# #         st.write(i)

#========================================================================================================================

# import streamlit as st
# import pickle
# import pandas as pd
# import gdown
# import os

# # Google Drive file IDs (Extract from your shared links)
# MOVIES_FILE_ID = pickle.load(open('movies.pkl', 'rb')) # Replace with correct ID
# SIMILARITY_FILE_ID = "1GRFwKbSosqd42APXvT4hR5in719aL_Qm"  # Replace with correct ID


# def download_file_from_drive(file_id, output):
#     url = f"https://drive.google.com/uc?id={file_id}"
#     gdown.download(url, output, quiet=False)


# # Download files if not present
# if not os.path.exists("movies.pkl"):
#     download_file_from_drive(MOVIES_FILE_ID, "movies.pkl")

# if not os.path.exists("similarity.pkl"):
#     download_file_from_drive(SIMILARITY_FILE_ID, "similarity.pkl")

# # Load the movie data
# movies_df = pickle.load(open("movies.pkl", "rb"))  # Load as DataFrame
# movies_list = movies_df["title"].tolist()  # Extract titles as a list

# # Load similarity matrix
# similarity = pickle.load(open("similarity.pkl", "rb"))

# def recommend(movie):
#     # Get index of the selected movie
#     if movie not in movies_df["title"].values:
#         return ["Movie not found!"]
    
#     movie_index = movies_df[movies_df["title"] == movie].index[0]

#     # Find similar movies
#     distance = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
#     # Get movie titles
#     reco_movies = [movies_df.iloc[i[0]]["title"] for i in movies_list]
    
#     return reco_movies

# # Streamlit UI
# st.title("Movie Recommendation System")

# select_movie_name = st.selectbox(
#     "Select a movie:",
#     movies_list
# )

# if st.button("Recommend"):
#     recommendations = recommend(select_movie_name)
#     for i in recommendations:
#         st.write(i)

from flask import Flask, request, render_template
import pickle
import pandas as pd
import gdown
import os

app = Flask(__name__)

# Google Drive file IDs (Replace with correct IDs)
MOVIES_FILE_ID =pickle.load(open('movies.pkl', 'rb'))
SIMILARITY_FILE_ID = "1GRFwKbSosqd42APXvT4hR5in719aL_Qm"  # Replace with actual ID
def download_file_from_drive(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(url, output, quiet=False)
    except Exception as e:
        print(f"Error downloading {output}: {e}")

# Download files if not present
if not os.path.exists("movies.pkl"):
    download_file_from_drive(MOVIES_FILE_ID, "movies.pkl")

if not os.path.exists("similarity.pkl"):
    download_file_from_drive(SIMILARITY_FILE_ID, "similarity.pkl")

# Load the movie data
try:
    with open("movies.pkl", "rb") as f:
        movies_df = pickle.load(f)
        movies_list = movies_df["title"].tolist()
except Exception as e:
    print(f"Error loading movies.pkl: {e}")
    movies_df = pd.DataFrame()
    movies_list = []

# Load similarity matrix
try:
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    print(f"Error loading similarity.pkl: {e}")
    similarity = []

def recommend(movie):
    if movie not in movies_df["title"].values:
        return ["Movie not found!"]
    
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    reco_movies = [movies_df.iloc[i[0]]["title"] for i in movies_list]
    return reco_movies

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    selected_movie = None
    if request.method == "POST" and "movie" in request.form:
        selected_movie = request.form["movie"]
        recommendations = recommend(selected_movie)
    
    return render_template("index.html", movies=movies_list, selected_movie=selected_movie, recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
