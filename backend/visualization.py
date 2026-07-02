from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "dataset" / "customer_churn_clean.csv"

df = pd.read_csv(file_path)

# Churn Distribution
plt.figure(figsize=(6,4))
sns.countplot(x="Churn Label", data=df , hue="Churn Label")

plt.title("Customer Churn Distribution")
plt.show()

# Gender vs Churn

plt.figure(figsize=(6,4))
sns.countplot(x="Gender", hue="Churn Label", data=df)

plt.title("Gender vs Churn")
plt.show()

plt.figure(figsize=(8,5))
sns.countplot(x="Contract", hue="Churn Label", data=df)
plt.title("Contract Type vs Churn")
plt.xticks(rotation=15)
plt.show()


plt.figure(figsize=(8,5))
sns.countplot(x="Internet Service", hue="Churn Label", data=df)
plt.title("Internet Service vs Churn")
plt.show()


plt.figure(figsize=(10,5))
sns.countplot(x="Payment Method", hue="Churn Label", data=df)
plt.title("Payment Method vs Churn")
plt.xticks(rotation=30)
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["Monthly Charges"], bins=30)
plt.title("Monthly Charges Distribution")
plt.show()