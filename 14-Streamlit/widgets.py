import streamlit as st 
import pandas as pd

st.title("Streamlit text input")
name = st.text_input("Enter your name")
age= st.slider("Enter your age",0,100)





st.write(f"hi {name}, your age is {age}")
options=["python","java","c++","javascript"]
choice = st.selectbox("Select your favorite programming language",options)
st.write(f"hi {name}, your favorite programming language is {choice}")

uploaded_file = st.file_uploader("Choose a file",type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

if name:
    st.success(f"Hello {name}!")
    st.write(f"hi {name}, welcome to streamlit text input example")
    st.toast(f"welcome {name}")