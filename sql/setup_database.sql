USE AdventureWorksDW2025;
GO

IF NOT EXISTS (
    SELECT *
    FROM sys.schemas
    WHERE name = 'analytics'
)
BEGIN
    EXEC('CREATE SCHEMA analytics');
END
GO

IF OBJECT_ID('analytics.Sales_Data_Cleaned', 'U') IS NOT NULL
BEGIN
    DROP TABLE analytics.Sales_Data_Cleaned;
END
GO

IF OBJECT_ID('analytics.Sales_Data', 'U') IS NOT NULL
BEGIN
    DROP TABLE analytics.Sales_Data;
END
GO

SELECT
    f.SalesOrderNumber,
    f.OrderDate,

    d.EnglishProductName AS ProductName,

    pc.EnglishProductCategoryName AS ProductCategoryName,

    c.CustomerKey,
    c.FirstName,
    c.LastName,

    g.City,
    g.EnglishCountryRegionName AS Country,

    f.SalesAmount,
    f.TotalProductCost,

    (
        f.SalesAmount
        - f.TotalProductCost
    ) AS Profit

INTO analytics.Sales_Data

FROM FactInternetSales AS f

INNER JOIN DimProduct AS d
    ON f.ProductKey = d.ProductKey

INNER JOIN DimProductSubcategory AS s
    ON d.ProductSubcategoryKey = s.ProductSubcategoryKey

INNER JOIN DimProductCategory AS pc
    ON s.ProductCategoryKey = pc.ProductCategoryKey

INNER JOIN DimCustomer AS c
    ON f.CustomerKey = c.CustomerKey

INNER JOIN DimGeography AS g
    ON c.GeographyKey = g.GeographyKey;
GO

DELETE FROM analytics.Sales_Data
WHERE SalesAmount IS NULL
   OR OrderDate IS NULL;
GO

SELECT *
INTO analytics.Sales_Data_Cleaned
FROM analytics.Sales_Data;
GO

SELECT COUNT(*) AS TotalRows
FROM analytics.Sales_Data_Cleaned;

SELECT
    SUM(CASE WHEN SalesAmount IS NULL THEN 1 ELSE 0 END)
        AS MissingSalesAmount,

    SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END)
        AS MissingOrderDate
FROM analytics.Sales_Data_Cleaned;

SELECT COUNT(*) AS DuplicateRows
FROM
(
    SELECT
        SalesOrderNumber,
        OrderDate,
        ProductName,
        CustomerKey,
        SalesAmount,
        TotalProductCost,
        COUNT(*) AS DuplicateCount

    FROM analytics.Sales_Data_Cleaned

    GROUP BY
        SalesOrderNumber,
        OrderDate,
        ProductName,
        CustomerKey,
        SalesAmount,
        TotalProductCost

    HAVING COUNT(*) > 1
) AS duplicates;

SELECT COUNT(*) AS NegativeProfitRows
FROM analytics.Sales_Data_Cleaned
WHERE Profit < 0;

SELECT
    SUM(SalesAmount) AS TotalSales,
    SUM(Profit) AS TotalProfit
FROM analytics.Sales_Data_Cleaned;

SELECT TOP 10
    Country,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY Country
ORDER BY TotalSales DESC;

SELECT TOP 10
    ProductName,
    SUM(SalesAmount) AS Revenue
FROM analytics.Sales_Data_Cleaned
GROUP BY ProductName
ORDER BY Revenue DESC;

SELECT TOP 10
    CustomerKey,
    FirstName,
    LastName,
    SUM(SalesAmount) AS Revenue
FROM analytics.Sales_Data_Cleaned
GROUP BY
    CustomerKey,
    FirstName,
    LastName
ORDER BY Revenue DESC;

SELECT
    YEAR(OrderDate) AS OrderYear,
    MONTH(OrderDate) AS OrderMonth,
    SUM(SalesAmount) AS TotalSales
FROM analytics.Sales_Data_Cleaned
GROUP BY
    YEAR(OrderDate),
    MONTH(OrderDate)
ORDER BY
    OrderYear,
    OrderMonth;

SELECT
    YEAR(OrderDate) AS OrderYear,
    SUM(SalesAmount) AS TotalSales,
    SUM(Profit) AS TotalProfit
FROM analytics.Sales_Data_Cleaned
GROUP BY
    YEAR(OrderDate)
ORDER BY
    OrderYear;