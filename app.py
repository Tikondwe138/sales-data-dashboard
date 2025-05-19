import streamlit as st
import pandas as pd
from utils import (
    load_data, save_data, generate_kpis,
    plot_sales_by_region, plot_customer_ages, plot_gender_split
)
from st_aggrid import AgGrid, GridOptionsBuilder
import io

st.set_page_config(page_title="Sales Data Dashboard", layout="wide")

st.title("Sales Data Dashboard")

# Sidebar: Upload CSV
st.sidebar.header("1. Upload Sales Data")
uploaded_file = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

# Sidebar: Filters
st.sidebar.header("2. Filter Data")
region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Customer Gender'].unique(), default=df['Customer Gender'].unique())

filtered_df = df[df['Region'].isin(region) & df['Customer Gender'].isin(gender)]

# KPI Metrics
st.subheader("Key Performance Indicators")
total_sales, total_profit, profit_margin = generate_kpis(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")

# Visualizations
st.subheader("Visual Analytics")
st.plotly_chart(plot_sales_by_region(filtered_df), use_container_width=True)
st.plotly_chart(plot_customer_ages(filtered_df), use_container_width=True)
st.plotly_chart(plot_gender_split(filtered_df), use_container_width=True)

# Editable Data Table
st.subheader("Edit Sales Records")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_default_column(editable=True)
grid_options = gb.build()

grid_response = AgGrid(filtered_df, gridOptions=grid_options, update_mode='MODEL_CHANGED', height=300)
editable_df = grid_response['data']

# Add New Sale Entry
st.subheader("Add New Sale Entry")
with st.form("new_sale_form"):
    new_order = st.text_input("Order ID")
    new_date = st.date_input("Date")
    new_region = st.selectbox("Region", df['Region'].unique())
    new_sales = st.number_input("Sales", min_value=0.0)
    new_profit = st.number_input("Profit", min_value=0.0)
    new_age = st.number_input("Customer Age", min_value=0)
    new_gender = st.selectbox("Customer Gender", ["Male", "Female"])
    new_product = st.text_input("Product Category")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_entry = pd.DataFrame([{
            "Order ID": new_order, "Date": new_date, "Region": new_region,
            "Sales": new_sales, "Profit": new_profit,
            "Customer Age": new_age, "Customer Gender": new_gender,
            "Product Category": new_product
        }])
        editable_df = pd.concat([editable_df, new_entry], ignore_index=True)
        st.success("New entry added.")

# Download Updated Data
st.download_button(
    label="Download Current Dataset",
    data=editable_df.to_csv(index=False).encode(),
    file_name="updated_sales_data.csv",
    mime="text/csv"
)
