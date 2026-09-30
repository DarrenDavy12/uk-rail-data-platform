import boto3
from pathlib import Path
import pandas as pd

BUCKET_NAME = "uk-rail-data-platform-darren-20260001"

LOCAL_FILE = Path("data/bronze/reading_departures.parquet")


def upload_to_s3():
    df = pd.read_parquet(LOCAL_FILE)

    service_date = df["service_date"].iloc[0]

    s3_key = (
        "bronze/"
        "rail/"
        f"station=RDG/"
        f"service_date={service_date}/"
        "reading_departures.parquet"
    )

    s3 = boto3.client("s3")

    s3.upload_file(
        str(LOCAL_FILE),
        BUCKET_NAME,
        s3_key
    )

    print("Upload complete.")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"S3 key: {s3_key}")


def main():
    upload_to_s3()


if __name__ == "__main__":
    main()