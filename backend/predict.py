from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

# Load model + columns
model = joblib.load(BASE_DIR / "models" / "customer_churn_model.pkl")
columns = joblib.load(BASE_DIR / "models" / "columns.pkl")


# =====================================
# INPUT VALIDATION
# =====================================

def validate_input(data):

    try:
        if float(data["Tenure Months"]) < 0:
            return "❌ Tenure Months cannot be negative"

        if float(data["Monthly Charges"]) < 0:
            return "❌ Monthly Charges cannot be negative"

        if float(data["Total Charges"]) < 0:
            return "❌ Total Charges cannot be negative"

    except Exception as e:
        return f"❌ Invalid numeric input detected: {str(e)}"

    return None


# =====================================
# PREDICTION FUNCTION (IMPROVED)
# =====================================

def predict_customer(form_data):

    # Step 1: Validate input
    error = validate_input(form_data)

    if error:
        # IMPORTANT: always return same structure
        return {"label": error}, 0.0

    # Step 2: Convert form data safely
    data = {
    "Tenure Months": float(form_data.get("Tenure Months", 0)),
    "Monthly Charges": float(form_data.get("Monthly Charges", 0)),
    "Total Charges": float(form_data.get("Total Charges", 0)),
    "Internet Service": form_data.get("Internet Service"),
    "Online Security": form_data.get("Online Security"),
    "Tech Support": form_data.get("Tech Support"),
    "Contract": form_data.get("Contract"),
    "Payment Method": form_data.get("Payment Method")
}

    # Step 3: DataFrame
    df = pd.DataFrame([data])

    # Step 4: Encoding
    df = pd.get_dummies(df)

    # Step 5: Align columns
    df = df.reindex(columns=columns, fill_value=0)

    # Step 6
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    print("=" * 60)
    print("Prediction :", prediction)
    print("Probabilities :", probabilities)
    print("Classes :", model.classes_)
    print("=" * 60)

    probability = probabilities[1] * 100

    # Step 7
    label = "Churn" if prediction == 1 else "No Churn"

    # Step 8: Return structured output (VERY IMPORTANT)
    return {
        "label": label,
        "raw_prediction": int(prediction)
    }, float(probability)