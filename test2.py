import csv
import ast

def ft_dict_to_string(in_dict):
    genre_list = ast.literal_eval(in_dict)
    genres = ""
    for i,genre in enumerate(genre_list):
        genres += genre['name']
        if genre != len(genre_list) - 1:
            genres += ", "
    return genres

with open('movies_metadata.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    movies_dict = [row for row in csv_reader]

with open('credits.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    credits = [row for row in csv_reader]

with open('keywords.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    keywords = [row for row in csv_reader]

genres = ft_dict_to_string(movies_dict[1]["genres"])
kw = ft_dict_to_string(keywords[1]["keywords"])
cast = ft_dict_to_string(credits[1]["cast"])
crew = ft_dict_to_string(credits[1]["crew"])
produ_comp = ft_dict_to_string(movies_dict[1]["production_companies"])
languages = ft_dict_to_string(movies_dict[1]["spoken_languages"])

#data = [
#    {'name': movies_dict[1]["title"], 'genres': genres}
#]

#with open('university_records.csv', 'w', newline='') as csvfile:
#    fieldnames = ['name', 'genres']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#    writer.writeheader()
#    writer.writerows(data)

print(movies_dict[1])
print("\n\n\n\n")

print(movies_dict[1]["title"])
print(genres)
print(movies_dict[1]["overview"])
print(kw)
print(cast)
print(crew)
print(produ_comp)
print(movies_dict[1]["release_date"])
print(movies_dict[1]["runtime"])
print(languages)