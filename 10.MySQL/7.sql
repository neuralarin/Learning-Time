CREATE DATABASE churn;

USE churn;

-- Count by Gender
SELECT Gender, count(*) as Count 
FROM churn_data 
GROUP BY Gender;

-- Count by Credit Card Status AND Gender
SELECT HasCrCard, Gender, count(*) as Count 
FROM churn_data 
GROUP BY HasCrCard, Gender
ORDER BY HasCrCard ASC;

SELECT COUNT(Geography) FROM churn_data;

SELECT Geography, COUNT(*) FROM churn_data WHERE Geography='France';

SELECT MIN(Age) FROM churn_data;

SELECT MAX(Age) FROM churn_data;

SELECT SUM(Balance) FROM churn_data;

SELECT AVG(Balance) FROM churn_data;