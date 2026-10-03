-- Using dbt to create GOLD.DAILY_OPERATOR_PERFORMANCE in snowflake 

{{ config(materialized='table') }}

SELECT
    service_date,
    operator,

    COUNT(*) AS total_services,

    SUM(CASE
        WHEN cancelled THEN 1
        ELSE 0
    END) AS cancelled_services,

    SUM(CASE
        WHEN variation_min > 0 THEN 1
        ELSE 0
    END) AS late_services,

    SUM(CASE
        WHEN variation_min <= 0 THEN 1
        ELSE 0
    END) AS on_time_or_early_services,

    ROUND(AVG(variation_min), 2) AS average_delay_minutes,

    MAX(variation_min) AS max_delay_minutes

FROM RAIL_DATA.SILVER.DEPARTURES_SILVER

GROUP BY
    service_date,
    operator