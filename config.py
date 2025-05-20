import streamlit as st

def set_theme(dark: bool):
    """Apply dark or light theme via custom CSS."""
    bg_color = "#0E1117" if dark else "white"
    text_color = "white" if dark else "black"
    button_bg = "#1f77b4" if dark else "#007bff"

    st.markdown(f"""
        <style>
            /* App background and main text */
            .stApp, .css-1d391kg, .css-ffhzg2 {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}

            /* Headers, paragraphs, metric labels */
            .stMarkdown, .stText, .stMetricValue, .stMetricDelta, .css-1v0mbdj, .css-1kyxreq {{
                color: {text_color} !important;
            }}

            /* Sidebar text */
            .css-1nx0c8b, .css-1hynsf2, .css-1j9dxys {{
                color: {text_color} !important;
            }}

            /* Buttons */
            .stButton > button, .css-18e3th9 {{
                background-color: {button_bg} !important;
                color: white !important;
            }}
        </style>
    """, unsafe_allow_html=True)
