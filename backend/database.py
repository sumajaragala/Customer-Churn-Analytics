import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).resolve().parent / "churn.db"


# =====================================
# CREATE DATABASE TABLE
# =====================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction TEXT,
            probability REAL,
            risk_level TEXT
        )
    """)

    conn.commit()
    conn.close()


# =====================================
# SAVE PREDICTION
# =====================================

def save_prediction(prediction, probability, risk_level):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (prediction, probability, risk_level)
        VALUES (?, ?, ?)
    """, (prediction, probability, risk_level))

    conn.commit()
    conn.close()