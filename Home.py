import streamlit as st
import pandas as pd
from utils import (
    load_data,
    generate_kpis,
    plot_sales_by_region,
    plot_customer_ages,
    plot_gender_split
)
from config import set_theme
from auth import login

# === PAGE CONFIG ===
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Check if user logged in, else show login form and stop execution
# === AUTHENTICATION ===
if "user" not in st.session_state:
    if not login():
        st.stop()

# === DARK MODE TOGGLE ===
dark_mode = st.sidebar.toggle(" Enable Dark Mode", value=False)
set_theme(dark_mode)

st.title("📊 Sales Data Dashboard")

# === SIDEBAR: File Upload ===
st.sidebar.header("1. Upload Sales Data")
uploaded_file = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

# === SIDEBAR: Filters ===
st.sidebar.header("2. Filter Data")
region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Customer Gender'].unique(), default=df['Customer Gender'].unique())

filtered_df = df[df['Region'].isin(region) & df['Customer Gender'].isin(gender)]

# === KPIs ===
st.subheader("📈 Key Performance Indicators")
total_sales, total_profit, profit_margin = generate_kpis(filtered_df)

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Sales", f"${total_sales:,.2f}")
kpi2.metric("Total Profit", f"${total_profit:,.2f}")
kpi3.metric("Profit Margin", f"{profit_margin:.2f}%")

# === DRILL-DOWN CONTROLS ===
st.subheader("📌 Drill-Down Controls")
selected_region = st.selectbox("Drill down by Region", df['Region'].unique())
drill_df = df[df["Region"] == selected_region]
st.dataframe(drill_df)

# === CHARTS ===
st.subheader("📉 Visual Analytics")
chart1, chart2 = st.columns(2)

with chart1:
    st.plotly_chart(plot_sales_by_region(filtered_df), use_container_width=True)

with chart2:
    st.plotly_chart(plot_customer_ages(filtered_df), use_container_width=True)

st.plotly_chart(plot_gender_split(filtered_df), use_container_width=True)

# === FOOTER ===
st.markdown("---")
st.markdown("© 2025 TIKO Collective")
