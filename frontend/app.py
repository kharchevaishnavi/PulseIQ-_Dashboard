import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

# Page Configimport
st.set_page_config(page_title="PulseIQ Dashboard", layout="wide")

# Title
st.title("📊 PulseIQ - AI- Powered Business Intelligence Dashboard")


# Load Data

import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "Superstore.csv")

    df = pd.read_csv(file_path, encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    return df

df = load_data()



# ================= Sidebar =================
st.sidebar.header("🔍 Advanced Filters")

# Date Filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

# Region & Category
region = st.sidebar.multiselect("Region", df["Region"].unique())
category = st.sidebar.multiselect("Category", df["Category"].unique())

# ================= Filtering =================
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# ================= KPIs =================
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df.shape[0]
avg_sales = filtered_df['Sales'].mean()

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Orders", total_orders)
col4.metric("📊 Avg Sales", f"${avg_sales:,.0f}")

# ================= Tabs =================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📦 Product Analysis", "📉 Insights"])

# ================= TAB 1 =================
with tab1:
    st.subheader("Sales by Category")

    fig1 = px.bar(filtered_df, x="Category", y="Sales", color="Category")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Profit by Region")

    fig2 = px.bar(filtered_df, x="Region", y="Profit", color="Region")
    st.plotly_chart(fig2, use_container_width=True)

# ================= TAB 2 =================
with tab2:
    st.subheader("Top 10 Products by Sales")

    top_products = filtered_df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()

    fig3 = px.bar(top_products, x="Sales", y="Product Name", orientation='h')
    st.plotly_chart(fig3, use_container_width=True)

# ================= TAB 3 =================
with tab3:
    st.subheader("Correlation Heatmap")

    corr = filtered_df[["Sales", "Profit", "Quantity", "Discount"]].corr()

    fig4 = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig4, use_container_width=True)

# ================= Download =================
st.subheader("📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv'
)

# ================= Data Preview =================
st.subheader("📂 Data Preview")
st.dataframe(filtered_df.head(50))

# ================== CHURN PREDICTION ==================

st.subheader("🔮 Churn Prediction")

profit = st.number_input("Enter Profit")
quantity = st.number_input("Enter Quantity")
discount = st.number_input("Enter Discount")

if st.button("Predict Churn"):

    url = "http://127.0.0.1:8000/predict_churn"

    params = {
        "profit": profit,
        "quantity": quantity,
        "discount": discount
    }

    response = requests.post(url, params=params)

    result = response.json()

    st.success(f"Prediction: {result}")
    st.write(result)