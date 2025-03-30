import csv
import ast

with open('movies_metadata.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    movies_dict = [row for row in csv_reader]

x = 0
genres_set = set()  # To store unique genres
genres = ""

while x < len(movies_dict):  # Ensure you don't go out of bounds
    genre_list = ast.literal_eval(movies_dict[x]["genres"])
    for i, genre in enumerate(genre_list):
        if genre['name'] not in genres_set:  # Only add unique genres
            genres_set.add(genre['name'])
            genres += genre['name']
            # Add ", " if it's not the last genre in the list
            if i != len(genre_list) - 1:
                genres += ", "
    x += 1

print(genres)
