import streamlit as st

st.title("Devops_Community")

st.write("Welcome to python for devops class")

name = st.text_input("Enter your name")

if st.button("say helloo"):
    st.success(f"Hello {name}, welcome to python for devops class...")
