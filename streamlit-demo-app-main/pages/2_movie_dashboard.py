import streamlit as st
import pandas as pd
import numpy as np

st.write("# Dashboard - Movies List")

data = pd.read_csv("../movies.csv")
st.write(data)
