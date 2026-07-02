from pathlib import Path
import pandas as pd

# ===================================
# Load Dataset
# ===================================

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "dataset" / "Telco_customer_churn.xlsx"

df = pd.read_excel(input_file)

# ===================================
# Data Cleaning
# ===================================

# Convert Total Charges to numeric
df["Total Charges"] = pd.to_numeric(
    df["Total Charges"],
    errors="coerce"
)

# Fill missing values
df["Total Charges"] = df["Total Charges"].fillna(0)

# Remove unnecessary columns
columns_to_drop = [
    "CustomerID",
    "Count",
    "Country",
    "State"
]

df.drop(columns=columns_to_drop, inplace=True)

# ===================================
# Save Cleaned Dataset
# ===================================

output_file = BASE_DIR / "dataset" / "customer_churn_clean.csv"

df.to_csv(output_file, index=False)

print("=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nClean dataset saved successfully!")

print(output_file)