PulseIQ Dashboard

A Real-Time Business Intelligence Dashboard with Machine Learning-powered predictions and interactive visualizations.

---

📌 Project Overview

PulseIQ Dashboard is an end-to-end Data Science project that combines:

- 📊 Machine Learning Models
- ⚡ FastAPI Backend
- 🎨 Streamlit Frontend

It helps businesses predict:

- 💰 Sales Forecasting
- 🔁 Customer Churn

---

🛠 Tech Stack

- Programming: Python
- Machine Learning: Scikit-learn, XGBoost
- Backend: FastAPI
- Frontend: Streamlit
- Data Processing: Pandas, NumPy
- Model Storage: Joblib
- Visualization: Matplotlib, Seaborn

---

📁 Folder Structure

PulseIQ-Dashboard/
│
├── backend/              # FastAPI  APIs
│   └── main.py
│
├── frontend/             # Streamlit dashboard
│   └── app.py
│
├── models/               # Trained ML models
│   ├── churn_model.pkl
│   └── scaler.pkl
│
├── data/                 # Dataset
│   └── Superstore.csv
│
├── notebooks/            # Jupyter notebooks
│   └── PulseIQ.ipynb
│
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

---

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/your-username/PulseIQ-Dashboard.git
cd PulseIQ-Dashboard

2️⃣ Install Requirements

pip install -r requirements.txt

---

▶️ Run the Project

🚀 Start Backend (FastAPI)

uvicorn backend.main:app --reload

👉 Open API Docs:
http://127.0.0.1:8000/docs

---

🎨 Start Frontend (Streamlit)

streamlit run frontend/app.py

---

🔮 Features

- 📊 Sales Prediction using ML
- 🔁 Customer Churn Prediction
- ⚡ FastAPI REST API Integration
- 🎨 Interactive Streamlit Dashboard
- 📈 Real-time Inputs & Outputs





👩‍💻 Author

Vaishnavi Kharche


Give it a ⭐ on GitHub!
