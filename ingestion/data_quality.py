from sqlalchemy import create_engine, text
import sys

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
)

print("🔍 Running Data Quality Checks...\n")
passed = 0
failed = 0

def check(name, result, expected=True):
    global passed, failed
    if result == expected:
        print(f"✅ PASSED — {name}")
        passed += 1
    else:
        print(f"❌ FAILED — {name}")
        failed += 1

with engine.connect() as conn:

    # Check 1 — Row count is at least 50k
    count = conn.execute(text(
        "SELECT COUNT(*) FROM raw_chicago_crimes"
    )).scalar()
    print(f"📊 Total records: {count:,}")
    check("Row count is at least 50,000", count >= 50000)

    # Check 2 — No duplicate case numbers
    dupes = conn.execute(text("""
        SELECT COUNT(*) FROM (
            SELECT case_number, COUNT(*)
            FROM raw_chicago_crimes
            GROUP BY case_number
            HAVING COUNT(*) > 1
        ) dupes
    """)).scalar()
    print(f"📊 Duplicate case numbers: {dupes}")
    check("Duplicate case numbers under 100", dupes < 100)

    # Check 3 — No null IDs
    null_ids = conn.execute(text("""
        SELECT COUNT(*) FROM raw_chicago_crimes
        WHERE id IS NULL
    """)).scalar()
    print(f"📊 Null IDs: {null_ids}")
    check("No null IDs", null_ids == 0)

    # Check 4 — No null crime types
    null_types = conn.execute(text("""
        SELECT COUNT(*) FROM raw_chicago_crimes
        WHERE primary_type IS NULL
    """)).scalar()
    print(f"📊 Null crime types: {null_types}")
    check("No null crime types", null_types == 0)

    # Check 5 — No null dates
    null_dates = conn.execute(text("""
        SELECT COUNT(*) FROM raw_chicago_crimes
        WHERE date IS NULL
    """)).scalar()
    print(f"📊 Null dates: {null_dates}")
    check("No null dates", null_dates == 0)

    # Check 6 — Staging table exists and has data
    stg_count = conn.execute(text(
        "SELECT COUNT(*) FROM stg_chicago_crimes"
    )).scalar()
    print(f"📊 Staging table records: {stg_count:,}")
    check("Staging table has data", stg_count > 0)

    # Check 7 — crimes_by_type has data
    type_count = conn.execute(text(
        "SELECT COUNT(*) FROM crimes_by_type"
    )).scalar()
    print(f"📊 Crime types found: {type_count}")
    check("crimes_by_type has data", type_count > 0)

    # Check 8 — arrest rate is between 0 and 100
    bad_rates = conn.execute(text("""
        SELECT COUNT(*) FROM crimes_by_type
        WHERE arrest_rate_pct < 0 OR arrest_rate_pct > 100
    """)).scalar()
    print(f"📊 Invalid arrest rates: {bad_rates}")
    check("All arrest rates are valid (0-100%)", bad_rates == 0)

print(f"\n{'='*40}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"{'='*40}")

if failed > 0:
    print("\n⚠️ Some checks failed! Please review the data.")
    sys.exit(1)
else:
    print("\n🎉 All checks passed! Data quality is good!")