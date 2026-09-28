
# We're checking things such as:

# Are essential fields missing?
# Are train IDs duplicated?
# Are delay values behaving as expected?
# How many services are cancelled?


# Validation rule needs to understand the meaning of the data, not just flag unusual values.

import pandas as pd

BRONZE_FILE = "data/bronze/reading_departures.parquet"


def main():
    df = pd.read_parquet(BRONZE_FILE)

    print("=== Bronze Validation ===")

    print(f"Row count: {len(df)}")

    print(f"Missing station codes: {df['station_code'].isna().sum()}")

    print(f"Missing operators: {df['operator'].isna().sum()}")

    print(f"Missing destinations: {df['destination'].isna().sum()}")

    print(f"Duplicate train IDs: {df['live_train_id'].duplicated().sum()}")

    print(f"Negative delay values: {(df['variation_min'] < 0).sum()}")

    print(f"Cancelled services: {df['cancelled'].sum()}")


if __name__ == "__main__":
    main()




