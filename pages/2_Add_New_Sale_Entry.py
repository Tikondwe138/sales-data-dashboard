import streamlit as st
import pandas as pd
import datetime
from utils import load_data, export_to_excel, export_to_pdf
from config import set_theme
from auth import login

st.set_page_config(page_title="Add New Sale Entry", layout="wide")

# === AUTHENTICATION ===
if "user" not in st.session_state:
    if not login():
        st.stop()

# Theme toggle
dark = st.sidebar.toggle("🌙 Dark Mode", value=False)
set_theme(dark)

st.title("➕ Add New Sale Entry")

# Upload existing data or use default
uploaded_file = st.file_uploader("Upload Existing Dataset", type=["csv"])
df = pd.read_csv(uploaded_file) if uploaded_file else load_data()

# === Entry Form ===
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
        # === Validation ===
        if not new_order or not new_product:
            st.warning("🚫 Please fill in all required fields (Order ID & Product Category).")
        elif new_order in df['Order ID'].values:
            st.warning("⚠️ This Order ID already exists. Please use a unique ID.")
        else:
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
            st.success("✅ New entry added successfully!")
            st.dataframe(df)

            # Export buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Updated CSV",
                    df.to_csv(index=False).encode(),
                    "updated_sales_data.csv",
                    "text/csv"
                )
            with col2:
                st.download_button(
                    "📄 Export as PDF",
                    export_to_pdf(df),
                    "updated_sales_data.pdf",
                    "application/pdf"
                )

# === Footer ===
st.markdown("---")
st.markdown("© 2025 TIKO Collective")
