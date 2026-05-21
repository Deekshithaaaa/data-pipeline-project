-- How many crimes happened in each district?

SELECT
    district,
    COUNT(*) AS total_crimes,
    SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) AS total_arrests,
    ROUND(
        100.0 * SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS arrest_rate_pct,
    COUNT(DISTINCT crime_type) AS unique_crime_types
FROM {{ ref('stg_chicago_crimes') }}
GROUP BY district
ORDER BY total_crimes DESC