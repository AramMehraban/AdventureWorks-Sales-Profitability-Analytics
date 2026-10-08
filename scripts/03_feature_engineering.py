from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# ADVENTUREWORKS FEATURE ENGINEERING
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS FEATURE ENGINEERING")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_clean.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_featured.csv"
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD CLEAN DATA
# ============================================================

print("\n[1] LOADING CLEAN DATA")

print(
    f"Input file: {INPUT_FILE}"
)


if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )


df = pd.read_csv(
    INPUT_FILE
)


print(
    f"Input shape: "
    f"{len(df):,} rows × "
    f"{len(df.columns)} columns"
)


# ============================================================
# 3. REQUIRED COLUMNS
# ============================================================

print("\n[2] COLUMN VALIDATION")

required_columns = [
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


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


print(
    f"Required columns: "
    f"{len(required_columns)}"
)

print(
    f"Missing columns: "
    f"{len(missing_columns)}"
)


if missing_columns:

    print("\nMissing columns:")

    for column in missing_columns:
        print(f" - {column}")

    raise ValueError(
        "Required columns are missing."
    )


# ============================================================
# 4. DATE CONVERSION
# ============================================================

print("\n[3] DATE PREPARATION")

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
    f"Invalid dates: "
    f"{invalid_dates:,}"
)


if invalid_dates > 0:

    raise ValueError(
        "Invalid dates detected."
    )


# ============================================================
# 5. YEAR
# ============================================================

print("\n[4] CREATING TIME FEATURES")

df["OrderYear"] = (
    df["OrderDate"]
    .dt.year
)


# ============================================================
# 6. MONTH NUMBER
# ============================================================

df["OrderMonthNumber"] = (
    df["OrderDate"]
    .dt.month
)


# ============================================================
# 7. MONTH NAME
# ============================================================

df["OrderMonth"] = (
    df["OrderDate"]
    .dt.strftime("%B")
)


# ============================================================
# 8. YEAR-MONTH
# ============================================================

df["OrderYearMonth"] = (
    df["OrderDate"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# 9. PROFIT MARGIN
# ============================================================

print("\n[5] CREATING PROFITABILITY FEATURES")

df["ProfitMargin"] = np.where(
    df["SalesAmount"] != 0,
    df["Profit"] / df["SalesAmount"],
    np.nan
)


# ============================================================
# 10. FEATURE VALIDATION
# ============================================================

print("\n[6] FEATURE VALIDATION")

new_features = [
    "OrderYear",
    "OrderMonthNumber",
    "OrderMonth",
    "OrderYearMonth",
    "ProfitMargin",
]


for column in new_features:

    missing = (
        df[column]
        .isna()
        .sum()
    )

    print(
        f"{column}: "
        f"missing={missing:,}"
    )


# ============================================================
# 11. PROFIT VALIDATION
# ============================================================

print("\n[7] PROFIT VALIDATION")

profit_difference = (
    df["Profit"]
    - (
        df["SalesAmount"]
        - df["TotalProductCost"]
    )
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
# 12. PROFIT MARGIN VALIDATION
# ============================================================

print("\n[8] PROFIT MARGIN VALIDATION")

valid_margin = (
    df["SalesAmount"] != 0
)


expected_margin = (
    df.loc[
        valid_margin,
        "Profit"
    ]
    /
    df.loc[
        valid_margin,
        "SalesAmount"
    ]
)


margin_difference = (
    df.loc[
        valid_margin,
        "ProfitMargin"
    ]
    -
    expected_margin
).abs()


margin_mismatches = (
    margin_difference > 0.000001
).sum()


print(
    f"Profit margin mismatches: "
    f"{margin_mismatches:,}"
)


print(
    f"Minimum Profit Margin: "
    f"{df['ProfitMargin'].min():.2%}"
)


print(
    f"Maximum Profit Margin: "
    f"{df['ProfitMargin'].max():.2%}"
)


print(
    f"Average Profit Margin: "
    f"{df['ProfitMargin'].mean():.2%}"
)


if margin_mismatches > 0:

    raise ValueError(
        "Profit margin validation failed."
    )


# ============================================================
# 13. YEAR VALIDATION
# ============================================================

print("\n[9] YEAR VALIDATION")

print(
    f"Minimum OrderYear: "
    f"{df['OrderYear'].min()}"
)

print(
    f"Maximum OrderYear: "
    f"{df['OrderYear'].max()}"
)

print(
    "Years:"
)

for year in sorted(
    df["OrderYear"].unique()
):

    print(
        f" - {year}"
    )


# ============================================================
# 14. MONTH VALIDATION
# ============================================================

print("\n[10] MONTH VALIDATION")

print(
    f"Minimum month number: "
    f"{df['OrderMonthNumber'].min()}"
)

print(
    f"Maximum month number: "
    f"{df['OrderMonthNumber'].max()}"
)


# ============================================================
# 15. YEAR-MONTH VALIDATION
# ============================================================

print("\n[11] YEAR-MONTH VALIDATION")

print(
    f"Unique Year-Month values: "
    f"{df['OrderYearMonth'].nunique():,}"
)


print(
    "First 5 Year-Month values:"
)

for value in (
    df["OrderYearMonth"]
    .drop_duplicates()
    .sort_values()
    .head(5)
):

    print(
        f" - {value}"
    )


# ============================================================
# 16. FINAL COLUMN ORDER
# ============================================================

print("\n[12] FINAL COLUMN ORDER")

final_columns = [
    "SalesOrderNumber",
    "OrderDate",
    "OrderYear",
    "OrderMonthNumber",
    "OrderMonth",
    "OrderYearMonth",
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
    "ProfitMargin",
]


df = df[
    final_columns
]


print(
    f"Final columns: "
    f"{len(df.columns)}"
)


# ============================================================
# 17. SORT DATA
# ============================================================

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


# ============================================================
# 18. FINAL DATA VALIDATION
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


# ============================================================
# 19. EXPORT
# ============================================================

print("\n[14] EXPORT")

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(
    f"Featured dataset saved to:\n"
    f"{OUTPUT_FILE}"
)


# ============================================================
# 20. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 70)


if (
    final_missing == 0
    and final_duplicates == 0
    and profit_mismatches == 0
    and margin_mismatches == 0
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