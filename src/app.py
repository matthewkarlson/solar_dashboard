import pandas as pd
import numpy as np
import streamlit as st
import vis

# Load the data
df = pd.read_csv('Book1_perturbed.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

st.plotly_chart(vis.get_bar_chart(df, ['datetime'], ['Revenue (Invoiced)']))