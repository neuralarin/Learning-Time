USE classicmodels;

SELECT * FROM products;

CREATE TABLE productLinemsrp AS 
SELECT 
    sum(msrp) AS total_msrp, 
    productLine 
FROM products 
GROUP BY productLine;

SELECT * FROM productLinemsrp;

SELECT 
    productLine, 
    productName, 
    msrp,
    SUM(msrp) OVER (PARTITION BY productLine) as total_msrp_per_line 
FROM products;

SELECT 
    productName,
    quantityInStock, 
    RANK() OVER (ORDER BY quantityInStock) as stock_rank 
FROM products;

SELECT *, productCode FROM products ORDER BY buyPrice desc limit 1;
select * from products;