import streamlit as st
import pandas as pd
import os
from config import set_theme      # ✅ Corrected import
from auth import login

# === Page Config ===
st.set_page_config(page_title="📂 Data Index", layout="wide")

# === AUTHENTICATION ===
if "user" not in st.session_state:
    if not login():
        st.stop()

# === Theme Toggle ===
dark = st.sidebar.toggle("🌙 Dark Mode", value=False)
set_theme(dark)

# === Page Title ===
st.title("📁 Company Data Index")

# === Load CSV files from /data ===
DATA_FOLDER = "data"
csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

if not csv_files:
    st.info("🫙 No data files found in the `data/` folder.")
    st.stop()

# === Display 4x4 Grid ===
st.subheader("📊 Available Datasets")

columns = st.columns(4)  # 4 columns layout
for idx, file in enumerate(csv_files):
    col = columns[idx % 4]
    with col:
        st.markdown(f"**📄 {file}**")
        df = pd.read_csv(os.path.join(DATA_FOLDER, file))

        with st.expander("👀 Preview Top 5 Rows"):
            st.dataframe(df.head(), use_container_width=True)

        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False).encode(),
            file_name=file,
            mime="text/csv"
        )

# === Footer ===
st.markdown("---")
st.markdown("© 2025 TIKO Collective")
