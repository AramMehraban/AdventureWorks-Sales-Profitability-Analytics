USE AdventureWorksDW2025;
GO

-- Total Sales & Profit

SELECT
    SUM(SalesAmount) AS TotalSales,
    SUM(Profit) AS TotalProfit
FROM analytics.Sales_Data_Cleaned;

-- Top Countries

SELECT TOP 10
    Country,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY Country
ORDER BY TotalSales DESC;

-- Top Products

SELECT TOP 10
    ProductName,
    SUM(SalesAmount) AS Revenue
FROM analytics.Sales_Data_Cleaned
GROUP BY ProductName
ORDER BY Revenue DESC;

-- Top Customers

SELECT TOP 10
    CustomerKey,
    FirstName,
    LastName,
    SUM(SalesAmount) AS Revenue
FROM analytics.Sales_Data_Cleaned
GROUP BY CustomerKey, FirstName, LastName
ORDER BY Revenue DESC;

-- Monthly&Yearly Sales Trend

SELECT
    YEAR(OrderDate) AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY OrderYear, OrderMonth;


-- Yearly Sales Trend

SELECT
    YEAR(OrderDate) AS OrderYear,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY YEAR(OrderDate)
ORDER BY OrderYear;

-- Monthly Sales Trend

SELECT
    MONTH(OrderDate) AS OrderMonth,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY MONTH(OrderDate)
ORDER BY OrderMonth;