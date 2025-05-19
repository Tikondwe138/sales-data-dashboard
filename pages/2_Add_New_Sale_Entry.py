import streamlit as st
import pandas as pd
from utils import load_data
import datetime

st.set_page_config(page_title="Add New Entry")

st.title("➕ Add New Sale Entry")

uploaded_file = st.file_uploader("Upload Existing Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

with st.form("add_entry"):
    new_order = st.text_input("Order ID")
    new_date = st.date_input("Date", value=datetime.date.today())
    new_region = st.selectbox("Region", df['Region'].unique())
    new_sales = st.number_input("Sales", min_value=0.0)
    new_profit = st.number_input("Profit", min_value=0.0)
    new_age = st.number_input("Customer Age", min_value=0)
    new_gender = st.selectbox("Customer Gender", ["Male", "Female"])
    new_product = st.text_input("Product Category")

    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_data = pd.DataFrame([{
            "Order ID": new_order,
            "Date": new_date,
            "Region": new_region,
            "Sales": new_sales,
            "Profit": new_profit,
            "Customer Age": new_age,
            "Customer Gender": new_gender,
            "Product Category": new_product
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        st.success("New entry added!")
        st.dataframe(df)

        st.download_button(
            "📥 Download Updated Dataset",
            df.to_csv(index=False).encode(),
            "updated_sales_data.csv",
            "text/csv"
        )

st.markdown("© 2025 TIKO Collective")
