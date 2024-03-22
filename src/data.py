import json
import pathlib
import random 

current_dictionary = pathlib.Path(__file__).parent.resolve()

# Define a function to load the JSON file
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        for entry in json_data:
            # Extract data from each entry, handling missing values
            web_url = entry.get('web_url')
            image_url = entry.get('image_url')
            imdb_score = entry.get('imdb_score')
            tomato_score = entry.get('tomato_score')
            review = entry.get('review')
            
            # Append the data as a tuple
            data.append((web_url, image_url, imdb_score, tomato_score, review))
    
    return data

def load_one_entry(load_randomly=False):
    # Example usage:
    file_path = current_dictionary / '../data.json'  # Path to your JSON file
    loaded_data = load_data(file_path)

    idx = -1
    if load_randomly:
        idx = random.randint(0, len(loaded_data)-1)

    entry = loaded_data[idx]
    return entry 
