import pandas as pd

BRONZE_FILE = "data/bronze/reading_departures.parquet"


def main():
    df = pd.read_parquet(BRONZE_FILE)

    print("\n=== Bronze Schema ===")
    print(df.dtypes)

    print("\n=== Bronze Data ===")
    print(df.to_string(index=False))

    print("\n=== Row Count ===")
    print(len(df))


if __name__ == "__main__":
    main()


# this script prints the output of data from the saved 'BRONZE_FILE' which is parquet, 5 train-service records alongwith columns diplayed columns


