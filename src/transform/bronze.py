
# Bronze.py = preserve and structure the source.
# Minimal transformation

import json
from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/reading_departures.json")
BRONZE_FILE = Path("data/bronze/reading_departures.parquet")


# edit the raw json file and then return 
def load_raw_data():
    with open(RAW_FILE, "r") as file:
        return json.load(file)



# copy data from json into pandas dataframe(temporary table) 
def transform_to_bronze(data):
    board = data["departures"]          # board goes into list in departures in departures in the json file 

    departures = board["departures"]        # then create variable 'departures' variable on top of the board variable 

    rows = []

# loop through 'departures' copy each row in function and edit row names to bring all need rows together from nested list/dictionaries across the whole json file 

        # Train-level data
        #       +
        # Board-level metadata
        #       +
        # Our ingestion metadata

    for departure in departures:
        row = departure.copy()

        row["station_code"] = board["crs"]
        row["station_name"] = board["name"]
        row["service_date"] = board["date"]
        row["source"] = board["source"]
        row["kind"] = board["kind"]
        row["extracted_at"] = data["extracted_at"]

        rows.append(row)

    return pd.DataFrame(rows)



# save dataframe as parquet as 'BRONZE_FILE' 
def save_bronze(df):
    BRONZE_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        BRONZE_FILE,
        index=False
    )


def main():
    data = load_raw_data()          # first:  function under variable 

    df = transform_to_bronze(data)      # second:  function under transformation 

    save_bronze(df)                         # third:  function to save as BRONZE_FILE 

    print(f"Bronze file created: {BRONZE_FILE}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()

# If successful once ran: Notice we didn't have to force the API into the schema we expected. 
# We inspect the actual response and adapted the pipeline -> ETL thinking.