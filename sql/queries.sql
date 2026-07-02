-- ==========================================
-- Useful SQL Queries
-- ==========================================

-- View all predictions
SELECT * FROM predictions;

-------------------------------------------------

-- Total Predictions
SELECT COUNT(*) AS Total_Predictions
FROM predictions;

-------------------------------------------------

-- Total Churn Customers
SELECT COUNT(*) AS Churn_Customers
FROM predictions
WHERE prediction='Churn';

-------------------------------------------------

-- Total Safe Customers
SELECT COUNT(*) AS Safe_Customers
FROM predictions
WHERE prediction='No Churn';

-------------------------------------------------

-- Average Probability
SELECT ROUND(AVG(probability),2) AS Average_Probability
FROM predictions;

-------------------------------------------------

-- Highest Risk Customers
SELECT *
FROM predictions
ORDER BY probability DESC;

-------------------------------------------------

-- Latest Prediction
SELECT *
FROM predictions
ORDER BY id DESC
LIMIT 1;

-------------------------------------------------

-- High Risk Customers (>70%)
SELECT *
FROM predictions
WHERE probability > 70;

-------------------------------------------------

-- Medium Risk Customers (40% - 70%)
SELECT *
FROM predictions
WHERE probability BETWEEN 40 AND 70;

-------------------------------------------------

-- Low Risk Customers (<40%)
SELECT *
FROM predictions
WHERE probability < 40;

-------------------------------------------------

-- Count by Risk Level
SELECT risk_level,
COUNT(*) AS Total
FROM predictions
GROUP BY risk_level;

-------------------------------------------------

-- Count by Prediction
SELECT prediction,
COUNT(*) AS Total
FROM predictions
GROUP BY prediction;

-------------------------------------------------

-- Delete All Records (Use Carefully)
DELETE FROM predictions;

-------------------------------------------------

-- Reset Auto Increment
DELETE FROM sqlite_sequence
WHERE name='predictions';

DELETE FROM predictions
WHERE id = 15;