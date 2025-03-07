import streamlit as st
import time
from utils import update_data
def timer(conn):
    st.title("Task Timer")

    all_tasks = st.session_state.tasks
    
    if not all_tasks:
        st.warning("No tasks available. Please add tasks in 'Task Management' or import data.")
    else:
        selected_task = st.selectbox("Select a task", all_tasks)

        # Input for setting timer duration (hours & minutes)
        minutes = st.number_input("Minutes", min_value=0, max_value=60*24, step=1)
        seconds = st.number_input("Seconds", min_value=0, max_value=59, step=1)
        total_seconds = minutes * 60 + seconds

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

            while st.session_state.remaining_time >= 0 and st.session_state.timer_running:
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
            update_data(conn, st.session_state.user_uid, selected_task, total_seconds)
            # st.rerun()
            st.success(f"Time logged for {selected_task}: {total_seconds // 60} minutes")
            