import streamlit as st

# Define authentication functions
def login(auth_client, email, password):
    try:
        user = auth_client.sign_in_with_email_and_password(email, password)
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.session_state.user_uid = user["localId"]  # UID of the logged-in user
        
        return user
    except Exception as e:
        st.error("Invalid email or password")
        return None


def signup(auth_client, email, password):
    try:
        user = auth_client.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        st.error("Signup failed: " + str(e))
        return None


def read_data(conn, user_uid):
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "SELECT * FROM pomodoro;"
    #         cursor.execute(query)
    #         return dict(cursor.fetchall())
    tasks_ref = conn.collection("users").document(user_uid).collection("tasks").stream()

    tasks = [doc for doc in tasks_ref]
    return tasks


def insert_data(conn, user_uid, task, duration):
    st.session_state.tasks[task] = duration
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "INSERT INTO pomodoro (task, duration) VALUES (%s, %s);"
    #         cursor.execute(query, (task, duration))

    task_data = {
        "task": task,
        "duration": duration
    }
    conn.collection("users").document(user_uid).collection("tasks").add(task_data)


def update_data(conn, user_uid, task, duration=None, new_task_name=None):
    if new_task_name:
        st.session_state.tasks[new_task_name] = st.session_state.tasks.pop(task)
        # with conn:
        #     with conn.cursor() as cursor:
        #         query = "UPDATE pomodoro SET task = %s WHERE task = %s"
        #         cursor.execute(query, (new_task_name, task))

    
    tasks_ref = conn.collection("users").document(user_uid).collection("tasks").where("task", "==", task).stream()

    for doc in tasks_ref:
        if not duration:
            duration = doc.get('duration')
        if not new_task_name:
            st.session_state.tasks[task] += duration # // 60
            new_task_name = doc.get('task')

        doc_ref = conn.collection("users").document(user_uid).collection("tasks").document(doc.id)
        doc_ref.update({"task": new_task_name, "duration": duration})

    # if duration:
        # st.session_state.tasks[task] += duration # // 60
    #     with conn:
    #         with conn.cursor() as cursor:
    #             query = "UPDATE pomodoro SET duration = %s WHERE task = %s"
    #             cursor.execute(query, (duration, task))


def delete_data(conn, user_uid, task):
    del st.session_state[f"editing_{task}"]
    del st.session_state[f"confirm_delete_{task}"]
    # with conn:
    #     with conn.cursor() as cursor:
    #         query = "DELETE FROM pomodoro WHERE task = %s"
    #         st.write(query)
    #         cursor.execute(query, (task,))
    docs = conn.collection("users").document(user_uid).collection("tasks").where("task", "==", task).stream()
    for doc in docs:
        conn.collection("users").document(user_uid).collection("tasks").document(doc.id).delete()