# api.casinoscores.com/svc-evolution-game-events/api/crazytime/latest?tableId=CrazyTime0000001
# api.casinoscores.com/svc-evolution-game-events/api/crazytime

import requests
import json
import datetime
from time import sleep
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

# Replace 'your_api_endpoint_url' with the actual URL you want to send the request to
url = 'https://api.casinoscores.com/svc-evolution-game-events/api/crazytime/latest?tableId=CrazyTime0000001'
current_id = ""
while True:
    json_data = get_json_from_url(url)
    if json_data:
        if current_id == json_data['id']: # check if a new incident has occured
            sleep(3)
            continue
        else:
            current_id = json_data['id']
        # Get the current datetime and format it as a string suitable for filenames
        # Format: YYYY-MM-DD_HH-MM-SS
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Construct the filename with the current datetime
        filename = f"./real_time_data/data_{datetime_str}.json"
        # Save the data to a JSON file with the generated filename
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(json.dumps(json_data, indent=4))
        sleep(3)
