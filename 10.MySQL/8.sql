USE churn;

SELECT product_name, product_id, DATEDIFF(SYSDATE(), order_date)
AS date_difference, order_date FROM transaction;

SELECT DATE_FORMAT(order_date, '%M'), order_date FROM transaction;

SELECT DAY(order_date), order_date FROM transaction;

SELECT QUARTER(order_date), order_date FROM transaction;

SELECT ADDDATE('2026-01-01', INTERVAL 10 YEAR);

SELECT SUBDATE('2026-01-01', INTERVAL 10 DAY)