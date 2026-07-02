
-- ==========================================
-- Customer Churn Prediction System
-- Database Table Creation Script
-- ==========================================

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction TEXT NOT NULL,
    probability REAL NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
