
# Original API response

import requests 
import json 
from datetime import datetime, timezone


API_URL = "https://api.railinfo.uk/boards/RDG/departures?limit=5"

# fetch api repsonse and catch any errors 
def extract_departures():
    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    return response.json()

# add some metadata using python to json response 
def main():
    data = extract_departures()

    output = {
        "station_code": "RDG",
        "station_name": "Reading",
        "extracted_at": datetime.now(timezone.utc).isoformat(),         # time of extraction based on when data is ingested
        "departures": data
    }
# create and keep json file containing data from api as raw data 
    with open("data/raw/reading_departures.json", "w") as file:
        json.dump(output, file, indent=2)

    print("Extraction complete.")
    print("Saved to data/raw/reading_departures.json")


if __name__ == "__main__":
    main()


