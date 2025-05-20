import streamlit as st
import pandas as pd
from utils import load_data, export_to_excel, export_to_pdf
from st_aggrid import AgGrid, GridOptionsBuilder
from config import set_theme
from auth import login

# === PAGE CONFIG ===
st.set_page_config(page_title="Edit Sales Records", layout="wide")

# === AUTHENTICATION ===
if "user" not in st.session_state:
    if not login():
        st.stop()

# === THEME TOGGLE ===
dark = st.sidebar.toggle("🌙 Dark Mode", value=False)
set_theme(dark)

st.title("📝 Edit Sales Records")

# === FILE UPLOAD ===
uploaded_file = st.file_uploader("Upload CSV to Edit", type=["csv"])
df = pd.read_csv(uploaded_file) if uploaded_file else load_data()

# === EDITABLE TABLE ===
st.write("Edit directly in the table below:")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)
grid_options = gb.build()

grid_response = AgGrid(df, gridOptions=grid_options, update_mode='MODEL_CHANGED', height=400)

# Fallback in case data key is missing
editable_df = grid_response.get('data', df)

st.success("✅ You can now download the edited records.")

# === DOWNLOAD BUTTONS ===
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        "📥 Download as CSV",
        data=editable_df.to_csv(index=False).encode(),
        file_name="edited_sales_data.csv",
        mime="text/csv"
    )
with col2:
    st.download_button(
        "📄 Export as PDF",
        data=export_to_pdf(editable_df),
        file_name="edited_sales_data.pdf",
        mime="application/pdf"
    )

# === FOOTER ===
st.markdown("---")
st.markdown("© 2025 TIKO Collective")
