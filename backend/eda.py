from pathlib import Path
import pandas as pd

# ==========================
# Load Cleaned Dataset
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "dataset" / "customer_churn_clean.csv"

df = pd.read_csv(file_path)

print("="*60)
print("DATASET OVERVIEW")
print("="*60)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())

print("\nTarget Variable:")
print(df["Churn Label"].value_counts())