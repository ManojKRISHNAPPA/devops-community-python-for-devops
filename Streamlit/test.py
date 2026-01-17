import streamlit as st
import pandas as pd

st.title("Streamlit and Pandas")

data = {
    "Name": ["Manoj","Zara","Mounica","Rahul","sai"],
    "Age": [30,20,25,22,23],
    "City": ["Banglore","Ranchi","US","Mumbai","Hyd"]
}

df = pd.DataFrame(data)

st.subheader("user detail table..")
st.dataframe(df)