-- Business-rule dbt test
-- should be 8 tests overall now including one from schema.yml 

-- Show me any operator/day where the number of late services plus on-time/early services doesn't equal the total.

-- Custom SQL tests = "Does the data make sense?"
-- It checks whether the data actually makes logical sense.

SELECT
    service_date,
    operator,
    total_services,
    late_services,
    on_time_or_early_services
FROM {{ ref('daily_operator_performance') }}
WHERE
    COALESCE(late_services, 0)
    + COALESCE(on_time_or_early_services, 0)
    != total_services
    OR total_services IS NULL