# UK Rail Data Platform using Python, AWS, Snowflake and DBT

### Documentation

- [x] Python API extraction
- [x] Raw JSON ingestion
- [x] Bronze transformation
- [x] Bronze Parquet output
- [x] Bronze data-quality validation
- [x] Terraform AWS infrastructure
- [x] AWS S3 bucket
- [x] AWS IAM authentication - rail-data-platform IAM user → your AWS CLI / boto3 authentication
- [x] AWS IAM role for Snowflake - rail-snowflake-role IAM role → Snowflake's authentication to S3
- [x] Local Bronze → S3 upload
- [x] boto3 S3 upload automation
- [x] Snowflake database and RAW schema
- [x] Snowflake RAW table - Snowflake appropriate data types for bronze parquet - light transformations
- [x] Snowflake storage integration - The clean approach is to use a Snowflake storage integration + AWS IAM role, rather than putting AWS access keys inside Snowflake.
- [x] Snowflake external stage
- [x] S3 → Snowflake connectivity verified - Snowflake can see Parquet
- [x] S3 → Snowflake RAW ingestion - using COPY INTO command to load the Parquet into RAW (Batch 1)
- [x] Snowpipe - gets new data into Snowflake (automation) -> to detent new files and automatically loads them (Batch 2)

            Batch 1 → 5 rows
            Batch 2 → 5 rows
                    ↓
            10 rows in RAW

- [x] Snowflake Streams - identifies what changed -> track changes and only new records coming in from api when extracting:

        Batch 1 → RAW -> 5 rows 
        Batch 2 → RAW -> 10 rows 

        CREATE STREAM

        Batch 3 → RAW -> 15 rows
                    ↓
                STREAM
                    ↓
                detects Batch 3

- [x] Snowpark transformations - Python transformations inside Snowflake

        RAW       = 15 rows
        STREAM    = 5 new rows
        SILVER    = 5 processed rows
        


The Python code executed inside Snowflake's environment:

        Local Machine
            │
            │ SQL
            ▼
        Snowflake
            │
            ├── Stream
            │
            └── Snowpark Python
                    ↓
                  Silver


- [x] dbt-snowflake is the adapter in virtual environment allows dbt to communicate with Snowflake
        (dbt isn't replacing Snowflake. dbt is managing your SQL transformations inside Snowflake.)

- [x] dbt Silver/Gold models - SQL-based data modelling
        (created dbt tests for daily_operator_performance)

- [x] Snowflake Tasks - automate the pipeline


### Architecture

API → Python ETL → Bronze Parquet → S3 → Snowpipe → Snowflake RAW → Streams → Snowpark → dbt Silver/Gold → Tasks → Power BI


# Diagram - UK Rail Data Platform — Architecture

```
             UK Rail Public API
                     │
                     ▼
                Python ETL
          Extract → Transform → Validate
                     │
                     ▼
              Bronze Parquet
                     │
                     ▼
                  AWS S3
                     │
                     ▼
                 Snowpipe
                     │
                     ▼
              Snowflake RAW
                     │
                     ▼
              Snowflake Stream
                     │
                     ▼
          Snowflake Task (conditional)
          WHEN stream has pending data
                     │
                     ▼
          Snowpark Python Procedure
                     │
                     ▼
             Snowflake SILVER
                     │
                     ▼
                    dbt
             Transform and test
                     │
                     ▼
             Snowflake GOLD
                     │
                     ▼
         Analytics / BI consumption
              (e.g. Power BI)
```



## Troubleshooting and Incident Resolution - New Bronze data was not loading into Snowflake RAW

**Issue**

After running the Python ingestion pipeline, a new Parquet file was successfully uploaded to Amazon S3, but the corresponding records did not appear in the Snowflake RAW table. Snowpipe reported that it was running with no pending files, while queries for the latest extraction returned zero rows.

**Investigation**

The issue was investigated across the ingestion pipeline:

1. **Python extraction:** Confirmed that the railway API returned five departure records and saved the response as JSON.
2. **Bronze transformation:** Converted the response into a Parquet file containing five rows and 23 columns.
3. **Data validation:** Checked for missing station codes, operators and destinations, duplicate train IDs, negative delays and cancelled services.
4. **S3 upload:** Confirmed that the new Parquet file was uploaded successfully to a new date-partitioned location:
   `bronze/rail/station=RDG/service_date=2026-10-29/reading_departures.parquet`
5. **Snowpipe monitoring:** Checked the pipe status and queried the RAW table to establish whether the new records had loaded.
6. **Configuration inspection:** Retrieved the Snowpipe definition and identified that `AUTO_INGEST` was set to `FALSE`.

**Root cause**

The Snowpipe configuration did not enable automatic ingestion through S3 event notifications. Consequently, uploading a new file to S3 did not automatically trigger its loading into Snowflake RAW.

**Resolution**

Triggered a manual Snowpipe refresh:

```sql
ALTER PIPE RAIL_DATA.RAW.RAIL_DEPARTURES_PIPE REFRESH;
```

This prompted Snowflake to discover eligible files in the configured stage path and load files that had not already been processed.

**Verification**

Queried the RAW table for records extracted on 29 October 2026. The query returned five records, confirming that the new batch had successfully reached Snowflake RAW.

**Lessons learned**

- A pipe reporting `RUNNING` does not, by itself, prove that new files are being loaded.
- A zero pending-file count does not prove that the latest S3 upload has reached the target table.
- Ingestion monitoring should verify the actual data in RAW, not rely solely on service status.
- Manual refresh is a useful when automatic ingestion is not configured.
- The stream-triggered Snowflake Task is a separate downstream process and must be validated independently.

**Follow-up improvements**

- Decide whether to retain manual refresh or configure S3 event notifications for automatic ingestion.
- Add monitoring for ingestion freshness and expected row counts.
- Validate stream-triggered task execution and confirm that Silver receives the expected records.
- Implement idempotent processing to prevent duplicate Silver records during retries or repeated ingestion.

