import streamlit as st
import pandas as pd
from datetime import datetime
import os

USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["userid", "password"])

def save_user(userid, password):
    df = load_users()
    df = pd.concat([df, pd.DataFrame([[userid, password]], columns=df.columns)])
    df.to_csv(USERS_FILE, index=False)

def save_history(userid, filename):
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
    else:
        df = pd.DataFrame(columns=["userid", "filename", "datetime"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.concat([df, pd.DataFrame([[userid, filename, now]], columns=df.columns)])
    df.to_csv(HISTORY_FILE, index=False)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.userid = ""

st.sidebar.title("Menu")

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Select", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Select", ["Explore CSV", "See History", "Logout"])


st.title("CSV User System")

if menu == "Home":
    st.write("Welcome! Please login or register.")

# REGISTER
elif menu == "Register":
    st.subheader("Register")
    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = load_users()
        if userid in users["userid"].values:
            st.error("User already exists")
        else:
            save_user(userid, password)
            st.success("Registration successful")

# LOGIN
elif menu == "Login":
    st.subheader("Login")
    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        valid = users[
            (users["userid"] == userid) & (users["password"] == password)
        ]
        if not valid.empty:
            st.session_state.logged_in = True
            st.session_state.userid = userid
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif menu == "Explore CSV":
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        save_history(st.session_state.userid, uploaded_file.name)
        st.success("File uploaded and history saved")

elif menu == "See History":
    st.subheader("Upload History")
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        user_df = df[df["userid"] == st.session_state.userid]
        st.dataframe(user_df)
    else:
        st.info("No history found")

# LOGOUT
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.userid = ""
    st.success("Logged out successfully")
    st.write("Thanks for using the app ")