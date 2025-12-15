import streamlit as st
import pandas as pd
import sqlite3

st.title("CSV File Executor")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("CSV Data")
    st.dataframe(df)

   
    conn = sqlite3.connect(":memory:")
    df.to_sql("data", conn, index=False, if_exists="replace")


    query = st.text_area(
        "Enter SQL Query",
        "SELECT * FROM data"
    )

  
    if st.button("Execute"):
        try:
            result = pd.read_sql(query, conn)
            st.subheader("Query Result")
            st.dataframe(result)
        except Exception as e:
            st.error(e)

