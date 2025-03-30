from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv
import torch

# Check if CUDA is available, fallback to CPU if not
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load SBERT model once and keep it in memory
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2", device=device)

# Loads and processes movie metadata and credits to create structured descriptions.
def load_movie_data(movies_file="movies_metadata.csv", credits_file="credits.csv"):
    with open(movies_file, mode="r") as file:
        movies_dict = [row for row in csv.DictReader(file)]
    with open(credits_file, mode="r") as file:
        credits = [row for row in csv.DictReader(file)]
    movies = []
    min_length = min(len(movies_dict), len(credits))
    for i in range(min_length):
        movie = movies_dict[i]
        credit = credits[i]
        title = movie.get("title", "N/A") or "N/A"
        overview = movie.get("overview", "No description available") or "No description available"
        genres = movie.get("genres", "Unknown") or "Unknown"
        runtime = movie.get("runtime", "Unknown") or "Unknown"
        cast = credit.get("cast", "").split(",") if "cast" in credit else []
        cast_str = ", ".join(cast) if cast else "No cast information"
        crew = credit.get("crew", "").split(",") if "crew" in credit else []
        director = next((person for person in crew if "Director" in person), "No director info")
        movie_str = f"Title: {title} | Description: {overview} | Cast: {cast_str} | Genre: {genres} | Runtime: {runtime} minutes | Director: {director}"
        movies.append(movie_str)

    return movies


def recommend_movies(user_watched, movies, top_n=5):
    """Generates movie recommendations excluding already watched movies."""
    movie_embeddings = model.encode(movies, convert_to_tensor=True, device=device)
    user_embeddings = model.encode(user_watched, convert_to_tensor=True, device=device)
    user_profile = torch.mean(user_embeddings, dim=0).unsqueeze(0)
    similarities = cosine_similarity(user_profile.cpu().numpy(), movie_embeddings.cpu().numpy())
    watched_set = set(user_watched)
    sorted_indices = similarities.argsort()[0][::-1]
    filtered_recommendations = [movies[i] for i in sorted_indices if movies[i] not in watched_set]
    return filtered_recommendations[:top_n]


if __name__ == "__main__":
    user_watched = []
    movies = load_movie_data()
    for i in range(len(movies)):
        if "Title: Avatar" in movies[i]:
            user_watched.append(movies[i])
        if "Title: Interstellar" in movies[i]:
            user_watched.append(movies[i])
    user_unliked = []
    #for i in range(len(user_watched)):
    #    print("\n")
    #    print (user_watched[i])
    #    print("\n")
    #exit (1)
    while True:
        arr = user_unliked + user_watched
        recommendations = recommend_movies(arr , movies, top_n=7)
        print("\nRecommended Movies:")
        for movie in recommendations:
            print(movie)
            cont = input("Add again?(y/n): \n").strip().lower()
            if cont == "y":
                user_watched.append(movie)
            else:
                user_unliked.append(movie)
        cont = input("Run again? (y/n): ").strip().lower()
        if cont != "y":
            break