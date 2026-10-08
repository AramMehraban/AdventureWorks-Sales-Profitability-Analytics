from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# ADVENTUREWORKS DATA CLEANING
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS DATA CLEANING")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "sales_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_clean.csv"
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. EXPECTED COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "SalesOrderNumber",
    "OrderDate",
    "ProductName",
    "ProductCategoryName",
    "CustomerKey",
    "FirstName",
    "LastName",
    "City",
    "Country",
    "SalesAmount",
    "TotalProductCost",
    "Profit",
]


# ============================================================
# 3. LOAD DATA
# ============================================================

print("\n[1] LOADING RAW DATA")

print(f"Input file: {INPUT_FILE}")

if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )


df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Original shape: "
    f"{df.shape[0]:,} rows × {df.shape[1]} columns"
)


# ============================================================
# 4. COLUMN VALIDATION
# ============================================================

print("\n[2] COLUMN VALIDATION")

missing_columns = [
    column
    for column in EXPECTED_COLUMNS
    if column not in df.columns
]

unexpected_columns = [
    column
    for column in df.columns
    if column not in EXPECTED_COLUMNS
]


print(
    f"Expected columns:   {len(EXPECTED_COLUMNS)}"
)

print(
    f"Actual columns:     {len(df.columns)}"
)

print(
    f"Missing columns:    {len(missing_columns)}"
)

print(
    f"Unexpected columns: {len(unexpected_columns)}"
)


if missing_columns:

    print("\nMissing columns:")

    for column in missing_columns:

        print(f" - {column}")

    raise ValueError(
        "Required columns are missing."
    )


if unexpected_columns:

    print("\nUnexpected columns:")

    for column in unexpected_columns:

        print(f" - {column}")


# ============================================================
# 5. COLUMN ORDER
# ============================================================

df = df[
    EXPECTED_COLUMNS
]


print(
    "\nColumn order standardized."
)


# ============================================================
# 6. TEXT CLEANING
# ============================================================

print("\n[3] TEXT CLEANING")

text_columns = [
    "SalesOrderNumber",
    "ProductName",
    "ProductCategoryName",
    "FirstName",
    "LastName",
    "City",
    "Country",
]


for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


print(
    f"Text columns cleaned: "
    f"{len(text_columns)}"
)


# ============================================================
# 7. DATE CLEANING
# ============================================================

print("\n[4] DATE CLEANING")

df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    errors="coerce"
)


invalid_dates = (
    df["OrderDate"]
    .isna()
    .sum()
)


print(
    f"Invalid dates: {invalid_dates:,}"
)


if invalid_dates > 0:

    raise ValueError(
        "Invalid OrderDate values detected."
    )


print(
    f"Minimum date: "
    f"{df['OrderDate'].min().date()}"
)

print(
    f"Maximum date: "
    f"{df['OrderDate'].max().date()}"
)


# ============================================================
# 8. NUMERIC CLEANING
# ============================================================

print("\n[5] NUMERIC VALIDATION")

numeric_columns = [
    "CustomerKey",
    "SalesAmount",
    "TotalProductCost",
    "Profit",
]


for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


    invalid_values = (
        df[column]
        .isna()
        .sum()
    )


    infinite_values = (
        np.isinf(
            df[column]
        )
        .sum()
    )


    print(
        f"{column}: "
        f"invalid={invalid_values:,}, "
        f"infinite={infinite_values:,}"
    )


# ============================================================
# 9. MISSING VALUE VALIDATION
# ============================================================

print("\n[6] MISSING VALUE VALIDATION")

missing_total = (
    df.isna()
    .sum()
    .sum()
)


print(
    f"Total missing values: "
    f"{missing_total:,}"
)


if missing_total > 0:

    print("\nColumns with missing values:")

    missing_by_column = (
        df.isna()
        .sum()
    )


    for column, count in (
        missing_by_column.items()
    ):

        if count > 0:

            print(
                f" - {column}: {count:,}"
            )


# ============================================================
# 10. DUPLICATE VALIDATION
# ============================================================

print("\n[7] DUPLICATE VALIDATION")

duplicate_rows = (
    df.duplicated()
    .sum()
)


print(
    f"Duplicate rows: "
    f"{duplicate_rows:,}"
)


if duplicate_rows > 0:

    print(
        "Removing exact duplicate rows..."
    )

    df = (
        df
        .drop_duplicates()
        .copy()
    )


    print(
        f"Rows after duplicate removal: "
        f"{len(df):,}"
    )


# ============================================================
# 11. BUSINESS KEY VALIDATION
# ============================================================

print("\n[8] BUSINESS KEY VALIDATION")

missing_order_numbers = (
    df["SalesOrderNumber"]
    .isna()
    .sum()
)


unique_orders = (
    df["SalesOrderNumber"]
    .nunique()
)


missing_customer_keys = (
    df["CustomerKey"]
    .isna()
    .sum()
)


unique_customers = (
    df["CustomerKey"]
    .nunique()
)


print(
    f"Missing SalesOrderNumber: "
    f"{missing_order_numbers:,}"
)

print(
    f"Unique SalesOrderNumber: "
    f"{unique_orders:,}"
)

print(
    f"Missing CustomerKey: "
    f"{missing_customer_keys:,}"
)

print(
    f"Unique CustomerKey: "
    f"{unique_customers:,}"
)


# ============================================================
# 12. PROFIT VALIDATION
# ============================================================

print("\n[9] PROFIT VALIDATION")

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
    f"Profit calculation mismatches: "
    f"{profit_mismatches:,}"
)


if profit_mismatches > 0:

    raise ValueError(
        "Profit calculation mismatch detected."
    )


# ============================================================
# 13. BUSINESS VALUE VALIDATION
# ============================================================

print("\n[10] BUSINESS VALUE VALIDATION")

negative_sales = (
    df["SalesAmount"] < 0
).sum()


negative_cost = (
    df["TotalProductCost"] < 0
).sum()


negative_profit = (
    df["Profit"] < 0
).sum()


zero_sales = (
    df["SalesAmount"] == 0
).sum()


print(
    f"Negative SalesAmount:      "
    f"{negative_sales:,}"
)

print(
    f"Negative TotalProductCost: "
    f"{negative_cost:,}"
)

print(
    f"Negative Profit:           "
    f"{negative_profit:,}"
)

print(
    f"Zero SalesAmount:          "
    f"{zero_sales:,}"
)


# ============================================================
# 14. PROFIT MARGIN CHECK
# ============================================================

print("\n[11] PROFIT MARGIN CHECK")

valid_sales = (
    df["SalesAmount"] != 0
)


profit_margin = (
    df.loc[
        valid_sales,
        "Profit"
    ]
    /
    df.loc[
        valid_sales,
        "SalesAmount"
    ]
)


print(
    f"Minimum Profit Margin: "
    f"{profit_margin.min():.2%}"
)


print(
    f"Maximum Profit Margin: "
    f"{profit_margin.max():.2%}"
)


print(
    f"Average Profit Margin: "
    f"{profit_margin.mean():.2%}"
)


# ============================================================
# 15. SORT DATA
# ============================================================

print("\n[12] SORTING DATA")

df = (
    df
    .sort_values(
        by=[
            "OrderDate",
            "SalesOrderNumber"
        ]
    )
    .reset_index(drop=True)
)


print(
    "Data sorted by OrderDate "
    "and SalesOrderNumber."
)


# ============================================================
# 16. FINAL VALIDATION
# ============================================================

print("\n[13] FINAL VALIDATION")

final_missing = (
    df.isna()
    .sum()
    .sum()
)


final_duplicates = (
    df.duplicated()
    .sum()
)


final_profit_difference = (
    df["Profit"]
    - (
        df["SalesAmount"]
        - df["TotalProductCost"]
    )
).abs()


final_profit_mismatches = (
    final_profit_difference > 0.01
).sum()


print(
    f"Final rows: "
    f"{len(df):,}"
)


print(
    f"Final columns: "
    f"{len(df.columns):,}"
)


print(
    f"Final missing values: "
    f"{final_missing:,}"
)


print(
    f"Final duplicate rows: "
    f"{final_duplicates:,}"
)


print(
    f"Final profit mismatches: "
    f"{final_profit_mismatches:,}"
)


# ============================================================
# 17. EXPORT CLEAN DATASET
# ============================================================

print("\n[14] EXPORT")

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    f"Clean dataset saved to:\n"
    f"{OUTPUT_FILE}"
)


# ============================================================
# 18. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)


if (
    final_missing == 0
    and final_duplicates == 0
    and final_profit_mismatches == 0
):

    print(
        "OVERALL STATUS: PASS"
    )

else:

    print(
        "OVERALL STATUS: REVIEW"
    )


print(
    f"Final dataset: "
    f"{len(df):,} rows × "
    f"{len(df.columns):,} columns"
)


print(
    f"Output file: "
    f"{OUTPUT_FILE}"
)


print("=" * 70)