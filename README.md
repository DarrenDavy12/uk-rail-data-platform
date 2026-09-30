## Current Progress

### Completed

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
- [x] Snowpipe - automation -> to detent new files and automatically loads them (Batch 2)
                                                                                                        Batch 1 → 5 rows
                                                                                                        Batch 2 → 5 rows
                                                                                                                    ↓
                                                                                                                10 rows in RAW

### In Progress

- [ ] Snowflake Streams
- [ ] Snowpark transformations
- [ ] dbt Silver/Gold models
- [ ] Snowflake Tasks
- [ ] Power BI


### Architecture

API → Python ETL → Bronze Parquet → S3 → Snowpipe → Snowflake RAW → Streams → Snowpark → dbt Silver/Gold → Tasks → Power BI



