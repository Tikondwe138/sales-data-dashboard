import streamlit as st

# Dummy user database
USERS = {
    "admin": "admin123",
    "analyst": "analyst123"
}

def login():
    # --- Check if already logged in ---
    if "user" in st.session_state:
        st.sidebar.success(f"Logged in as **{st.session_state['user']}**")
        if st.sidebar.button("Logout"):
            del st.session_state["user"]
        return True

    # --- Login form ---
    with st.sidebar:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_clicked = st.button("Login", key="login_button")

    # --- Process login ---
    if login_clicked:
        if USERS.get(username) == password:
            st.session_state["user"] = username
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password")

    return False
