from flask import Flask, render_template, request
from predict import predict_customer
from database import init_db, save_prediction
import sqlite3
import joblib
from pathlib import Path

app = Flask(__name__)

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "churn.db"

# Initialize database
init_db()


# =========================
# DATABASE HELPER
# =========================

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_db_data():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='Churn'")
    churn = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='No Churn'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(probability) FROM predictions")
    avg_prob = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT prediction, probability
        FROM predictions
        ORDER BY id DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()

    conn.close()

    if latest:
        latest_prediction = latest[0]
        latest_probability = float(latest[1])
    else:
        latest_prediction = "No Data"
        latest_probability = 0.0

    return (
        total,
        churn,
        safe,
        avg_prob,
        latest_prediction,
        latest_probability,
    )


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# PREDICT
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    result, probability = predict_customer(request.form)

    # If validation failed
    if result["label"].startswith("❌"):
        return render_template(
            "index.html",
            error=result["label"]
        )

    label = result["label"]
    probability = float(probability)

    if probability > 70:
        risk_level = "High Risk"
    elif probability > 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    # Save only valid predictions
    save_prediction(label, probability, risk_level)

    return render_template(
        "index.html",
        prediction=label,
        probability=round(probability, 2),
        risk_level=risk_level,
        risk_score=int(probability),
        safe_score=int(100 - probability)
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    total, churn, safe, avg_prob, latest_prediction, latest_probability = get_db_data()

    if latest_probability >= 70:
        risk_level = "High Risk"
    elif latest_probability >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    try:
        feature_df = joblib.load(
            BASE_DIR.parent / "models" / "feature_importance.pkl"
        )

        top = feature_df.head(10)

        features = top["Feature"].tolist()
        importance = top["Importance"].tolist()

    except Exception:

        features = []
        importance = []

    data = {
        "total": total,
        "churn": churn,
        "safe": safe,
        "avg_prob": round(avg_prob, 2),

        "latest_prediction": latest_prediction,
        "latest_probability": round(latest_probability, 2),

        "risk_level": risk_level,
        "risk_score": round(latest_probability, 2),
        "safe_score": round(100 - latest_probability, 2),

        "features": features,
        "importance": importance
    }

    return render_template("dashboard.html", data=data)


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# =========================
# API
# =========================

@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.json

    result, probability = predict_customer(data)

    return {
        "prediction": result["label"],
        "probability": float(probability)
    }


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)