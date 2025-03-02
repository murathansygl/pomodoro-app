import streamlit as st
import pandas as pd
from streamlit_extras.bottom_container import bottom
from utils import read_data, insert_data, update_data, delete_data
def task_manager(conn):

    st.title("Task Management")
    task_name = st.text_input("Enter a new task:")
    if st.button("Add Task"):
        if task_name and task_name not in st.session_state.tasks:
            insert_data(conn=conn, task=task_name, duration=0)
            st.success(f"Task '{task_name}' added.")
        elif task_name in st.session_state.tasks:
            st.warning("Task already exists.")
        else:
            st.error("Task name cannot be empty.")

    
    if  st.session_state.tasks:
        # Task List Management
        st.subheader("Task List")
        
        if not st.session_state.tasks:
            st.info("No tasks available.")
        else:
            for task in list(st.session_state.tasks.keys()):
                col1, col2, col3 = st.columns([6, 1, 1])

                if f"editing_{task}" not in st.session_state:
                    st.session_state[f"editing_{task}"] = False  # Initialize state for existing tasks

                    # Initialize delete state for each task
                if f"confirm_delete_{task}" not in st.session_state:
                    st.session_state[f"confirm_delete_{task}"] = False  

                if st.session_state[f"editing_{task}"]:
                    # Editable input field
                    new_task_name = col1.text_input("Edit Task", task, key=f"edit_{task}")
                    if col1.button("Save", key=f"save_{task}"):
                        if new_task_name and new_task_name != task:
                            update_data(conn=conn, task=task, new_task_name=new_task_name)
                            st.session_state[f"editing_{new_task_name}"] = st.session_state.pop(f"editing_{task}")
                            st.success(f"Task '{task}' renamed to '{new_task_name}'.")
                        st.session_state[f"editing_{new_task_name}"] = False
                        st.rerun()
                # Confirmation Popup
                elif st.session_state[f"confirm_delete_{task}"]:
                    # col1, col2, col3 = st.columns([6,1,1])
                    col1.warning(f"Are you sure you want to delete '{task}'?")
                
                    if col2.button("Delete", key=f"delete_{task}"):
                        delete_data(conn, task)
                        st.success(f"Task '{task}' deleted.")
                        st.rerun()

                    if col3.button("Cancel", key=f"cancel_delete_{task}"):
                        st.session_state[f"confirm_delete_{task}"] = False
                        st.rerun()
                else:
                    col1.write(task)
                    if col2.button("Edit", key=f"edit_btn_{task}"):
                        st.session_state[f"editing_{task}"] = True
                        st.rerun()

                    if col3.button("Delete", key=f"delete_btn_{task}"):
                        st.session_state[f"confirm_delete_{task}"] = True  # Make delete task-specific
                        st.rerun()

                
        if st.session_state.tasks:
            df = pd.DataFrame(st.session_state.tasks.items(), columns=["Task", "Time Spent (minutes)"])
            st.write(df)
            st.bar_chart(data=df,y="Time Spent (minutes)", x="Task", color="Task")

            # Export button
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("Export Data as CSV", csv_data, "time_logs.csv", "text/csv")
        else:
            st.info("No time logs yet. Start a task timer to track time.")

    with bottom():
    
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
