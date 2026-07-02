import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "churn.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Delete the record with ID 15
cursor.execute("DELETE FROM predictions WHERE id = ?", (16,))

conn.commit()
conn.close()

print("Record deleted successfully!")