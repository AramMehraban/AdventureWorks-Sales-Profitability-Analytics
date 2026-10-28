# AdventureWorks Sales & Profitability Analytics

**End-to-End Business Intelligence & Data Analytics Portfolio Project**

[**Launch Interactive Dashboard →**](https://adventureworks-sales-analytics.streamlit.app/) · [**View Source Code →**](https://github.com/AramMehraban/AdventureWorks-Sales-Profitability-Analytics)

**Project focus:** Sales Analytics · Profitability · Data Quality · Business Intelligence

**Status:** Portfolio project — core analytics workflow and interactive dashboard available.

## Project Overview

This project demonstrates an end-to-end analytics workflow using Microsoft SQL Server, Python, Power BI, Excel, and Streamlit.

Using the AdventureWorksDW2025 sample data warehouse, I developed a workflow for data extraction, cleaning, validation, feature engineering, business analysis, KPI development, reporting, and interactive visualization.

The analysis focuses on sales performance, product profitability, customer revenue, geographical trends, and management reporting.

## Key Results

| KPI | Result |
|---|---:|
| Sales Records | 60,398 |
| Unique Orders | 27,659 |
| Unique Customers | 18,484 |
| Unique Products | 130 |
| Countries Represented | 6 |
| Total Sales | 29,358,677.22 |
| Total Cost | 17,277,793.58 |
| Total Profit | 12,080,883.65 |
| Overall Profit Margin | 41.15% |
| Average Order Value | 1,061.45 |

*Currency note: Monetary values retain the numeric units of the source dataset. No currency conversion has been performed.*

Sales records represent individual analytical rows, not distinct orders.

## Live Interactive Dashboard

**[Explore the Streamlit Dashboard →](https://adventureworks-sales-analytics.streamlit.app/)**

The browser-based application presents selected analytical results without requiring a local Python or Power BI installation.

Features include:
- Executive KPI overview
- Sales and profitability analysis
- Product and category comparisons
- Country-level performance
- Interactive filters and visualizations
- Business insights

The application is a portfolio demonstration, not a live operational reporting system.

## Business Questions

This project investigates the following questions:

1. How do sales and profit change over time?
2. Which countries and product categories generate the most revenue?
3. Which products contribute most to sales and profitability?
4. Which customers generate the highest revenue?
5. How concentrated is revenue among high-value customers?
6. Which product categories have the highest profit margins?
7. How does sales performance change year over year?
8. Which areas deserve further management attention?

## Selected Business Findings

- **Bikes** are the dominant revenue category, generating approximately 28.32 million in sales.
- Bikes account for approximately 96.46% of total sales.
- **Accessories** have the highest reported category profit margin, at approximately 62.60%.
- Overall reported profit margin is 41.15%.
- Customer revenue concentration and product performance segmentation provide additional perspectives for business analysis.

These findings are based on the sample dataset and should be interpreted within its business context.

## Analytics Workflow

```text
SQL Server
AdventureWorksDW2025
        |
        v
Data Extraction
        |
        v
Python: Cleaning & Validation
        |
        v
Feature Engineering
        |
        +--------------------+
        |                    |
        v                    v
Python Analytics       Power BI & DAX
        |                    |
        v                    v
Charts & Excel         Interactive Report
        |                    |
        +----------+---------+
                   |
                   v
           Business Insights
                   |
                   v
          Streamlit Dashboard
```

## Data Preparation & Quality

Python is used to validate data types, dates, identifiers, sales values, costs, profits, and duplicate rows.

Reported validation results:

| Quality Check | Result |
|---|---:|
| Records after cleaning | 60,398 |
| Missing values | 0 |
| Duplicate rows | 0 |
| Invalid dates | 0 |
| Missing customer keys | 0 |
| Profit calculation validation | PASS |

Profit is calculated as:

`Profit = SalesAmount - TotalProductCost`

The cleaned dataset contains 12 columns. Feature engineering expands it to 17 columns, including year, month, year-month, and profit margin fields.

## Power BI Report

The report contains five business pages and a dedicated quality-assurance page.

| Report Page | Purpose |
|---|---|
| Executive Overview | Core KPIs and overall performance |
| Sales Performance | Trends, countries, categories, and growth |
| Customer Intelligence | Customer revenue and concentration |
| Product & Profitability | Product rankings and margins |
| Management Insights | Findings and recommendations |
| QA | KPI consistency and data-quality checks |

The model includes a dedicated date table and DAX measures for total sales, cost, profit, profit margin, unique orders, unique customers, average order value, year-to-date metrics, year-over-year growth, and rolling 12-month performance.

**Power BI file:** `powerbi/AdventureworksDashboard.pbix`

## Technology Stack

| Area | Technologies |
|---|---|
| Database & Querying | Microsoft SQL Server, SQL |
| Data Processing | Python, Pandas, NumPy |
| Business Intelligence | Power BI, DAX, Power Query |
| Visualization | Matplotlib, Seaborn, Plotly |
| Interactive Dashboard | Streamlit |
| Reporting | Excel, OpenPyXL, XlsxWriter |
| Database Connectivity | SQLAlchemy, pyodbc |
| Development | Jupyter Notebook, VS Code, Git, GitHub |

## Data Source

The project uses the AdventureWorksDW2025 sample data warehouse, including:

- `FactInternetSales`
- `DimProduct`
- `DimProductSubcategory`
- `DimProductCategory`
- `DimCustomer`
- `DimGeography`

The dataset covers the period from 2010-12-29 to 2014-01-28.

This is an educational and portfolio project using sample data. It does not represent the actual financial performance of a real operating business.

## Run Locally

### Prerequisites

- Python 3.11 or compatible version
- Microsoft SQL Server and AdventureWorksDW2025
- Microsoft ODBC Driver for SQL Server
- Power BI Desktop (for the Power BI report)

### 1. Clone the repository

```bash
git clone https://github.com/AramMehraban/AdventureWorks-Sales-Profitability-Analytics.git
cd AdventureWorks-Sales-Profitability-Analytics
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Configure your local SQL Server connection using the environment variables expected by the project scripts.

Keep credentials and local `.env` files out of GitHub.

### 5. Run the dashboard

```bash
python -m streamlit run app.py
```

The data extraction scripts require access to a configured SQL Server instance and the sample database.

## Limitations & Future Improvements

Potential extensions include:

- Automated ETL execution and scheduled refresh
- Automated regression tests for KPI calculations
- Additional dimensional modeling
- Enhanced dashboard drill-through and tooltips
- Power BI Service deployment, subject to licensing and account requirements

These are potential improvements, not claims about existing functionality.

## About the Author

**Aram Mehraban**

Data Analytics · Business Intelligence · SQL · Python · Power BI · Excel

- [GitHub Profile](https://github.com/AramMehraban)
- [LinkedIn](https://www.linkedin.com/in/arammehraban/)
- [Live Dashboard](https://adventureworks-sales-analytics.streamlit.app/)

---

*This portfolio project demonstrates practical work in data preparation, analytical problem-solving, KPI development, business reporting, data validation, and interactive visualization.*
