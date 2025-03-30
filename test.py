from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the SBERT model
#model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2', device='cuda')

# Example movie metadata

import csv

# Read movies metadata
with open('movies_metadata.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    movies_dict = [row for row in csv_reader]

# Read credits
with open('credits.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    credits = [row for row in csv_reader]

movies = []

# Loop through both lists and create the movie description strings
for i in range(len(movies_dict)):
    try:
        # Ensure we don't go out of bounds
        movie = movies_dict[i]
        credit = credits[i]
        
        # Construct the movie description string
        title = movie.get("title", "N/A") if movie.get("title") else "N/A"
        overview = movie.get("overview", "No description available") if movie.get("overview") else "No description available"
        genres = movie.get("genres", "Unknown") if movie.get("genres") else "Unknown"
        runtime = movie.get("runtime", "Unknown") if movie.get("runtime") else "Unknown"
        
        # Handle the cast and crew from the credits data
        cast = credit.get("cast", "").split(",") if "cast" in credit else []
        cast_str = ", ".join(cast) if cast else "No cast information"
        
        crew = credit.get("crew", "").split(",") if "crew" in credit else []
        director = next((person for person in crew if "Director" in person), "No director info")
        
        # Construct the final description string
        test_str = f"Title: {title} | Description: {overview} | Cast: {cast_str} | Genre: {genres} | Runtime: {runtime} minutes | Director: {director}"
        movies.append(test_str)
        
    except IndexError:
        print(f"Index error at index {i}. There might be a mismatch between movies and credits data.")
        break  # Exit the loop if there is an index error.



# Generate embeddings for the combined movie metadata
#movie_embeddings = model.encode(movies)

# Example watch history (user watched these movies)
user_watched = [
    "Title: Avatar | Description: A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home. | Cast: Sam Worthington, Zoe Saldana | Genre: Action, Adventure, Sci-Fi | Runtime: 162 minutes | Director: James Cameron"
]
movie_embeddings = model.encode(movies)

# Generate embeddings for the user's watched movies
user_embeddings = model.encode(user_watched)

# Create a user profile by averaging the embeddings of the movies they've watched
user_profile = np.mean(user_embeddings, axis=0)

# Calculate cosine similarity between the user profile and all movie embeddings
similarities = cosine_similarity([user_profile], movie_embeddings)

# Get the indices of the top 5 most similar movies
top_movie_indices = similarities.argsort()[0][-7:][::-1]

# Get the top 5 movie recommendations
top_recommendations = [movies[i] for i in top_movie_indices]

# Print the recommended movies, each on a new line
# Print the recommended movies with a new line between each movie
print("Recommended Movies:")
for movie in top_recommendations:
    print(movie + "\n")  # Adds a newline after each movie