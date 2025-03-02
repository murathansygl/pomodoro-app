import streamlit as st

def read_data(conn):
    with conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM pomodoro;"
            cursor.execute(query)
            return dict(cursor.fetchall())


def insert_data(conn, task, duration):
    st.session_state.tasks[task] = duration
    with conn:
        with conn.cursor() as cursor:
            query = "INSERT INTO pomodoro (task, duration) VALUES (%s, %s);"
            cursor.execute(query, (task, duration))


def update_data(conn, task, duration=None, new_task_name=None):
    if new_task_name:
        st.session_state.tasks[new_task_name] = st.session_state.tasks.pop(task)
        with conn:
            with conn.cursor() as cursor:
                query = "UPDATE pomodoro SET task = %s WHERE task = %s"
                cursor.execute(query, (new_task_name, task))

    if duration:
        st.session_state.tasks[task] += duration # // 60
        with conn:
            with conn.cursor() as cursor:
                query = "UPDATE pomodoro SET duration = %s WHERE task = %s"
                cursor.execute(query, (duration, task))


def delete_data(conn, task):
    del st.session_state[f"editing_{task}"]
    del st.session_state[f"confirm_delete_{task}"]
    with conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM pomodoro WHERE task = %s"
            st.write(query)
            cursor.execute(query, (task,))