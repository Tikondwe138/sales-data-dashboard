import streamlit as st
import pandas as pd
from utils import load_data
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Edit Sales Records")

st.title("📝 Edit Sales Records")

uploaded_file = st.file_uploader("Upload CSV to Edit", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

st.write("Edit directly in the table below:")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)
grid_options = gb.build()

grid_response = AgGrid(df, gridOptions=grid_options, update_mode='MODEL_CHANGED', height=300)
editable_df = grid_response['data']

st.download_button(
    label="📥 Download Edited Data",
    data=editable_df.to_csv(index=False).encode(),
    file_name="edited_sales_data.csv",
    mime="text/csv"
)

st.markdown("© 2025 TIKO Collective")
