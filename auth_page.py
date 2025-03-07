import streamlit as st
from utils import login, signup
import time

def auth_page(auth_client, logout=False): 
   # Sidebar for authentication
    st.sidebar.title("🔐 Authentication")
    auth_option = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"], key=f"{logout}")

    if auth_option == "Login":
        st.sidebar.subheader("Login")
        email = st.sidebar.text_input("Email", key=f"login_email_{logout}")
        password = st.sidebar.text_input("Password", type="password", key=f"login_password_{logout}")

        if st.sidebar.button("Login", key=f"login_{logout}"):
            user = login(auth_client, email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()

    elif auth_option == "Sign Up":
        st.sidebar.subheader("Create a new account")
        email = st.sidebar.text_input("Email", key=f"signup_email_{logout}")
        password = st.sidebar.text_input("Password", type="password", key=f"signup_password_{logout}")

        if st.sidebar.button("Sign Up", key=f"signup_{logout}"):
            user = signup(auth_client, email, password)
            if user:
                st.success("Account created successfully! Please log in.")
