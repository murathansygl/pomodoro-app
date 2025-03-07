import streamlit as st
import psycopg2
import os
import pandas as pd
from streamlit_extras.bottom_container import bottom
from timer import timer
from task_manager import task_manager
from home import home
from utils import read_data
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_creds.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    # Firestore database instance
db = firestore.client()

load_dotenv()

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

# Initialize session state variables
data = read_data(db)
st.session_state.tasks = {item["task"]: item["duration"] for item in data}

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