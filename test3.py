import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load the SBERT model
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# Read data using pandas
movies_df = pd.read_csv('movies_metadata.csv')
credits_df = pd.read_csv('credits.csv')

# Prepare movie descriptions
movies = []

for i, movie in movies_df.iterrows():
    try:
        credit = credits_df.iloc[i]
        
        # Construct the movie description string
        title = movie.get("title", "N/A")
        overview = movie.get("overview", "No description available")
        genres = movie.get("genres", "Unknown")
        runtime = movie.get("runtime", "Unknown")
        
        # Handle the cast and crew from the credits data
        cast = credit.get("cast", "").split(",") if "cast" in credit else []
        cast_str = ", ".join(cast) if cast else "No cast information"
        
        crew = credit.get("crew", "").split(",") if "crew" in credit else []
        director = next((person for person in crew if "Director" in person), "No director info")
        
        # Construct the final description string
        test_str = f"Title: {title} | Description: {overview} | Cast: {cast_str} | Genre: {genres} | Runtime: {runtime} minutes | Director: {director}"
        movies.append(test_str)
        
    except IndexError:
        print(f"Index error at index {i}. Mismatch between movies and credits.")
        break

# Generate embeddings for the combined movie metadata (batch processing)
movie_embeddings = model.encode(movies, batch_size=64, show_progress_bar=True)

# Example watch history (user watched these movies)
user_watched = [
    "Title: Avatar | Description: A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home. | Cast: Sam Worthington, Zoe Saldana | Genre: Action, Adventure, Sci-Fi | Runtime: 162 minutes | Director: James Cameron"
]

# Generate embeddings for the user's watched movies
user_embeddings = model.encode(user_watched, batch_size=64, show_progress_bar=True)

# Create a user profile by averaging the embeddings of the movies they've watched
user_profile = np.mean(user_embeddings, axis=0)

# Use NearestNeighbors for faster similarity computation
knn = NearestNeighbors(n_neighbors=100, metric='cosine', n_jobs=-1)
knn.fit(movie_embeddings)
distances, indices = knn.kneighbors(user_profile.reshape(1, -1))

# Get the top 5 movie recommendations
top_recommendations = [movies[i] for i in indices[0]]

# Print the recommended movies
print("Recommended Movies:")
for movie in top_recommendations:
    print(movie + "\n")