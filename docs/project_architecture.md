# Project Architecture

## Overview

This project follows a modern end-to-end Data Analytics and Business Intelligence workflow built on the AdventureWorksDW2025 database.

The pipeline covers the full lifecycle from raw data extraction to business reporting and dashboard visualization.



# Architecture Flow

## High-Level Pipeline

```text
SQL Server (AdventureWorksDW2025)
            ↓
Python ETL Pipeline (SQLAlchemy + Pandas)
            ↓
Cleaned & Processed Dataset
            ↓
Feature Engineering Layer
            ↓
EDA & KPI Analysis
            ↓
Visualization Layer (Matplotlib / Seaborn)
            ↓
Reporting Layer (Excel / PDF / CSV)
            ↓
Power BI Dashboard


# Data Flow Architecture
## 1. Source Layer (SQL Server)

Database:

AdventureWorksDW2025

Main Tables:

     - FactInternetSales
     - DimCustomer
     - DimProduct
     - DimProductCategory
     - DimProductSubcategory
     - DimGeography



2. Analytics Layer (SQL Schema)

- Schema:
</> SQL
analytics

- Core Table:
</> SQL
analytics.Sales_Data    

- Cleaned Table::
</> SQL
analytics.Sales_Data_Cleaned

- Optional Views:
</> SQL
analytics.vw_sales_overview
analytics.vw_country_sales
analytics.vw_product_performance
analytics.vw_kpi_dashboard


# Python ETL Pipeline
### Step 1 — Data Extraction

File:
scripts/extract_data.py

Purpose:
     - Connect to SQL Server
     - Extract raw sales data
     - Load into Pandas DataFrame

### Step 2 — Data Cleaning

File:
scripts/clean_data.py

Processes:
     - Remove NULL values
     - Remove duplicates
     - Fix data inconsistencies
     - Standardize columns

### Step 3 — Feature Engineering

File:
scripts/feature_engineering.py

Created Features:
     - Profit
     - ProfitMargin
     - OrderYear
     - OrderMonth


### Step 4 — Data Analysis

File:
scripts/analysis.py

Business Logic:
     - KPI calculations
     - Country performance analysis
     - Product performance ranking
     - Customer segmentation insights

### Step 5 — Visualization

File:
scripts/visualization.py

Generated Charts:
     - Sales trend over time
     - Top products
     - Top customers
     - Country-wise performance
     - Profit analysis
     - Monthly & yearly sales

# Reporting Layer

## Generated Outputs:

     - CSV (processed datasets)
     - Excel reports
     - PDF business report
     - PNG charts
     - Power BI dataset integration

Output Folder:
reports/



# Dashboard Layer

Tool:
- Power BI

Features:

     - Interactive KPI dashboard
     - Sales performance overview
     - Product analysis
     - Customer segmentation
     - Country-wise insights


# Technologies Used
     - SQL Server
     - Python
     - Pandas
     - NumPy
     - Matplotlib
     - Seaborn
     - SQLAlchemy
     - PyODBC
     - Power BI
     - Excel
     - Git & GitHub



# Project Structure Logic

The project is designed with a modular architecture:

     - Separation of ETL steps
     - Reusable scripts
     - Scalable data pipeline
     - Clear analytics layer
     - Reproducible reporting system


# Future Improvements

## Planned enhancements:

     - Machine Learning forecasting models
     - Automated ETL scheduling (Airflow)
     - Docker containerization
     - Streamlit dashboard
     - Cloud deployment (Azure / AWS)
     - CI/CD integration for pipeline automation