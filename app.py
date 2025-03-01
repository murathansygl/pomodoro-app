import streamlit as st

import pandas as pd
from streamlit_extras.bottom_container import bottom
from timer import timer
from task_manager import task_manager
from home import home

# Initialize session state variables
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
    timer()

# Task Manager page
if st.session_state.page == "Task Manager":
    task_manager()