import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="PulseIQ Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "Superstore.csv")

    df = pd.read_csv(file_path, encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# ================= TITLE =================
st.title("📊 PulseIQ - AI Powered Business Intelligence Dashboard")
st.markdown("### Real-Time Analytics | Forecasting | Customer Insights | ML Prediction")

# ================= SIDEBAR =================
st.sidebar.header("🔍 Advanced Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# ================= FILTERING =================
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]

filtered_df = filtered_df[
    (filtered_df["Region"].isin(region)) &
    (filtered_df["Category"].isin(category))
]

# ================= KPI SECTION =================
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
customers = filtered_df["Customer Name"].nunique()

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("👥 Customers", customers)

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Overview", "📦 Products", "📈 Forecast", "🤖 Prediction"]
)

# ================= TAB 1 =================
with tab1:
    st.subheader("📅 Monthly Sales Trend")

    monthly = filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"].sum().reset_index()

    monthly["Order Date"] = monthly["Order Date"].astype(str)

    fig1 = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig1, width="stretch")

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("📦 Category Sales")

        cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()

        fig2 = px.bar(
            cat,
            x="Category",
            y="Sales",
            color="Category"
        )

        st.plotly_chart(fig2, width="stretch")

    with col6:
        st.subheader("🌍 Region Profit")

        reg = filtered_df.groupby("Region")["Profit"].sum().reset_index()

        fig3 = px.pie(
            reg,
            names="Region",
            values="Profit"
        )

        st.plotly_chart(fig3, width="stretch")

# ================= TAB 2 =================
with tab2:
    st.subheader("🏆 Top 10 Products")

    top_products = filtered_df.groupby("Product Name")["Sales"].sum()
    top_products = top_products.nlargest(10).reset_index()

    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales"
    )

    st.plotly_chart(fig4, width="stretch")

    st.subheader("🏆 Top Customers")

    top_customers = filtered_df.groupby("Customer Name")["Sales"].sum()
    top_customers = top_customers.nlargest(10).reset_index()

    st.dataframe(top_customers, width="stretch")

# ================= TAB 3 =================
with tab3:
    st.subheader("📈 Next 6 Months Forecast")

    monthly2 = filtered_df.groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"].sum().reset_index()

    monthly2["Order Date"] = monthly2["Order Date"].astype(str)

    last_sales = monthly2["Sales"].iloc[-1]

    future_months = pd.date_range(
        start=pd.to_datetime(df["Order Date"]).max(),
        periods=6,
        freq="ME"
    )

    forecast_sales = [
        last_sales * (1 + (i * 0.03))
        for i in range(1, 7)
    ]

    forecast_df = pd.DataFrame({
        "Month": future_months.astype(str),
        "Forecast Sales": forecast_sales
    })

    fig5 = px.line(
        forecast_df,
        x="Month",
        y="Forecast Sales",
        markers=True,
        title="Future Revenue Forecast"
    )

    st.plotly_chart(fig5, width="stretch")

# ================= TAB 4 =================
with tab4:
    st.subheader("🤖 Churn Prediction")

    profit = st.number_input("Enter Profit")
    quantity = st.number_input("Enter Quantity")
    discount = st.number_input("Enter Discount")

    if st.button("Predict Churn"):

        try:
            url = "http://127.0.0.1:8000/predict_churn"

            params = {
                "profit": profit,
                "quantity": quantity,
                "discount": discount
            }

            response = requests.post(url, params=params)

            result = response.json()

            st.success(f"Prediction Result: {result}")

        except:
            st.error("FastAPI server is not running")

# ================= DOWNLOAD =================
st.subheader("📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ================= DATA PREVIEW =================
st.subheader("📂 Data Preview")
st.dataframe(filtered_df.head(50), width="stretch")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 🚀 Created by Vaishnavi Kharche | PulseIQ Project")