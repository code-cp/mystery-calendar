import json
import pathlib
import random 

current_dictionary = pathlib.Path(__file__).parent.resolve()

def load_one_entry(load_randomly=False):
    # Example usage:
    file_path = current_dictionary / '../database.json'  # Path to your JSON file

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    idx = -1
    if load_randomly:
        idx = random.randint(0, len(json_data)-1)

    entry = json_data[idx]
        
    return entry 
