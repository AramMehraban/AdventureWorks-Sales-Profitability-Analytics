USE AdventureWorksDW2025;
GO

CREATE OR ALTER VIEW analytics.vw_sales_overview AS

SELECT
    SalesOrderNumber,
    OrderDate,
    Country,
    City,
    ProductCategoryName,
    ProductName,
    CustomerKey,
    FirstName,
    LastName,
    SalesAmount,
    TotalProductCost,
    Profit

FROM analytics.Sales_Data_Cleaned;




CREATE OR ALTER VIEW analytics.vw_country_sales AS

SELECT
    Country,
    COUNT(DISTINCT SalesOrderNumber) AS TotalOrders,
    SUM(SalesAmount) AS TotalSales,
    SUM(Profit) AS TotalProfit

FROM analytics.Sales_Data_Cleaned

GROUP BY Country;
