import streamlit as st
import psycopg2
import os
from timer import timer
from task_manager import task_manager
from home import home
from auth_page import auth_page
from utils import read_data 
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_config import auth_client

db = firestore.client()

load_dotenv()

st.set_page_config(page_title="Login", page_icon="🔐")
    # Session state to store user info
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_uid = None

if st.session_state.authenticated:
    # Initialize session state variables
    data = read_data(db, st.session_state.user_uid)
    st.session_state.tasks = {item.get('task'): item.get('duration') for item in data}

    if "tasks" not in st.session_state:
        st.session_state.tasks = {}
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None
    if "time_logs" not in st.session_state:
        st.session_state.time_logs = {}
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "remaining_time" not in st.session_state:
        st.session_state.remaining_time = 0

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("Task Manager"):
        st.session_state.page = "Task Manager"
    if st.sidebar.button("Timer"):
        st.session_state.page = "Timer"
    
    st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_uid = None
        st.rerun()

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Home page
    if st.session_state.page == "Home":
        home()

    # Timer page
    if st.session_state.page == "Timer":
        timer(db)

    # Task Manager page
    if st.session_state.page == "Task Manager":
        task_manager(db)
    
else:
    auth_page(auth_client, logout=True)
    st.warning("Please log in to access the content.")

# conn = psycopg2.connect(
#     dbname=os.environ.get("POSTGRES_DB"),
#     user=os.environ.get("POSTGRES_USER"),
#     password=os.environ.get("POSTGRES_PASSWORD"),
#     host=os.environ.get("POSTGRES_HOST"),
#     port=os.environ.get("POSTGRES_PORT")
# )

# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS pomodoro (task TEXT, duration INTEGER)")
# conn.commit()

