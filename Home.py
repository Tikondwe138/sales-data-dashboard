import streamlit as st
import pandas as pd
from utils import (
    load_data, generate_kpis,
    plot_sales_by_region, plot_customer_ages, plot_gender_split
)

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Data Dashboard")

# === SIDEBAR ===
st.sidebar.header("1. Upload Sales Data")
uploaded_file = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

# Sidebar filters
st.sidebar.header("2. Filter Data")
region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Customer Gender'].unique(), default=df['Customer Gender'].unique())

# Filter dataset
filtered_df = df[df['Region'].isin(region) & df['Customer Gender'].isin(gender)]

# === KPI SECTION ===
st.subheader("📈 Key Performance Indicators")
total_sales, total_profit, profit_margin = generate_kpis(filtered_df)

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${total_sales:,.2f}")
kpi2.metric("Total Profit", f"${total_profit:,.2f}")
kpi3.metric("Profit Margin", f"{profit_margin:.2f}%")

# === VISUALS ===
st.subheader("📉 Visual Analytics")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_sales_by_region(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(plot_customer_ages(filtered_df), use_container_width=True)

st.plotly_chart(plot_gender_split(filtered_df), use_container_width=True)

# === FOOTER ===
st.markdown("---")
st.markdown("© 2025 TIKO Collective")
