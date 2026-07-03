import streamlit as st
import pandas as pd
import numpy as np

# title in st
st.title("Streamlit title Example - Welcome to Streamlit")

#  display a simple text
st.text("This is a simple text using text function")
st.write("This is a simple text using write function")

# creating a simple dataframe
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [110, 210, 310, 410]
})

# displaying the dataframe using st.dataframe

st.dataframe(df)  # Same as st.write(df)
st.write(df)  # Same as st.dataframe(df)