from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# ADVENTUREWORKS VISUALIZATION
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS VISUALIZATION")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

ANALYSIS_DIR = (
    BASE_DIR
    / "reports"
    / "analysis"
)

CHART_DIR = (
    BASE_DIR
    / "reports"
    / "charts"
)

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD ANALYSIS DATA
# ============================================================

print("\n[1] LOADING ANALYSIS DATA")


required_files = [
    "yearly_sales_profit.csv",
    "monthly_sales_profit.csv",
    "country_analysis.csv",
    "category_analysis.csv",
    "product_analysis.csv",
    "customer_analysis.csv",
    "city_analysis.csv",
]


missing_files = [
    file_name
    for file_name in required_files
    if not (ANALYSIS_DIR / file_name).exists()
]


if missing_files:

    print("\nMissing analysis files:")

    for file_name in missing_files:
        print(f" - {file_name}")

    raise FileNotFoundError(
        "Required analysis files are missing."
    )


yearly = pd.read_csv(
    ANALYSIS_DIR / "yearly_sales_profit.csv"
)

monthly = pd.read_csv(
    ANALYSIS_DIR / "monthly_sales_profit.csv"
)

country = pd.read_csv(
    ANALYSIS_DIR / "country_analysis.csv"
)

category = pd.read_csv(
    ANALYSIS_DIR / "category_analysis.csv"
)

product = pd.read_csv(
    ANALYSIS_DIR / "product_analysis.csv"
)

customer = pd.read_csv(
    ANALYSIS_DIR / "customer_analysis.csv"
)

city = pd.read_csv(
    ANALYSIS_DIR / "city_analysis.csv"
)


print(
    f"Yearly rows: {len(yearly):,}"
)

print(
    f"Monthly rows: {len(monthly):,}"
)

print(
    f"Countries: {len(country):,}"
)

print(
    f"Categories: {len(category):,}"
)

print(
    f"Products: {len(product):,}"
)

print(
    f"Customers: {len(customer):,}"
)

print(
    f"Cities: {len(city):,}"
)


# ============================================================
# 3. CHART HELPER
# ============================================================

def save_chart(
    filename,
    title,
    xlabel=None,
    ylabel=None,
):
    """
    Apply common formatting and save the current chart.
    """

    plt.title(
        title,
        fontsize=14,
        fontweight="bold"
    )

    if xlabel:
        plt.xlabel(xlabel)

    if ylabel:
        plt.ylabel(ylabel)

    plt.tight_layout()

    output_file = (
        CHART_DIR
        / filename
    )

    plt.savefig(
        output_file,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {filename}"
    )


# ============================================================
# 4. YEARLY SALES TREND
# ============================================================

print("\n[2] YEARLY SALES TREND")

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    yearly["OrderYear"],
    yearly["Sales"],
    marker="o"
)

save_chart(
    "yearly_sales_trend.png",
    "Yearly Sales Trend",
    "Year",
    "Sales"
)


# ============================================================
# 5. YEARLY PROFIT TREND
# ============================================================

print("\n[3] YEARLY PROFIT TREND")

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    yearly["OrderYear"],
    yearly["Profit"],
    marker="o"
)

save_chart(
    "yearly_profit_trend.png",
    "Yearly Profit Trend",
    "Year",
    "Profit"
)


# ============================================================
# 6. YEARLY SALES VS PROFIT
# ============================================================

print("\n[4] YEARLY SALES VS PROFIT")

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    yearly["OrderYear"],
    yearly["Sales"],
    marker="o",
    label="Sales"
)

plt.plot(
    yearly["OrderYear"],
    yearly["Profit"],
    marker="o",
    label="Profit"
)

plt.legend()

save_chart(
    "yearly_sales_vs_profit.png",
    "Yearly Sales vs Profit",
    "Year",
    "Amount"
)


# ============================================================
# 7. MONTHLY SALES TREND
# ============================================================

print("\n[5] MONTHLY SALES TREND")

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    monthly["OrderYearMonth"],
    monthly["Sales"],
    marker="o"
)

plt.xticks(
    rotation=45
)

save_chart(
    "monthly_sales_trend.png",
    "Monthly Sales Trend",
    "Year-Month",
    "Sales"
)


# ============================================================
# 8. MONTHLY PROFIT TREND
# ============================================================

print("\n[6] MONTHLY PROFIT TREND")

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    monthly["OrderYearMonth"],
    monthly["Profit"],
    marker="o"
)

plt.xticks(
    rotation=45
)

save_chart(
    "monthly_profit_trend.png",
    "Monthly Profit Trend",
    "Year-Month",
    "Profit"
)


# ============================================================
# 9. PROFIT MARGIN TREND
# ============================================================

print("\n[7] PROFIT MARGIN TREND")

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    monthly["OrderYearMonth"],
    monthly["ProfitMargin"] * 100,
    marker="o"
)

plt.xticks(
    rotation=45
)

save_chart(
    "profit_margin_trend.png",
    "Monthly Profit Margin",
    "Year-Month",
    "Profit Margin (%)"
)


# ============================================================
# 10. TOP COUNTRIES
# ============================================================

print("\n[8] TOP COUNTRIES")

top_countries = (
    country
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
    .sort_values(
        "Sales"
    )
)


plt.figure(
    figsize=(10, 6)
)

plt.barh(
    top_countries["Country"],
    top_countries["Sales"]
)

save_chart(
    "top_countries.png",
    "Top 10 Countries by Sales",
    "Sales",
    "Country"
)


# ============================================================
# 11. CATEGORY SALES
# ============================================================

print("\n[9] CATEGORY SALES")

category_sorted = (
    category
    .sort_values(
        "Sales",
        ascending=False
    )
)


plt.figure(
    figsize=(9, 6)
)

plt.bar(
    category_sorted["ProductCategoryName"],
    category_sorted["Sales"]
)

plt.xticks(
    rotation=20
)

save_chart(
    "category_sales.png",
    "Sales by Product Category",
    "Category",
    "Sales"
)


# ============================================================
# 12. CATEGORY PROFIT MARGIN
# ============================================================

print("\n[10] CATEGORY PROFIT MARGIN")

category_margin = (
    category
    .sort_values(
        "ProfitMargin",
        ascending=False
    )
)


plt.figure(
    figsize=(9, 6)
)

plt.bar(
    category_margin["ProductCategoryName"],
    category_margin["ProfitMargin"] * 100
)

plt.xticks(
    rotation=20
)

save_chart(
    "category_profit_margin.png",
    "Profit Margin by Product Category",
    "Category",
    "Profit Margin (%)"
)


# ============================================================
# 13. TOP PRODUCTS
# ============================================================

print("\n[11] TOP PRODUCTS")

top_products = (
    product
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
    .sort_values(
        "Sales"
    )
)


plt.figure(
    figsize=(11, 7)
)

plt.barh(
    top_products["ProductName"],
    top_products["Sales"]
)

save_chart(
    "top_products.png",
    "Top 10 Products by Sales",
    "Sales",
    "Product"
)


# ============================================================
# 14. TOP CUSTOMERS
# ============================================================

print("\n[12] TOP CUSTOMERS")

top_customers = (
    customer
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
    .sort_values(
        "Sales"
    )
)


plt.figure(
    figsize=(11, 7)
)

plt.barh(
    top_customers["CustomerName"],
    top_customers["Sales"]
)

save_chart(
    "top_customers.png",
    "Top 10 Customers by Sales",
    "Sales",
    "Customer"
)


# ============================================================
# 15. KPI SUMMARY CHART
# ============================================================

print("\n[13] KPI SUMMARY")

total_sales = (
    yearly["Sales"]
    .sum()
)

total_profit = (
    yearly["Profit"]
    .sum()
)

total_orders = (
    yearly["Orders"]
    .sum()
)

total_customers = (
    customer["CustomerKey"]
    .nunique()
)

profit_margin = (
    total_profit
    /
    total_sales
)


kpi_values = [
    total_sales,
    total_profit,
]

kpi_labels = [
    "Total Sales",
    "Total Profit",
]


plt.figure(
    figsize=(9, 6)
)

plt.bar(
    kpi_labels,
    kpi_values
)

save_chart(
    "kpi_dashboard.png",
    "AdventureWorks KPI Summary",
    "KPI",
    "Amount"
)


# ============================================================
# 16. FINAL VALIDATION
# ============================================================

print("\n[14] CHART VALIDATION")

expected_charts = [
    "yearly_sales_trend.png",
    "yearly_profit_trend.png",
    "yearly_sales_vs_profit.png",
    "monthly_sales_trend.png",
    "monthly_profit_trend.png",
    "profit_margin_trend.png",
    "top_countries.png",
    "category_sales.png",
    "category_profit_margin.png",
    "top_products.png",
    "top_customers.png",
    "kpi_dashboard.png",
]


missing_charts = [
    chart
    for chart in expected_charts
    if not (CHART_DIR / chart).exists()
]


print(
    f"Expected charts: "
    f"{len(expected_charts)}"
)

print(
    f"Missing charts: "
    f"{len(missing_charts)}"
)


if missing_charts:

    print("\nMissing charts:")

    for chart in missing_charts:
        print(
            f" - {chart}"
        )

    raise RuntimeError(
        "Chart generation validation failed."
    )


# ============================================================
# 17. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("VISUALIZATION COMPLETED")
print("=" * 70)

print(
    "OVERALL STATUS: PASS"
)

print(
    f"Charts generated: "
    f"{len(expected_charts)}"
)

print(
    f"Chart directory:\n"
    f"{CHART_DIR}"
)

print("=" * 70)
