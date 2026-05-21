from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
)

with engine.connect() as conn:

    # Model 1: Staging - clean raw data
    print("Creating staging table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS stg_chicago_crimes;
        CREATE TABLE stg_chicago_crimes AS
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
            year::integer AS crime_year,
            latitude::float AS latitude,
            longitude::float AS longitude
        FROM raw_chicago_crimes
        WHERE id IS NOT NULL
        AND date IS NOT NULL;
    """))
    conn.commit()
    print("✅ Staging table created!")

    # Model 2: Crimes by type
    print("Creating crimes_by_type table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS crimes_by_type;
        CREATE TABLE crimes_by_type AS
        SELECT
            crime_type,
            COUNT(*) AS total_crimes,
            SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) AS total_arrests,
            ROUND(
                100.0 * SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS arrest_rate_pct
        FROM stg_chicago_crimes
        GROUP BY crime_type
        ORDER BY total_crimes DESC;
    """))
    conn.commit()
    print("✅ Crimes by type table created!")

    # Model 3: Crimes by district
    print("Creating crimes_by_district table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS crimes_by_district;
        CREATE TABLE crimes_by_district AS
        SELECT
            district,
            COUNT(*) AS total_crimes,
            SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) AS total_arrests,
            ROUND(
                100.0 * SUM(CASE WHEN was_arrested THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS arrest_rate_pct,
            COUNT(DISTINCT crime_type) AS unique_crime_types
        FROM stg_chicago_crimes
        GROUP BY district
        ORDER BY total_crimes DESC;
    """))
    conn.commit()
    print("✅ Crimes by district table created!")

print("\n🎉 All transformations done!")