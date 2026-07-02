from pathlib import Path
import pandas as pd
import joblib

# =====================================
# Load Dataset
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "dataset" / "customer_churn_clean.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 60)

print("Original Shape:", df.shape)

# =====================================
# Drop Unnecessary Columns
# =====================================

columns_to_drop = [
    "City",
    "Zip Code",
    "Lat Long",
    "Latitude",
    "Longitude",
    "Churn Label",
    "Churn Reason",
    "Churn Score",
    "CLTV"
]

df.drop(columns=columns_to_drop, inplace=True)

print("\nShape After Dropping Columns:", df.shape)

# =====================================
# Encode Categorical Columns
# =====================================

df = pd.get_dummies(df)

print("\nEncoding Completed Successfully!")

print("\nFinal Columns:")
print(df.columns.tolist())

# =====================================
# SELECT ONLY IMPORTANT FEATURES
# =====================================

selected_features = [
    "Tenure Months",
    "Monthly Charges",
    "Total Charges",

    "Internet Service_DSL",
    "Internet Service_Fiber optic",
    "Internet Service_No",

    "Online Security_No",
    "Online Security_No internet service",
    "Online Security_Yes",

    "Tech Support_No",
    "Tech Support_No internet service",
    "Tech Support_Yes",

    "Contract_Month-to-month",
    "Contract_One year",
    "Contract_Two year",

    "Payment Method_Bank transfer (automatic)",
    "Payment Method_Credit card (automatic)",
    "Payment Method_Electronic check",
    "Payment Method_Mailed check"
]

X = df[selected_features]
y = df["Churn Value"]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

# =====================================
# Train-Test Split
# =====================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Shape:", X_train.shape)
print("Testing Shape:", X_test.shape)

# =====================================
# Train Model
# =====================================

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel Trained Successfully!")

# =====================================
# Evaluation
# =====================================

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y_pred = model.predict(X_test)

print("\nAccuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =====================================
# FEATURE IMPORTANCE (NEW ADDITION 🚀)
# =====================================

importances = model.feature_importances_

feature_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
})

feature_df = feature_df.sort_values(by="Importance", ascending=False)

print("\nTop Important Features:")
print(feature_df.head(10))

# =====================================
# SAVE MODEL + COLUMNS + FEATURE IMPORTANCE
# =====================================

models_dir = BASE_DIR / "models"
models_dir.mkdir(exist_ok=True)

joblib.dump(model, models_dir / "customer_churn_model.pkl")

joblib.dump(X.columns, models_dir / "columns.pkl")

# NEW: Save feature importance for dashboard
joblib.dump(feature_df, models_dir / "feature_importance.pkl")

print("\nModel Saved Successfully!")
print("Model Path:", models_dir / "customer_churn_model.pkl")
print("Columns Saved Successfully!")
print("Feature Importance Saved Successfully!")