from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


# ============================================================
# ADVENTUREWORKS DATA EXTRACTION
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS DATA EXTRACTION")
print("=" * 70)


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = RAW_DATA_DIR / "sales_data.csv"


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    BASE_DIR / ".env"
)


# ============================================================
# 3. DATABASE CONFIGURATION
# ============================================================

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv(
    "DB_DRIVER",
    "ODBC Driver 17 for SQL Server"
)


print("\n[1] DATABASE CONFIGURATION")

print(f"Server: {DB_SERVER}")
print(f"Database: {DB_NAME}")
print(f"Driver: {DB_DRIVER}")


# ============================================================
# 4. VALIDATE ENVIRONMENT
# ============================================================

if not DB_SERVER:
    raise ValueError(
        "DB_SERVER is missing from .env"
    )

if not DB_NAME:
    raise ValueError(
        "DB_NAME is missing from .env"
    )


# ============================================================
# 5. CREATE DATABASE CONNECTION
# ============================================================

print("\n[2] CREATING DATABASE CONNECTION")

connection_string = (
    f"mssql+pyodbc://@{DB_SERVER}/"
    f"{DB_NAME}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
    "&trusted_connection=yes"
)

engine = create_engine(
    connection_string
)


# ============================================================
# 6. TEST CONNECTION
# ============================================================

print("\n[3] TESTING DATABASE CONNECTION")

with engine.connect() as connection:

    result = connection.execute(
        text("SELECT 1")
    )

    value = result.scalar()

    if value == 1:
        print("Database connection: PASS")
    else:
        print("Database connection: REVIEW")


# ============================================================
# 7. SQL QUERY
# ============================================================

print("\n[4] EXECUTING SALES QUERY")


query = """
SELECT
    fs.SalesOrderNumber,
    fs.OrderDate,
    p.EnglishProductName AS ProductName,
    pc.EnglishProductCategoryName AS ProductCategoryName,
    c.CustomerKey,
    c.FirstName,
    c.LastName,
    g.City,
    g.EnglishCountryRegionName AS Country,
    fs.SalesAmount,
    fs.TotalProductCost,
    fs.SalesAmount - fs.TotalProductCost AS Profit

FROM FactInternetSales AS fs

LEFT JOIN DimProduct AS p
    ON fs.ProductKey = p.ProductKey

LEFT JOIN DimProductSubcategory AS ps
    ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey

LEFT JOIN DimProductCategory AS pc
    ON ps.ProductCategoryKey = pc.ProductCategoryKey

LEFT JOIN DimCustomer AS c
    ON fs.CustomerKey = c.CustomerKey

LEFT JOIN DimGeography AS g
    ON c.GeographyKey = g.GeographyKey

WHERE fs.SalesOrderNumber IS NOT NULL
"""


# ============================================================
# 8. EXTRACT DATA
# ============================================================

df = pd.read_sql(
    query,
    engine
)


# ============================================================
# 9. BASIC VALIDATION
# ============================================================

print("\n[5] EXTRACTION VALIDATION")

print(f"Rows:    {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")

for column in df.columns:
    print(f" - {column}")


# ============================================================
# 10. DUPLICATE VALIDATION
# ============================================================

duplicate_rows = df.duplicated().sum()

print(
    f"\nDuplicate rows: {duplicate_rows:,}"
)


# ============================================================
# 11. MISSING VALUE VALIDATION
# ============================================================

total_missing = df.isna().sum().sum()

print(
    f"Total missing values: {total_missing:,}"
)

if total_missing > 0:

    print("\nColumns with missing values:")

    missing_values = df.isna().sum()

    for column, count in missing_values.items():

        if count > 0:

            print(
                f" - {column}: {count:,}"
            )


# ============================================================
# 12. DATE VALIDATION
# ============================================================

df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    errors="coerce"
)

invalid_dates = df["OrderDate"].isna().sum()

print(
    f"\nInvalid dates: {invalid_dates:,}"
)

if invalid_dates == 0:

    print(
        f"Minimum date: "
        f"{df['OrderDate'].min().date()}"
    )

    print(
        f"Maximum date: "
        f"{df['OrderDate'].max().date()}"
    )


# ============================================================
# 13. PROFIT VALIDATION
# ============================================================

calculated_profit = (
    df["SalesAmount"]
    - df["TotalProductCost"]
)

profit_difference = (
    df["Profit"]
    - calculated_profit
).abs()

profit_mismatches = (
    profit_difference > 0.01
).sum()

print(
    f"\nProfit calculation mismatches: "
    f"{profit_mismatches:,}"
)


# ============================================================
# 14. SAVE CSV
# ============================================================

print("\n[6] EXPORT")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"CSV saved to:\n{OUTPUT_FILE}"
)


# ============================================================
# 15. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("EXTRACTION COMPLETED")
print("=" * 70)

print(
    f"Final dataset: "
    f"{len(df):,} rows × {len(df.columns)} columns"
)

print(
    f"Output file: {OUTPUT_FILE}"
)

print("=" * 70)