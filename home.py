import streamlit as st
from streamlit_extras.bottom_container import bottom

def home():
    st.title("Welcome to Pomodoro App!")

    st.header("How to use?")

    st.subheader("1. Go to Task Manager")
    st.write("Use the sidebar to go to the Taks Manager. There, you can add new tasks, edit or delete the ones existing, and monitor you progress once you start working.")

    st.subheader("2. Start the timer, and FOCUS!")
    st.write("In the Timer page, you can select a task that you have added in the Task Manager. Once you selected, you can set the timer and start working. It's that simple!")
    st.write("After the timer ends, your progress is automatically logged. You can go back to the Task Manager to see your progress.")
    st.write("BUT... If you change the page before the timer ends, your progress will be lost. Be careful!")

    with bottom():
        st.write("Developed by Murathan Saygili")