from fastapi import FastAPI
import joblib
import numpy as np

# App initialize
app = FastAPI(title="PulseIQ API")

# Load models
churn_model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Home route
@app.get("/")
def home():
    return {"message": "PulseIQ API is running 🚀"}

# ---------------- SALES PREDICTION ----------------
@app.post("/predict_sales")
def predict_sales(profit: float, quantity: int, discount: float):
    
    data = np.array([[profit, quantity, discount]])
    data = scaler.transform(data)

    prediction = sales_model.predict(data)

    return {
        "predicted_sales": float(prediction[0])
    }

# ---------------- CHURN PREDICTION ----------------
@app.post("/predict_churn")
def predict_churn(profit: float, quantity: int, discount: float):

    data = np.array([[profit, quantity, discount]])

    prediction = churn_model.predict(data)

    return {
        "churn": int(prediction[0])
    }
# ================= PREDICTION API =================
@app.post("/predict")
def predict(data: dict):
    try:
        profit = data["Profit"]
        quantity = data["Quantity"]
        discount = data["Discount"]

        features = np.array([[profit, quantity, discount]])
        scaled = scaler.transform(features)

        prediction = churn_model.predict(scaled)[0]

        return {"prediction": float(prediction)}

    except Exception as e:
        return {"error": str(e)}