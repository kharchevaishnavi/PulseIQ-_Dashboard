import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Page Config

st.set_page_config(page_title="PulseIQ Dashboard", layout="wide")

#Title

st.title("📊 PulseIQ - Sales Dashboard")


#Load Data

@st.cache_data
def load_data():
    df = pd.read_csv("Superstore.csv", encoding='latin1')
    return df

df = load_data()

#Sidebar Filters

st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect("Select Region", df["Region"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique())

#Apply Filters

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

#KPIs

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Total Orders", filtered_df.shape[0])

#Sales by Category

st.subheader("📊 Sales by Category")

fig1, ax1 = plt.subplots()
sns.barplot(x="Category", y="Sales", data=filtered_df, ax=ax1)
plt.xticks(rotation=30)
st.pyplot(fig1)

#Profit by Region

st.subheader("📈 Profit by Region")

fig2, ax2 = plt.subplots()
sns.barplot(x="Region", y="Profit", data=filtered_df, ax=ax2)
plt.xticks(rotation=30)
st.pyplot(fig2)

#Data Table

st.subheader("📂 Data Preview")
st.dataframe(filtered_df.head(50))