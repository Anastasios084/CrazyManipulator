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

def create_df(json_data_path):
    column_names = ['id', 'totalWinners', 'totalAmount', "winners","startedAt", "settledAt", "status", "gameType", "currency", "wager", "payout", "dealerName", "dealerUid", "numOfParticipants", "topSlot_WheelSector", "topSlot_Multi", "resultType", "resultSector", "bonusType", "bonusMultiplier","cashMinMulti", "coinColor", "flapperGreen", "flapperBlue", "flapperYellow","maxMulti", "isTopSlotMatched"]

    df = pd.DataFrame(columns=column_names)

    file_path = json_data_path
    # Now, try to load the JSON from the new file
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)  # This should now work without errors

    i = 0

    for js in json_data:
        # create empty row
        df.loc[len(df)] = [None] * len(df.columns)
        # set ID
        df.loc[len(df)-1, 'id'] = js['id']
        # set Transmission ID
        # df.loc[len(df)-1, 'trans_id'] = js['transmissionId']
        # TRY to get total winners
        try:
            df.loc[len(df)-1, 'totalWinners'] = js['totalWinners']
        except:
            df.loc[len(df)-1, 'totalWinners'] = -1
        
        # TRY to get total amount
        try:
            df.loc[len(df)-1, 'totalAmount'] = js['totalAmount']
        except:
            df.loc[len(df)-1, 'totalAmount'] = -1

        # TRY to get top 5 winnings
        try:
            # Assuming json_data is your main JSON dictionary
            winners_list = js["winners"]

            # Extract the winnings
            winnings_array = [winner["winnings"] for winner in winners_list]
            # print(winnings_array)
            df.at[len(df)-1, 'winners'] = winnings_array  # Encapsulate winnings_array in another list
        except:
            df.at[len(df)-1, 'winners'] = []
        
        # get dataID
        # df.loc[len(df)-1, 'dataID'] = js['data']['id']
        df.loc[len(df)-1, 'startedAt'] = js['data']['startedAt']
        df.loc[len(df)-1, 'settledAt'] = js['data']['settledAt']
        df.loc[len(df)-1, 'status'] = js['data']['status']
        df.loc[len(df)-1, 'gameType'] = js['data']['gameType']
        df.loc[len(df)-1, 'currency'] = js['data']['currency']
        try:
            df.loc[len(df)-1, 'wager'] = js['data']['wager']
        except:
            df.loc[len(df)-1, 'wager'] = -1
        
        try:
            df.loc[len(df)-1, 'payout'] = js['data']['payout']
        except:
            df.loc[len(df)-1, 'payout'] = -1

        try:
            df.loc[len(df)-1, 'dealerName'] = js['data']['dealer']['name']
        except:
            df.loc[len(df)-1, 'dealerName'] = "Unknown"

        try:
            df.loc[len(df)-1, 'dealerUid'] = js['data']['dealer']['uid']
        except:
            df.loc[len(df)-1, 'dealerUid'] = "Unknown"

        df.loc[len(df)-1, 'numOfParticipants'] = js['data']['numOfParticipants']
        df.loc[len(df)-1, 'topSlot_WheelSector'] = js['data']['result']['outcome']['topSlot']['wheelSector']
        try:
            df.loc[len(df)-1, 'topSlot_Multi'] = js['data']['result']['outcome']['topSlot']['multiplier']
        except:
            df.loc[len(df)-1, 'topSlot_Multi'] = 1
        df.loc[len(df)-1, 'resultType'] = js['data']['result']['outcome']['wheelResult']['type']
        df.loc[len(df)-1, 'resultSector'] = js['data']['result']['outcome']['wheelResult']['wheelSector']

        ################################################################################################################## EDW KSEKINAEI TO FUCKFEST
        # "bonusType", "bonusMultiplier","cashMinMulti", "coinColor", "flapperGreen", "flapperBlue", "flapperYellow", "maxMulti", "isTopSlotMatched"
        if js['data']['result']['outcome']['wheelResult']['type'] == "BonusRound":
            bonusType = js['data']['result']['outcome']['wheelResult']['bonus']['type']
            df.loc[len(df)-1, 'bonusType'] = bonusType

            if bonusType == "Pachinko":
                df.loc[len(df)-1, 'bonusMultiplier'] = js['data']['result']['outcome']['wheelResult']['bonus']['bonusMultiplier']['value']
            elif bonusType == "CashHunt":
                df.at[len(df)-1, 'bonusMultiplier'] = js['data']['result']['outcome']['wheelResult']['bonus']['bonusMultipliers']
                df.at[len(df)-1, 'cashMinMulti'] = js['data']['result']['outcome']["cashHuntMinMultiplier"]
            elif bonusType == "CoinFlip":
                df.loc[len(df)-1, 'bonusMultiplier'] = js['data']['result']['outcome']['wheelResult']['bonus']['result']['multiplier']
                df.loc[len(df)-1, 'coinColor'] = js['data']['result']['outcome']['wheelResult']['bonus']['result']['color']
            elif bonusType == "CrazyBonus":
                df.loc[len(df)-1, 'flapperGreen'] = js['data']['result']['outcome']['wheelResult']['bonus']['flapperResult']['left']['bonusMultiplier']
                df.loc[len(df)-1, 'flapperBlue'] = js['data']['result']['outcome']['wheelResult']['bonus']['flapperResult']['top']['bonusMultiplier']
                df.loc[len(df)-1, 'flapperYellow'] = js['data']['result']['outcome']['wheelResult']['bonus']['flapperResult']['right']['bonusMultiplier']

            
        df.at[len(df)-1, 'maxMulti'] = js['data']['result']['outcome']["maxMultiplier"]
        df.at[len(df)-1, 'isTopSlotMatched'] = js['data']['result']['outcome']["isTopSlotMatchedToWheelResult"]



        i += 1

        if(i%100 == 0):
            print(i)


    # print(df)
    unique_count = df['id'].nunique()
    print(f"Number of unique values in the column: {unique_count}")
    return df

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
def get_inference_data(size):
    current_id = ""

    url = 'https://api.casinoscores.com/svc-evolution-game-events/api/crazytime?size={size}&tableId=CrazyTime0000001'
    json_data = get_json_from_url(url)
    if json_data:
        # Construct the filename with the current datetime
        filename = "./inference/inference_data.json"
        # Save the data to a JSON file with the generated filename
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        # print(json.dumps(json_data, indent=4))


    directory = "./inference"
    output_file = './inference/inference_data.json'
    concatenate_json_files(directory, output_file)


    file_path = "./inference/inference_data.json"
    # Now, try to load the JSON from the new file
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)  # This should now work without errors



    file_path = "./inference/inference_data.json"
    df = create_df(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Combined jsons removed successfully")
    else:
        print("There are no  combined jsons to remove.")


    return df



print(get_inference_data(10))