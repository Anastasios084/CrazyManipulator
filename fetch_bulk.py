# api.casinoscores.com/svc-evolution-game-events/api/crazytime/latest?tableId=CrazyTime0000001
# api.casinoscores.com/svc-evolution-game-events/api/crazytime

import requests
import json
import os
import codecs  # Import the codecs library
from time import sleep
import shutil
import re
import pandas as pd
from aux_df import *
def get_json_from_url(url):
    # Send a GET request to the specified URL
    try:
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else {err}")
    else:
        # Parse the response JSON
        try:
            data = response.json()
            return data
        except json.JSONDecodeError:
            print("Error: Could not parse JSON")

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


# Replace 'your_api_endpoint_url' with the actual URL you want to send the request to

current_id = ""
while True:
    for i in range(3):
        url = 'https://api.casinoscores.com/svc-evolution-game-events/api/crazytime?size=40000&duration=60000&page={i}&tableId=CrazyTime0000001'
        json_data = get_json_from_url(url)
        if json_data:
            # Construct the filename with the current datetime
            filename = "./bulk_data/"+str(i)+".json"
            # Save the data to a JSON file with the generated filename
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=4)
            # print(json.dumps(json_data, indent=4))


    directory = "./bulk_data"
    output_file = './bulk_data/combined_data.json'
    concatenate_json_files(directory, output_file)

    # open current csv file
    df = pd.read_csv("crazy.csv")
    df.to_csv("crazyBACKUP.csv", index=False)
    file_path = "./bulk_data/combined_data.json"
    # Now, try to load the JSON from the new file
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)  # This should now work without errors

    fill_df(df, json_data)

    # # Define the source and destination directories
    # source_dir = './bulk_data'
    # destination_dir = './bulk_data_USED'

    # # Find the highest number used in the destination filenames
    # highest_num = 0
    # for filename in os.listdir(destination_dir):
    #     match = re.search(r'crazy(\d+)UTF8\.json', filename)
    #     if match:
    #         num = int(match.group(1))
    #         if num > highest_num:
    #             highest_num = num

    # # Move and rename files from the source to the destination directory
    # for filename in os.listdir(source_dir):
    #     # Check if it is a file (and not a directory)
    #     source_path = os.path.join(source_dir, filename)
    #     if os.path.isfile(source_path):
    #         # Increment the highest number for the new filename
    #         highest_num += 1
    #         new_filename = f'crazy{highest_num}UTF8.json'
    #         destination_path = os.path.join(destination_dir, new_filename)
            
    #         # Move and rename the file
    #         shutil.move(source_path, destination_path)
    #         print(f'Moved and renamed: {source_path} to {destination_path}')
    file_path = "./bulk_data/combined_data.json"
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Combined jsons removed successfully")
    else:
        print("There are no  combined jsons to remove.")

    print("Sleeping for 10 minutes...")
    sleep(600)
