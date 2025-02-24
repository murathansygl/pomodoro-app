import streamlit as st
import time
import pandas as pd

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

# Sidebar navigation using buttons
st.sidebar.title("Navigation")
if st.sidebar.button("Go to Timer"):
    st.session_state.page = "Timer"
if st.sidebar.button("Go to Task Management"):
    st.session_state.page = "Task Management"
if st.sidebar.button("Go to Import Data"):
    st.session_state.page = "Import Data"


# Default page setup
if "page" not in st.session_state:
    st.session_state.page = "Timer"
if st.session_state.page == "Timer":
    st.title("Task Timer")

    all_tasks = list(set(st.session_state.tasks.keys()) | set(st.session_state.time_logs.keys()))

    if not all_tasks:
        st.warning("No tasks available. Please add tasks in 'Task Management' or import data.")
    else:
        selected_task = st.selectbox("Select a task", all_tasks)

        # Input for setting timer duration (hours & minutes)
        hours = st.number_input("Hours", min_value=0, max_value=23, step=1)
        minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1)
        total_seconds = hours * 3600 + minutes * 60

        # Start & Stop Buttons
        if st.button("Start Timer"):
            if total_seconds > 0:
                st.session_state.timer_running = True
                st.session_state.remaining_time = total_seconds
                st.session_state.task_selected = selected_task

        if st.button("Stop Timer"):
            st.session_state.timer_running = False
            st.session_state.remaining_time = 0

        # Timer Countdown with Dynamic Background Update
        if st.session_state.get("timer_running", False):
            timer_container = st.empty()
            bg_container = st.empty()

            while st.session_state.remaining_time > 0 and st.session_state.timer_running:
                progress = 1 - (st.session_state.remaining_time / total_seconds)
                red = int(255 * progress)
                green = int(255 * (1 - progress))
                background_color = f"rgb({red}, {green}, 100)"

                # Update the background color dynamically
                bg_container.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-color: {background_color} !important;
                        transition: background-color 1s ease;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                mins, secs = divmod(st.session_state.remaining_time, 60)
                timer_container.metric(label="Time Left", value=f"{mins:02}:{secs:02}")

                time.sleep(1)
                st.session_state.remaining_time -= 1

            # Log the time after completion
            st.session_state.timer_running = False
            st.session_state.time_logs[selected_task] = (
                st.session_state.time_logs.get(selected_task, 0) + total_seconds // 60
            )
            st.success(f"Time logged for {selected_task}: {total_seconds // 60} minutes")

# TASK MANAGEMENT PAGE
if st.session_state.page == "Task Management":
    st.title("Task Management")

    task_name = st.text_input("Enter a new task:")
    if st.button("Add Task"):
        if task_name and task_name not in st.session_state.tasks:
            st.session_state.tasks[task_name] = 0
            st.success(f"Task '{task_name}' added.")
        elif task_name in st.session_state.tasks:
            st.warning("Task already exists.")
        else:
            st.error("Task name cannot be empty.")

    # Display bar chart
    if st.session_state.time_logs:
        df = pd.DataFrame(list(st.session_state.time_logs.items()), columns=["Task", "Time Spent (minutes)"])
        st.bar_chart(df.set_index("Task"))

        # Export button
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("Export Data as CSV", csv_data, "time_logs.csv", "text/csv")
    else:
        st.info("No time logs yet. Start a task timer to track time.")



if st.session_state.page == "Import Data":
    st.title("Import Log Data")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if "Task" in df.columns and "Time Spent (minutes)" in df.columns:
            for _, row in df.iterrows():
                task = row["Task"]
                time_spent = row["Time Spent (minutes)"]

                # Add task if it doesn't exist in the session state
                if task not in st.session_state.tasks:
                    st.session_state.tasks[task] = 0  

                # Update time logs
                st.session_state.time_logs[task] = st.session_state.time_logs.get(task, 0) + time_spent

            st.success("Data imported successfully!")
        else:
            st.error("Invalid file format. Ensure the CSV has 'Task' and 'Time Spent (minutes)' columns.")
