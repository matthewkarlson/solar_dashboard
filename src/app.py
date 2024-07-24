import pandas as pd
import numpy as np
import streamlit as st

# Load the data
df = pd.read_csv('Book1_perturbed.csv')
st.write(df)
