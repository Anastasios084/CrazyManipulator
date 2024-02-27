# import json

# file1 = "./bulk_data/crazy1UTF8.json"
# file2 = "./bulk_data/crazy2UTF8.json"
# file3 = "./bulk_data/crazy3UTF8.json"


# This file actually get all the json files in the bulk data folder and merges the json files to one  big json file.
import os
import json
import codecs  # Import the codecs library

def concatenate_json_files(directory, output_file):
    # Initialize an empty list to hold the combined data
    combined_data = []

    # Loop through every file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(directory, filename)  # Get the full path of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Load the JSON data from the file
                if isinstance(data, list):  # Check if the JSON data is a list
                    combined_data.extend(data)  # Add the data to the combined list
                else:
                    print(f"Warning: The file {filename} does not contain a JSON array.")
    
    with codecs.open(output_file, 'w', encoding='utf-8', errors='ignore') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
# Usage example
directory = """C:\\Users\\tasar\\Desktop\\Random projects\\crazytime manipulator\\bulk _data""" ############ FIX PATH
output_file = 'combined_data.json'
concatenate_json_files(directory, output_file)