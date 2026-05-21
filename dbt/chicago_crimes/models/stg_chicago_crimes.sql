-- Staging model: clean and prepare raw chicago crimes data

SELECT
    id,
    case_number,
    date::timestamp AS crime_date,
    block,
    primary_type AS crime_type,
    description,
    location_description,
    arrest::boolean AS was_arrested,
    domestic::boolean AS is_domestic,
    beat,
    district,
    ward,
    community_area,
    fbi_code,
    year::integer AS crime_year,
    latitude::float AS latitude,
    longitude::float AS longitude
FROM raw_chicago_crimes
WHERE id IS NOT NULL
AND date IS NOT NULL