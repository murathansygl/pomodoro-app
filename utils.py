import streamlit as st

def read_data(conn):
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "SELECT * FROM pomodoro;"
    #         cursor.execute(query)
    #         return dict(cursor.fetchall())
    tasks_ref = conn.collection("pomodoro").stream()
    tasks = [{"id": doc.id, "task": doc.to_dict()["task"], "duration": doc.to_dict()["duration"]} for doc in tasks_ref]
    return tasks


def insert_data(conn, task, duration):
    st.session_state.tasks[task] = duration
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "INSERT INTO pomodoro (task, duration) VALUES (%s, %s);"
    #         cursor.execute(query, (task, duration))
    doc_ref = conn.collection("pomodoro").document()
    doc_ref.set({
        "task": task,
        "duration": duration
    })


def update_data(conn, task, duration=None, new_task_name=None):
    if new_task_name:
        st.session_state.tasks[new_task_name] = st.session_state.tasks.pop(task)
        # with conn:
        #     with conn.cursor() as cursor:
        #         query = "UPDATE pomodoro SET task = %s WHERE task = %s"
        #         cursor.execute(query, (new_task_name, task))

    
    docs = conn.collection("pomodoro").where("task", "==", task).stream()


    for doc in docs:
        if not duration:
            duration = doc.get('duration')
        if not new_task_name:
            st.session_state.tasks[task] += duration # // 60
            new_task_name = doc.get('task')

        doc_ref = conn.collection("pomodoro").document(doc.id)
        doc_ref.update({"task": new_task_name, "duration": duration})

    # if duration:
        # st.session_state.tasks[task] += duration # // 60
    #     with conn:
    #         with conn.cursor() as cursor:
    #             query = "UPDATE pomodoro SET duration = %s WHERE task = %s"
    #             cursor.execute(query, (duration, task))


def delete_data(conn, task):
    del st.session_state[f"editing_{task}"]
    del st.session_state[f"confirm_delete_{task}"]
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "DELETE FROM pomodoro WHERE task = %s"
    #         st.write(query)
    #         cursor.execute(query, (task,))
    docs = conn.collection("pomodoro").where("task", "==", task).stream()
    for doc in docs:
        conn.collection("pomodoro").document(doc.id).delete()