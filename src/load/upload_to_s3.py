import boto3
from pathlib import Path

BUCKET_NAME = "uk-rail-data-platform-darren-20260001"

LOCAL_FILE = Path("data/bronze/reading_departures.parquet")

S3_KEY = (
    "bronze/"
    "rail/"
    "station=RDG/"
    "service_date=2026-09-16/"
    "reading_departures.parquet"
)


def upload_to_s3():
    s3 = boto3.client("s3")

    s3.upload_file(
        str(LOCAL_FILE),
        BUCKET_NAME,
        S3_KEY
    )

    print("Upload complete.")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"S3 key: {S3_KEY}")


def main():
    upload_to_s3()


if __name__ == "__main__":
    main()


# real small ETL pipeline complete! 

# boto3
#   ↓
# AWS S3




