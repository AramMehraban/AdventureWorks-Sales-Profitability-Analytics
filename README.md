# AdventureWorks Sales & Profitability Analytics

## Overview

This project presents a complete end-to-end **Business Intelligence and Data Analytics workflow** using the AdventureWorksDW2025 database.

The project analyzes sales performance, customer behavior, product performance, profitability, and business trends using **SQL Server, Python, Excel, and Power BI**.

The goal is to demonstrate a realistic analytics workflow from raw database data to validated business insights and an interactive Power BI dashboard.

### Project Workflow

```text
SQL Server AdventureWorksDW2025
            ↓
     Data Extraction
            ↓
       Data Cleaning
            ↓
    Feature Engineering
            ↓
   Python Data Analysis
            ↓
    SQL / Excel / Power BI
            ↓
     Business Insights
            ↓
         GitHub
```

---

# Tech Stack

* SQL Server
* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook
* Power BI
* DAX
* Power Query
* Excel
* SQLAlchemy
* PyODBC
* Git / GitHub

---

# Data Source

The project uses the **AdventureWorksDW2025** data warehouse.

### Main Tables

* `FactInternetSales`
* `DimCustomer`
* `DimProduct`
* `DimProductCategory`
* `DimProductSubcategory`
* `DimGeography`

The final analytical dataset combines sales transactions with product, customer, geography, and product-category information.

---

# Data Pipeline

## 1. Data Extraction

Sales data was extracted from SQL Server using SQL queries and Python.

The extraction layer combines information from the following tables:

```text
FactInternetSales
        +
DimProduct
        +
DimProductSubcategory
        +
DimProductCategory
        +
DimCustomer
        +
DimGeography
```

The resulting dataset is exported to:

```text
data/raw/sales_data.csv
```

### Extracted Dataset

* 60,398 sales records
* 27,659 unique orders
* 18,484 unique customers
* 12 source columns

---

# 2. Data Cleaning

The extracted data was validated and cleaned using Python.

The cleaning process includes:

* Data type validation
* Date validation
* Missing-value checks
* Duplicate-row checks
* Sales amount validation
* Cost validation
* Profit validation
* Sales order validation
* Customer validation
* Profit calculation validation

The cleaned dataset is stored in:

```text
data/processed/sales_clean.csv
```

### Data Quality Results

```text
Rows                  60,398
Columns               12
Missing Values        0
Duplicate Rows        0
Invalid Dates         0
Missing Order IDs     0
Missing Customer IDs  0
Negative Sales        0
Negative Cost         0
Negative Profit       0
Profit Validation     PASS
```

---

# 3. Feature Engineering

Additional analytical features were created to support time-series analysis and profitability analysis.

### Features

* `OrderYear`
* `OrderMonthNumber`
* `OrderMonth`
* `OrderYearMonth`
* `ProfitMargin`

The final analytical dataset contains:

```text
60,398 rows
17 columns
```

Saved to:

```text
data/processed/sales_featured.csv
```

---

# Business Questions

The project answers the following business questions:

1. How much total revenue and profit were generated?
2. How do sales and profit change over time?
3. Which countries generate the highest sales?
4. Which product categories drive revenue?
5. Which products generate the highest sales and profit?
6. Which customers contribute the most revenue?
7. How concentrated is customer revenue?
8. Which product categories have the highest profit margins?
9. How does sales performance change year over year?
10. Which business areas require management attention?

---

# Key Business KPIs

The final validated results are:

| KPI                      |         Value |
| ------------------------ | ------------: |
| Total Sales              | 29,358,677.22 |
| Total Cost               | 17,277,793.58 |
| Total Profit             | 12,080,883.65 |
| Profit Margin            |        41.15% |
| Sales Records            |        60,398 |
| Unique Orders            |        27,659 |
| Unique Customers         |        18,484 |
| Unique Products          |           130 |
| Average Order Value      |      1,061.45 |
| Average Sales per Record |        486.09 |

> Note: The project does not perform currency conversion. Monetary values are reported in the source dataset's original currency context.

---

# Business Analysis

## Sales Performance

Total sales reached approximately:

```text
29.36M
```

Total profit reached approximately:

```text
12.08M
```

with an overall profit margin of:

```text
41.15%
```

Sales performance is analyzed by year, month, country, and product category.

---

## Product Category Performance

Three main product categories are represented:

* Bikes
* Accessories
* Clothing

### Key findings

* **Bikes** are the dominant revenue category and generate the vast majority of total sales.
* **Accessories** achieve the highest profit margin at approximately **62.6%**.
* Bikes generate the largest absolute profit because of their much higher sales volume.
* Clothing contributes a smaller share of total revenue.

This indicates that Bikes are critical for revenue generation, while Accessories provide an important high-margin opportunity.

---

# Customer Analysis

Customer analysis focuses on:

* Customer revenue
* Customer order frequency
* Customer profitability
* Customer concentration
* Top customers by sales

The project contains:

```text
18,484 unique customers
```

A relatively small group of high-value customers contributes a significant share of total revenue.

This makes customer retention and revenue concentration important management considerations.

---

# Product Analysis

Product performance is analyzed using:

* Total Sales
* Total Profit
* Profit Margin
* Product Category
* Performance Segment

Products are classified into four analytical segments:

```text
Star
Review
Growth Opportunity
Low Priority
```

The segmentation considers both:

* Product sales performance
* Product profit margin

This helps identify products that are strong revenue and profitability performers as well as products that may require further review.

---

# Time Intelligence

Power BI time intelligence was implemented using a dedicated `DimDate` table.

The model supports:

* Year
* Month
* Quarter
* Year-Month
* YTD Sales
* YTD Profit
* Previous Year Sales
* Previous Year Profit
* Year-over-Year Sales Growth
* Rolling 12-Month Sales
* Rolling 12-Month Profit

### Year-over-Year Analysis

Because the source data starts in late 2010 and ends in early 2014, only comparable complete-year periods are used for the main YoY comparison.

Validated results include:

```text
2012 vs 2011    -17.43%
2013 vs 2012    179.87%
```

Incomplete comparison periods are intentionally excluded.

---

# Power BI Dashboard

The project includes an interactive Power BI dashboard with five main business pages.

## 1. Overview

Provides an executive summary of:

* Total Sales
* Total Profit
* Profit Margin
* Unique Orders
* Unique Customers
* Average Order Value
* Monthly Sales Trend
* Monthly Profit Trend
* Sales by Year

---

## 2. Sales

Provides detailed sales-performance analysis including:

* Sales
* Profit
* Profit Margin
* Sales YoY %
* Sales Trend
* Sales by Country
* Sales by Product Category
* Year-over-Year Sales Growth

---

## 3. Customers

Provides customer intelligence including:

* Unique Customers
* Total Sales
* Average Order Value
* Average Sales per Record
* Customers by Country
* Top 10 Customers
* Customer Revenue Concentration
* Customer Sales vs Order Frequency
* Customer Sales vs Profit
* Customer Profitability

---

## 4. Products

Provides product and profitability analysis including:

* Total Sales
* Total Profit
* Profit Margin
* Number of Products
* Sales by Product Category
* Sales & Profit by Product Category
* Top 10 Products by Sales
* Top 10 Products by Profit
* Category Profit Margin
* Product Performance Analysis

---

## 5. Insights

Provides management-oriented business insights and recommendations.

The page summarizes:

* Revenue Drivers
* Profit Contribution
* Customer Revenue Concentration
* Top Products by Profit
* Management Recommendations

### Main Recommendations

1. Protect the Bikes revenue base.
2. Expand high-margin Accessories opportunities.
3. Monitor customer revenue concentration.
4. Focus on products with strong sales and profitability.
5. Use Power BI monitoring to support recurring business decisions.

---

# Power BI Navigation

The dashboard uses a page navigator for easy navigation between WITH ARROW TO FORWARD AND BACKWARD PAGE:

```text
EXECUTIVE OVERVIEW | SALES PERFORMANCE | CUSTOMERS INTELLIGENCE | PRODUCTS & PROFITABILITY | MANAGEMENT INSIGHTS
```

A dedicated QA page is also included for internal validation.

---

# Data Quality & QA

A dedicated QA page was created in Power BI to validate the final analytical model.

### Final QA Results

```text
Total Sales        29,358,677.22
Total Cost         17,277,793.58
Total Profit       12,080,883.65
Profit Margin      41.15%
Unique Orders      27,659
Unique Customers   18,484
Sales Records      60,398
Unique Products    130
Missing Values     0
Duplicate Rows     0
Profit Validation  PASS
```

The Power BI results were cross-checked against the established Python/SQL analytical results.

**Cross-system validation: PASS**

---

# Python Analysis

Python was used for:

* Data extraction
* Data cleaning
* Feature engineering
* Exploratory analysis
* KPI calculation
* Business analysis
* Visualization
* Excel reporting

The main Python scripts are located in:

```text
scripts/
```

---

# Data Visualizations

The Python visualization pipeline generates charts for:

* KPI Dashboard
* Yearly Sales Trend
* Yearly Profit Trend
* Yearly Sales vs Profit
* Monthly Sales Trend
* Monthly Profit Trend
* Profit Margin Trend
* Top Countries
* Category Sales
* Category Profit Margin
* Top Products
* Top Customers

Charts are exported automatically to:

```text
reports/charts/
```

---

# Excel Business Report

An Excel analytical report is generated automatically using Python.

The report contains the following sheets:

```text
KPI Summary
Yearly Analysis
Monthly Analysis
Country Analysis
Category Analysis
Product Analysis
Customer Analysis
City Analysis
```

Output file:

```text
reports/AdventureWorks_Analytics_Report.xlsx
```

---

# Project Structure

```text
AdventureWorksDW-Analysis_PowerBI_Excel/
│
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   │
│   └── processed/
│       ├── sales_clean.csv
│       └── sales_featured.csv
│
├── docs/
│   └── project_architecture.md
│
├── notebooks/
│   ├── 01_data_extraction.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda_analysis.ipynb
│   ├── 05_visualization_dashboard.ipynb
│   └── 06_export_excel.ipynb
│
├── powerbi/
│   ├── AdventureworksDashboard.pbix
│   └── Dashboards_Screenshots/
│       ├── P1_Executive_Overview.jpg
│       ├── P2_Sales_Performance.jpg
│       ├── P3_Customer.jpg
│       ├── P3_Customer_Mit_Filter.jpg
│       ├── P4_Product_Profitability.jpg
│       └── P5_Management_Insights.jpg
│
├── reports/
│   ├── charts/
│   │   ├── kpi_dashboard.png
│   │   ├── monthly_sales_trend.png
│   │   ├── monthly_profit_trend.png
│   │   ├── profit_margin_trend.png
│   │   ├── yearly_sales_trend.png
│   │   ├── yearly_profit_trend.png
│   │   ├── yearly_sales_vs_profit.png
│   │   ├── top_countries.png
│   │   ├── category_sales.png
│   │   ├── category_profit_margin.png
│   │   ├── top_products.png
│   │   └── top_customers.png
│   │
│   ├── screenshots/
│   │   ├── monthly_sales_trends.png
│   │   ├── sale_data_table.png
│   │   ├── sales_data_clreaned_table.png
│   │   ├── to_10_products.png
│   │   ├── top_10_countries.png
│   │   ├── top_10_customers.png
│   │   ├── total_rowa.png
│   │   ├── total_sales_and_profit.png
│   │   ├── total_sales_profit.png
│   │   ├── vw_contry_sales.png
│   │   ├── vw_sales_overview.png
│   │   ├── yearly&monthly_sales_trend.png
│   │   └── yearly_trend.png
│   │
│   ├── AdventureWorks_Analytics_Report.xlsx
│   ├── business_reports.pdf
│   └── business_reports.odt
│
├── scripts/
│   ├── 01_data_extraction.py
│   ├── 02_data_cleaning.py
│   ├── 03_feature_engineering.py
│   ├── 04_analysis.py
│   ├── 05_visualization.py
│   └── 06_export_excel.py
│
├── sql/
│   ├── business_queries.sql
│   ├── create_view.sql
│   └── setup_database.sql
│
├── venv/
│
├── .env
├── .gitignore
├── AdventureWorksDW-Analysis_PowerBI.slnx
├── requirements.txt
└── README.md
```

---

# How to Run

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AdventureWorksDW-Analysis_PowerBI_Excel
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure SQL Server

The project expects:

```text
Server: localhost\SQLEXPRESS
Database: AdventureWorksDW2025
Driver: ODBC Driver 17 for SQL Server
```

The database connection is configured through environment variables.

Create a local `.env` file:

```text
SERVER=localhost\SQLEXPRESS
DATABASE=AdventureWorksDW2025
DRIVER=ODBC Driver 17 for SQL Server

DB_SERVER=localhost\SQLEXPRESS
DB_NAME=AdventureWorksDW2025
DB_DRIVER=ODBC Driver 17 for SQL Server
```

**Important:** Never commit `.env` to GitHub.

---

# Run the Analytics Pipeline

Run the scripts in the following order:

### Step 1 — Data Extraction

```bash
python scripts/01_data_extraction.py
```

### Step 2 — Data Cleaning

```bash
python scripts/02_data_cleaning.py
```

### Step 3 — Feature Engineering

```bash
python scripts/03_feature_engineering.py
```

### Step 4 — Business Analysis

```bash
python scripts/04_analysis.py
```

### Step 5 — Visualization

```bash
python scripts/05_visualization.py
```

### Step 6 — Excel Export

```bash
python scripts/06_export_excel.py
```

---

# Power BI

Open:

```text
powerbi/AdventureworksDashboard.pbix
```

The Power BI model uses:

```text
sales_featured
        ↓
DimDate
```

The model includes a dedicated date table and time-intelligence measures.

---

# Key Business Findings

### 1. Strong Overall Profitability

The project generates approximately:

```text
29.36M Total Sales
12.08M Total Profit
41.15% Profit Margin
```

---

### 2. Bikes Drive Revenue

Bikes represent the dominant product category and are responsible for the vast majority of total sales.

This means overall revenue performance is strongly dependent on the Bikes category.

---

### 3. Accessories Have the Highest Margin

Accessories achieve a profit margin of approximately:

```text
62.6%
```

This makes Accessories an important potential growth and profitability opportunity.

---

### 4. Customer Concentration Matters

A relatively small group of customers contributes a significant share of total revenue.

High-value customers should therefore be monitored carefully to reduce revenue concentration risk.

---

### 5. Product Performance Is Uneven

A limited number of products contribute a significant share of total sales and profit.

These products should receive continued attention in:

* Inventory planning
* Product availability
* Commercial strategy
* Profitability management

---

# Future Improvements

Potential future enhancements include:

* Customer segmentation
* Sales forecasting
* Machine learning prediction
* Customer churn analysis
* Streamlit analytics application
* Automated ETL pipelines
* Power BI Service deployment
* Microsoft Fabric integration
* Cloud data warehouse integration
* Automated dashboard refresh
* Advanced anomaly detection
* Advanced DAX and business intelligence features

---

# Portfolio Value

This project demonstrates practical experience across the complete analytics lifecycle:

```text
Database
   ↓
SQL
   ↓
Python
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Business Analysis
   ↓
Excel Reporting
   ↓
Power BI
   ↓
Data Validation
   ↓
Business Insights
```

The project is designed as a portfolio example for roles such as:

* Junior Data Analyst
* Data Analyst
* BI Analyst
* Reporting Analyst
* Power BI Analyst
* Business Intelligence Developer

---

# Author

## Aram Mehraban

**Data Analyst | BI & Reporting | Python | SQL | Power BI | Excel**

This project is part of my Data Analytics and Business Intelligence portfolio.

---

# License

This project is licensed under the MIT License.
