from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# ADVENTUREWORKS BUSINESS ANALYSIS
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "sales_featured.csv"
)

REPORT_DIR = (
    BASE_DIR
    / "reports"
)

ANALYSIS_DIR = (
    REPORT_DIR
    / "analysis"
)

ANALYSIS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD FEATURED DATA
# ============================================================

print("\n[1] LOADING FEATURED DATA")

print(
    f"Input file:\n{INPUT_FILE}"
)


if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )


df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["OrderDate"]
)


print(
    f"Input shape: "
    f"{len(df):,} rows × "
    f"{len(df.columns):,} columns"
)


# ============================================================
# 3. REQUIRED COLUMNS
# ============================================================

print("\n[2] COLUMN VALIDATION")

required_columns = [
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
# 4. BASIC DATA VALIDATION
# ============================================================

print("\n[3] BASIC DATA VALIDATION")

missing_values = (
    df[required_columns]
    .isna()
    .sum()
    .sum()
)


duplicate_rows = (
    df.duplicated()
    .sum()
)


profit_difference = (
    df["Profit"]
    -
    (
        df["SalesAmount"]
        -
        df["TotalProductCost"]
    )
).abs()


profit_mismatches = (
    profit_difference > 0.01
).sum()


print(
    f"Missing values: "
    f"{missing_values:,}"
)

print(
    f"Duplicate rows: "
    f"{duplicate_rows:,}"
)

print(
    f"Profit mismatches: "
    f"{profit_mismatches:,}"
)


if missing_values > 0:
    raise ValueError(
        "Missing values detected."
    )


if duplicate_rows > 0:
    raise ValueError(
        "Duplicate rows detected."
    )


if profit_mismatches > 0:
    raise ValueError(
        "Profit calculation mismatch detected."
    )


# ============================================================
# 5. CORE BUSINESS KPIs
# ============================================================

print("\n[4] CORE BUSINESS KPIs")

total_sales = (
    df["SalesAmount"]
    .sum()
)

total_cost = (
    df["TotalProductCost"]
    .sum()
)

total_profit = (
    df["Profit"]
    .sum()
)

profit_margin = (
    total_profit
    /
    total_sales
)

total_sales_records = (
    len(df)
)

unique_orders = (
    df["SalesOrderNumber"]
    .nunique()
)

unique_customers = (
    df["CustomerKey"]
    .nunique()
)

average_order_value = (
    total_sales
    /
    unique_orders
)

average_sales_per_record = (
    total_sales
    /
    total_sales_records
)


print(
    f"Total Sales: "
    f"{total_sales:,.2f}"
)

print(
    f"Total Cost: "
    f"{total_cost:,.2f}"
)

print(
    f"Total Profit: "
    f"{total_profit:,.2f}"
)

print(
    f"Profit Margin: "
    f"{profit_margin:.2%}"
)

print(
    f"Sales Records: "
    f"{total_sales_records:,}"
)

print(
    f"Unique Orders: "
    f"{unique_orders:,}"
)

print(
    f"Unique Customers: "
    f"{unique_customers:,}"
)

print(
    f"Average Order Value: "
    f"{average_order_value:,.2f}"
)

print(
    f"Average Sales per Record: "
    f"{average_sales_per_record:,.2f}"
)


# ============================================================
# 6. YEARLY SALES & PROFIT
# ============================================================

print("\n[5] YEARLY SALES & PROFIT")

yearly_analysis = (
    df
    .groupby("OrderYear", as_index=False)
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        SalesRecords=(
            "SalesOrderNumber",
            "size"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


yearly_analysis["ProfitMargin"] = (
    yearly_analysis["Profit"]
    /
    yearly_analysis["Sales"]
)


yearly_analysis["AverageOrderValue"] = (
    yearly_analysis["Sales"]
    /
    yearly_analysis["Orders"]
)


yearly_analysis = (
    yearly_analysis
    .sort_values("OrderYear")
    .reset_index(drop=True)
)


print(
    yearly_analysis.to_string(
        index=False
    )
)


# ============================================================
# 7. YEAR-OVER-YEAR GROWTH
# ============================================================

print("\n[6] YEAR-OVER-YEAR GROWTH")

yearly_analysis["SalesYoYGrowth"] = (
    yearly_analysis["Sales"]
    .pct_change()
)

yearly_analysis["ProfitYoYGrowth"] = (
    yearly_analysis["Profit"]
    .pct_change()
)


print(
    yearly_analysis[
        [
            "OrderYear",
            "Sales",
            "SalesYoYGrowth",
            "Profit",
            "ProfitYoYGrowth",
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. MONTHLY SALES & PROFIT
# ============================================================

print("\n[7] MONTHLY SALES & PROFIT")

monthly_analysis = (
    df
    .groupby(
        [
            "OrderYear",
            "OrderMonthNumber",
            "OrderMonth",
            "OrderYearMonth",
        ],
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        SalesRecords=(
            "SalesOrderNumber",
            "size"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


monthly_analysis["ProfitMargin"] = (
    monthly_analysis["Profit"]
    /
    monthly_analysis["Sales"]
)


monthly_analysis["AverageOrderValue"] = (
    monthly_analysis["Sales"]
    /
    monthly_analysis["Orders"]
)


monthly_analysis = (
    monthly_analysis
    .sort_values(
        [
            "OrderYear",
            "OrderMonthNumber",
        ]
    )
    .reset_index(drop=True)
)


print(
    monthly_analysis.head(12).to_string(
        index=False
    )
)


print(
    f"\nTotal monthly periods: "
    f"{len(monthly_analysis):,}"
)


# ============================================================
# 9. COUNTRY ANALYSIS
# ============================================================

print("\n[8] COUNTRY ANALYSIS")

country_analysis = (
    df
    .groupby(
        "Country",
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


country_analysis["ProfitMargin"] = (
    country_analysis["Profit"]
    /
    country_analysis["Sales"]
)


country_analysis["SalesShare"] = (
    country_analysis["Sales"]
    /
    total_sales
)


country_analysis = (
    country_analysis
    .sort_values(
        "Sales",
        ascending=False
    )
    .reset_index(drop=True)
)


print(
    country_analysis.head(10).to_string(
        index=False
    )
)


# ============================================================
# 10. PRODUCT CATEGORY ANALYSIS
# ============================================================

print("\n[9] PRODUCT CATEGORY ANALYSIS")

category_analysis = (
    df
    .groupby(
        "ProductCategoryName",
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


category_analysis["ProfitMargin"] = (
    category_analysis["Profit"]
    /
    category_analysis["Sales"]
)


category_analysis["SalesShare"] = (
    category_analysis["Sales"]
    /
    total_sales
)


category_analysis = (
    category_analysis
    .sort_values(
        "Sales",
        ascending=False
    )
    .reset_index(drop=True)
)


print(
    category_analysis.to_string(
        index=False
    )
)


# ============================================================
# 11. TOP PRODUCTS
# ============================================================

print("\n[10] TOP PRODUCTS")

product_analysis = (
    df
    .groupby(
        "ProductName",
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        SalesRecords=(
            "SalesOrderNumber",
            "size"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


product_analysis["ProfitMargin"] = (
    product_analysis["Profit"]
    /
    product_analysis["Sales"]
)


product_analysis = (
    product_analysis
    .sort_values(
        "Sales",
        ascending=False
    )
    .reset_index(drop=True)
)


print(
    product_analysis.head(10).to_string(
        index=False
    )
)


# ============================================================
# 12. TOP CUSTOMERS
# ============================================================

print("\n[11] TOP CUSTOMERS")

df["CustomerName"] = (
    df["FirstName"].fillna("")
    .str.strip()
    + " "
    +
    df["LastName"].fillna("")
    .str.strip()
)


customer_analysis = (
    df
    .groupby(
        [
            "CustomerKey",
            "CustomerName",
        ],
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Cost=(
            "TotalProductCost",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        SalesRecords=(
            "SalesOrderNumber",
            "size"
        ),
    )
)


customer_analysis["ProfitMargin"] = (
    customer_analysis["Profit"]
    /
    customer_analysis["Sales"]
)


customer_analysis = (
    customer_analysis
    .sort_values(
        "Sales",
        ascending=False
    )
    .reset_index(drop=True)
)


print(
    customer_analysis.head(10).to_string(
        index=False
    )
)


# ============================================================
# 13. TOP CITY ANALYSIS
# ============================================================

print("\n[12] TOP CITIES")

city_analysis = (
    df
    .groupby(
        "City",
        as_index=False
    )
    .agg(
        Sales=(
            "SalesAmount",
            "sum"
        ),
        Profit=(
            "Profit",
            "sum"
        ),
        Orders=(
            "SalesOrderNumber",
            "nunique"
        ),
        Customers=(
            "CustomerKey",
            "nunique"
        ),
    )
)


city_analysis["ProfitMargin"] = (
    city_analysis["Profit"]
    /
    city_analysis["Sales"]
)


city_analysis = (
    city_analysis
    .sort_values(
        "Sales",
        ascending=False
    )
    .reset_index(drop=True)
)


print(
    city_analysis.head(10).to_string(
        index=False
    )
)


# ============================================================
# 14. BUSINESS VALIDATION
# ============================================================

print("\n[13] BUSINESS VALIDATION")

yearly_sales_total = (
    yearly_analysis["Sales"]
    .sum()
)

yearly_profit_total = (
    yearly_analysis["Profit"]
    .sum()
)

country_sales_total = (
    country_analysis["Sales"]
    .sum()
)

category_sales_total = (
    category_analysis["Sales"]
    .sum()
)


sales_difference_year = abs(
    total_sales
    -
    yearly_sales_total
)

profit_difference_year = abs(
    total_profit
    -
    yearly_profit_total
)

sales_difference_country = abs(
    total_sales
    -
    country_sales_total
)

sales_difference_category = abs(
    total_sales
    -
    category_sales_total
)


print(
    f"Sales vs yearly analysis difference: "
    f"{sales_difference_year:.6f}"
)

print(
    f"Profit vs yearly analysis difference: "
    f"{profit_difference_year:.6f}"
)

print(
    f"Sales vs country analysis difference: "
    f"{sales_difference_country:.6f}"
)

print(
    f"Sales vs category analysis difference: "
    f"{sales_difference_category:.6f}"
)


validation_pass = (
    sales_difference_year < 0.01
    and
    profit_difference_year < 0.01
    and
    sales_difference_country < 0.01
    and
    sales_difference_category < 0.01
)


if not validation_pass:

    raise ValueError(
        "Business aggregation validation failed."
    )


# ============================================================
# 15. KPI EXPORT
# ============================================================

print("\n[14] EXPORTING ANALYSIS RESULTS")

kpi_summary = pd.DataFrame(
    [
        {
            "KPI": "Total Sales",
            "Value": total_sales,
        },
        {
            "KPI": "Total Cost",
            "Value": total_cost,
        },
        {
            "KPI": "Total Profit",
            "Value": total_profit,
        },
        {
            "KPI": "Profit Margin",
            "Value": profit_margin,
        },
        {
            "KPI": "Sales Records",
            "Value": total_sales_records,
        },
        {
            "KPI": "Unique Orders",
            "Value": unique_orders,
        },
        {
            "KPI": "Unique Customers",
            "Value": unique_customers,
        },
        {
            "KPI": "Average Order Value",
            "Value": average_order_value,
        },
        {
            "KPI": "Average Sales per Record",
            "Value": average_sales_per_record,
        },
    ]
)


# ============================================================
# 16. SAVE ANALYSIS FILES
# ============================================================

kpi_file = (
    ANALYSIS_DIR
    / "kpi_summary.csv"
)

yearly_file = (
    ANALYSIS_DIR
    / "yearly_sales_profit.csv"
)

monthly_file = (
    ANALYSIS_DIR
    / "monthly_sales_profit.csv"
)

country_file = (
    ANALYSIS_DIR
    / "country_analysis.csv"
)

category_file = (
    ANALYSIS_DIR
    / "category_analysis.csv"
)

product_file = (
    ANALYSIS_DIR
    / "product_analysis.csv"
)

customer_file = (
    ANALYSIS_DIR
    / "customer_analysis.csv"
)

city_file = (
    ANALYSIS_DIR
    / "city_analysis.csv"
)


kpi_summary.to_csv(
    kpi_file,
    index=False
)

yearly_analysis.to_csv(
    yearly_file,
    index=False
)

monthly_analysis.to_csv(
    monthly_file,
    index=False
)

country_analysis.to_csv(
    country_file,
    index=False
)

category_analysis.to_csv(
    category_file,
    index=False
)

product_analysis.to_csv(
    product_file,
    index=False
)

customer_analysis.to_csv(
    customer_file,
    index=False
)

city_analysis.to_csv(
    city_file,
    index=False
)


# ============================================================
# 17. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED")
print("=" * 70)

print(
    "OVERALL STATUS: PASS"
)

print(
    f"Input dataset: "
    f"{len(df):,} rows × "
    f"{len(df.columns):,} columns"
)

print(
    f"Analysis output directory:\n"
    f"{ANALYSIS_DIR}"
)

print("\nGenerated files:")

for file_path in [
    kpi_file,
    yearly_file,
    monthly_file,
    country_file,
    category_file,
    product_file,
    customer_file,
    city_file,
]:

    print(
        f" - {file_path.name}"
    )

print("=" * 70)