from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI(title="PulseIQ API")

# Load Models
churn_model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Home
@app.get("/")
def home():
    return {"message": "PulseIQ API is running 🚀"}

# ---------------- SALES PREDICTION ----------------
@app.post("/predict_sales")
def predict_sales(profit: float, quantity: int, discount: float):

    data = np.array([[profit, quantity, discount]])
    scaled = scaler.transform(data)

    prediction = sales_model.predict(scaled)

    return {
        "predicted_sales": float(prediction[0])
    }

# ---------------- CHURN PREDICTION ----------------
@app.post("/predict_churn")
def predict_churn(profit: float, quantity: int, discount: float):

    data = np.array([[profit, quantity, discount]])
    scaled = scaler.transform(data)

    prediction = churn_model.predict(scaled)[0]

    result = "Customer May Churn" if prediction == 1 else "Customer Will Stay"

    return {
        "prediction": int(prediction),
        "result": result
    }