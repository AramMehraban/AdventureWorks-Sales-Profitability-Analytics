# AdventureWorks Sales & Profitability Analytics

**End-to-End Business Intelligence & Data Analytics Portfolio Project**

[![Open Interactive Streamlit Dashboard](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)

**[Launch the Live Interactive Dashboard](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)** · **[View the GitHub Repository](https://github.com/AramMehraban/AdventureWorks-Sales-Profitability-Analytics)**

This project demonstrates an end-to-end analytics workflow using Microsoft SQL Server, Python, Excel, Power BI, and Streamlit. It covers data extraction, data quality validation, feature engineering, exploratory analysis, KPI development, interactive dashboards, automated reporting, and actionable business insights.

The analysis focuses on sales performance, profitability, product categories, customer behavior, geographical performance, and management reporting.

## Live Interactive Dashboard

**Explore the browser-based dashboard without installing Python or Power BI Desktop.**

[**Open AdventureWorks Sales & Profitability Analytics →**](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)

The Streamlit application provides an online portfolio demonstration of the project's analytical results.

Key capabilities include:
- Interactive business KPI overview
- Sales and profitability analysis
- Product and category performance
- Country and geographical comparisons
- Interactive charts and filters
- Data-driven business insights

The online application is a portfolio presentation of the analytical project. It is separate from a live operational reporting system.

## Project Highlights

- End-to-end analytics pipeline using SQL Server and Python
- Data cleaning, validation, and feature engineering
- Exploratory data analysis and business KPI calculation
- Automated chart generation and Excel reporting
- Interactive Power BI dashboard with five business pages
- DAX measures, date modeling, and time intelligence
- Customer revenue concentration and product performance segmentation
- Cross-checking of core Power BI KPIs against validated analytical results
- Browser-based dashboard demonstration using Streamlit and Plotly

## Dashboard

### Streamlit Dashboard

**Live demo:** [Open the interactive dashboard](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)

### Power BI Report

The Power BI report contains five main business pages and a dedicated internal QA page.

| Dashboard page | Business purpose |
|---|---|
| **Executive Overview** | Executive KPIs, sales and profit trends, orders, customers, and average order value |
| **Sales Performance** | Sales trends, country performance, product categories, and year-over-year growth |
| **Customer Intelligence** | Customer revenue, order frequency, profitability, and revenue concentration |
| **Product & Profitability** | Product rankings, category performance, margins, and product performance segments |
| **Management Insights** | Business findings, revenue drivers, profitability, and management recommendations |
| **QA** | Internal KPI, data quality, and profit validation checks |

**Power BI report file:** `powerbi/AdventureworksDashboard.pbix`

Open the file using Power BI Desktop. A separate Power BI Service link can be added if the report is published online.

## Technology Stack

| Area | Technologies |
|---|---|
| Database | Microsoft SQL Server |
| Querying | SQL, joins, analytical queries, database views |
| Data processing | Python, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Business Intelligence | Power BI, DAX, Power Query |
| Interactive web dashboard | Streamlit |
| Reporting | Microsoft Excel, OpenPyXL, XlsxWriter |
| Database connectivity | SQLAlchemy, pyodbc |
| Development | Jupyter Notebook, VS Code, Git, GitHub |

## Data Source

The project uses the **AdventureWorksDW2025** sample data warehouse.

The extraction query combines data from:

- `FactInternetSales`
- `DimProduct`
- `DimProductSubcategory`
- `DimProductCategory`
- `DimCustomer`
- `DimGeography`

The resulting analytical dataset contains sales transactions enriched with product, customer, product-category, and geographical attributes.

This is a sample-data portfolio project, not a live reporting system for an operational business.

## End-to-End Data Pipeline

```text
SQL Server: AdventureWorksDW2025
                 |
                 v
          Data Extraction
                 |
                 v
       data/raw/sales_data.csv
                 |
                 v
       Data Cleaning & QA
                 |
                 v
     sales_clean.csv (12 columns)
                 |
                 v
        Feature Engineering
                 |
                 v
   sales_featured.csv (17 columns)
                 |
          +------+------+
          |             |
          v             v
   Python Analysis   Power BI
          |             |
          v             v
  Charts & Insights  Interactive
          |          Dashboard
          v
   Excel Reporting
          |
          v
  Business Recommendations

          |
          v
  Streamlit Web Dashboard
  Online Portfolio Demonstration
```

## Dataset Overview

The final extracted dataset contains **60,398 sales records**.

| Dataset metric | Result |
|---|---:|
| Sales records | 60,398 |
| Source columns | 12 |
| Feature-engineered columns | 17 |
| Unique orders | 27,659 |
| Unique customers | 18,484 |
| Unique products | 130 |
| Countries represented | 6 |
| Order date range | 2010-12-29 to 2014-01-28 |

**Important distinction:** Sales records represent individual dataset rows. They are not the same as unique orders.

## Data Extraction

Sales data is extracted from SQL Server using SQL queries and Python.

The extraction script:

- Connects to the configured SQL Server database
- Joins sales with product, customer, category, and geography information
- Calculates profit from sales and product cost
- Validates the extracted dataset
- Exports the raw analytical dataset

Output:

`data/raw/sales_data.csv`

Main script:

`scripts/01_data_extraction.py`

## Data Cleaning and Validation

Python is used to validate data types, dates, identifiers, sales values, costs, profits, and duplicate rows.

The cleaning process includes:

- Data type validation
- Invalid-date checks
- Missing-value checks
- Duplicate-row checks
- Sales order and customer identifier validation
- Sales, cost, and profit validation
- Profit calculation consistency checks
- Validation of negative values against the project's business rules

### Data Quality Results

| Check | Result |
|---|---:|
| Rows after cleaning | 60,398 |
| Columns | 12 |
| Missing values | 0 |
| Duplicate rows | 0 |
| Invalid dates | 0 |
| Missing order numbers | 0 |
| Missing customer keys | 0 |
| Negative sales amounts | 0 |
| Negative product costs | 0 |
| Negative profit values | 0 |
| Profit calculation validation | PASS |

Profit is validated using:

`Profit = SalesAmount - TotalProductCost`

Output:

`data/processed/sales_clean.csv`

Main script:

`scripts/02_data_cleaning.py`

## Feature Engineering

The feature-engineering stage adds fields for time-based analysis and profitability reporting.

| Feature | Purpose |
|---|---|
| `OrderYear` | Annual analysis |
| `OrderMonthNumber` | Correct chronological month sorting |
| `OrderMonth` | Month-level reporting |
| `OrderYearMonth` | Monthly trend analysis |
| `ProfitMargin` | Record-level profitability analysis |

The final feature-engineered dataset contains **60,398 rows and 17 columns**.

Output:

`data/processed/sales_featured.csv`

Main script:

`scripts/03_feature_engineering.py`

## Business Questions

The analysis addresses the following questions:

1. What are the total sales, costs, and profit?
2. How do sales and profit change over time?
3. Which countries generate the highest sales?
4. Which product categories drive revenue?
5. Which products generate the highest sales and profit?
6. Which customers contribute the most revenue?
7. How concentrated is revenue among high-value customers?
8. Which product categories have the highest profit margins?
9. How does sales performance change year over year?
10. Which products and business areas deserve management attention?

## Key Business KPIs

The following values were validated during the project.

| KPI | Validated result |
|---|---:|
| Total Sales | 29,358,677.22 |
| Total Cost | 17,277,793.58 |
| Total Profit | 12,080,883.65 |
| Profit Margin | 41.15% |
| Sales Records | 60,398 |
| Unique Orders | 27,659 |
| Unique Customers | 18,484 |
| Unique Products | 130 |
| Average Order Value | 1,061.45 |
| Average Sales per Record | 486.09 |

*Currency note: The report preserves the monetary values from the source dataset's numeric fields. No currency conversion has been performed, so no EUR or USD conversion is claimed.*

## Business Analysis and Findings

### 1. Sales Performance

The dataset contains approximately 29.36 million in total sales and 12.08 million in total profit, with an overall profit margin of 41.15%.

Sales and profitability are analyzed by year, month, country, and product category.

### 2. Product Category Performance

The three main product categories are:

- Bikes
- Accessories
- Clothing

Key findings:

- **Bikes** are the dominant revenue category, with approximately 28.32 million in sales.
- Bikes account for approximately 96.46% of total sales.
- **Accessories** achieve the highest category profit margin at approximately 62.60%.
- Bikes have a profit margin of approximately 40.63%.
- Clothing has a profit margin of approximately 40.15%.

These results indicate that Bikes are the main revenue driver, while Accessories represent an important high-margin category.

### 3. Customer Intelligence

Customer analysis covers:

- Customer revenue
- Order frequency
- Customer profitability
- Top customers by sales
- Revenue concentration among the top 10, 50, 100, and 500 customers

The analysis supports the identification of high-value customer groups and highlights the importance of monitoring revenue concentration.

### 4. Product Performance Segmentation

The product analysis classifies products into four performance segments:

- `Star`
- `Review`
- `Growth Opportunity`
- `Low Priority`

The segmentation compares product sales performance with product profit margin, helping distinguish strong performers from products that may require further review.

These segments are analytical categories, not independently verified business decisions.

### 5. Management Recommendations

Based on the analyzed results, the dashboard highlights the following management priorities:

1. Protect the Bikes revenue base.
2. Evaluate opportunities to expand high-margin Accessories.
3. Monitor customer revenue concentration.
4. Maintain availability of high-performing products.
5. Review product profitability alongside sales volume.
6. Use consistent KPI monitoring to support recurring business decisions.

These recommendations are derived from the sample dataset and should be evaluated against business context before real-world implementation.

## Time Intelligence in Power BI

A dedicated `DimDate` table supports date-based analysis.

The model includes:

- Year
- Month and month number
- Quarter
- Year-Month
- Sales YTD
- Profit YTD
- Previous-year sales and profit
- Year-over-year sales growth
- Rolling 12-month sales
- Rolling 12-month profit

### Year-over-Year Validation

The source data starts in late 2010 and ends in early 2014. Therefore, incomplete comparison periods are excluded from the main YoY growth measure.

| Comparison | Sales YoY |
|---|---:|
| 2012 vs 2011 | -17.43% |
| 2013 vs 2012 | 179.87% |

The measure returns blank for excluded periods rather than presenting an incomplete comparison as a full-year result.

## Power BI Data Model

The Power BI report uses the feature-engineered sales dataset and a dedicated date table.

```text
DimDate
   |
   | 1 : *
   v
sales_featured
```

The active relationship connects:

`DimDate[Date]` → `sales_featured[OrderDate]`

Core DAX measures include:

- `Total Sales`
- `Total Cost`
- `Total Profit`
- `Profit Margin %`
- `Sales Records`
- `Unique Orders`
- `Unique Customers`
- `Average Order Value`
- `Average Sales per Record`
- `Sales YTD`
- `Profit YTD`
- `Sales YoY %`
- `Rolling 12M Sales`
- `Rolling 12M Profit`

## Python Analysis and Visualizations

Python is used for KPI calculation, business analysis, chart generation, and report preparation.

The visualization pipeline generates 12 charts:

- KPI dashboard
- Yearly sales trend
- Yearly profit trend
- Yearly sales versus profit
- Monthly sales trend
- Monthly profit trend
- Profit margin trend
- Top countries
- Category sales
- Category profit margin
- Top products
- Top customers

Output directory:

`reports/charts/`

Main scripts:

- `scripts/04_analysis.py`
- `scripts/05_visualization.py`

## Excel Business Report

The Excel reporting pipeline creates a workbook containing eight analytical sheets:

1. KPI Summary
2. Yearly Analysis
3. Monthly Analysis
4. Country Analysis
5. Category Analysis
6. Product Analysis
7. Customer Analysis
8. City Analysis

Output:

`reports/AdventureWorks_Analytics_Report.xlsx`

Main script:

`scripts/06_export_excel.py`

## Data Quality and Cross-System Validation

The dedicated Power BI QA page displays the core KPI results and data quality checks.

### Final QA Results

| Validation | Result |
|---|---:|
| Total Sales | 29,358,677.22 |
| Total Cost | 17,277,793.58 |
| Total Profit | 12,080,883.65 |
| Profit Margin | 41.15% |
| Unique Orders | 27,659 |
| Unique Customers | 18,484 |
| Sales Records | 60,398 |
| Unique Products | 130 |
| Missing Values | 0 |
| Duplicate Rows | 0 |
| Profit Validation | PASS |

**Validation status:** Core Power BI KPI values match the established analytical reference values from the Python/SQL workflow.

## Repository Structure

```text
AdventureWorksDW-Analysis_PowerBI_Excel/
│
├── app.py
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── sales_data.csv
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
│   └── Dashboards_Screenshot/
│
├── reports/
│   ├── charts/
│   ├── screenshots/
│   ├── analysis/
│   └── AdventureWorks_Analytics_Report.xlsx
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
├── .env.example
├── .gitignore
└── README.md
```

*The directory listing describes the intended project structure. Actual files may vary depending on which generated reports and datasets are committed to the repository.*

## Getting Started

### Prerequisites

- Python 3.11 or a compatible version
- Microsoft SQL Server with the AdventureWorksDW2025 database
- Microsoft ODBC Driver for SQL Server
- Power BI Desktop
- Microsoft Excel or a compatible spreadsheet application

### 1. Clone the Repository

```bash
git clone https://github.com/AramMehraban/AdventureWorks-Sales-Profitability-Analytics.git
cd AdventureWorks-Sales-Profitability-Analytics
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database Connection

Create a local `.env` file using `.env.example` as a template.

Example:

```dotenv
SERVER=localhost\SQLEXPRESS
DATABASE=AdventureWorksDW2025
DRIVER=ODBC Driver 17 for SQL Server

DB_SERVER=localhost\SQLEXPRESS
DB_NAME=AdventureWorksDW2025
DB_DRIVER=ODBC Driver 17 for SQL Server
```

Adjust the connection settings to match your SQL Server installation.

**Security:** Never commit `.env`, database credentials, or other secrets to GitHub.

### 5. Run the Analytics Pipeline

Run the scripts from the project root in this order:

```bash
python scripts/01_data_extraction.py
python scripts/02_data_cleaning.py
python scripts/03_feature_engineering.py
python scripts/04_analysis.py
python scripts/05_visualization.py
python scripts/06_export_excel.py
```

The extraction step requires access to a configured SQL Server instance and the source database.

### 6. Run the Streamlit Dashboard Locally

From the project root:

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser. Its online version is available here:

[**Live Streamlit Dashboard**](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)

### 7. Open the Power BI Report

Open:

`powerbi/AdventureworksDashboard.pbix`

If the repository is moved to another computer, update the Power BI data source path as necessary and refresh the report.

## Project Deliverables

- SQL extraction and analytical queries
- Python data extraction and transformation scripts
- Cleaned and feature-engineered datasets
- Business analysis and KPI calculations
- Automated data visualizations
- Excel reporting workbook
- Interactive Power BI dashboard
- Browser-based Streamlit dashboard
- Data quality validation and business recommendations

## Limitations and Future Improvements

Potential future enhancements include:

- Automated ETL execution and scheduled refresh
- Automated regression tests for KPI calculations
- Dedicated customer and product dimension tables
- Additional drill-through and report tooltip functionality
- Power BI Service deployment, subject to account and licensing requirements
- Additional datasets for broader business analysis

These items are potential extensions, not claims about features already implemented.

## Portfolio Relevance

This project demonstrates practical work across the analytics lifecycle:

```text
SQL Server
    ↓
SQL & Data Extraction
    ↓
Python Data Cleaning
    ↓
Feature Engineering
    ↓
Exploratory Analysis
    ↓
Excel Reporting
    ↓
Power BI & DAX
    ↓
Data Validation
    ↓
Streamlit Web Dashboard
    ↓
Business Insights
```

Relevant roles include:

- Junior Data Analyst
- Data Analyst
- BI Analyst
- Reporting Analyst
- Power BI Analyst
- Business Intelligence Developer

## Author

**Aram Mehraban**

Data Analyst | Business Intelligence | SQL | Python | Power BI | Excel | GIS

- **GitHub:** [AramMehraban](https://github.com/AramMehraban)
- **LinkedIn:** [Aram Mehraban](https://www.linkedin.com/in/arammehraban/)
- **Live Dashboard:** [AdventureWorks Sales & Profitability Analytics](https://adventureworks-sales-profitability-analytics-jjrjxwdkcbdlqkrxj.streamlit.app/)

---

*This repository is a portfolio project demonstrating data extraction, data quality validation, analytics, reporting, and business intelligence development.*