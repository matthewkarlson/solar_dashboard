import pandas as pd
import numpy as np
import streamlit as st
import vis

# Load the data
df = pd.read_csv('Book1_perturbed.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

st.sidebar.date_input('Start Date', min_value=df['datetime'].min(), max_value=df['datetime'].max())
st.sidebar.date_input('End Date', min_value=df['datetime'].min(), max_value=df['datetime'].max())

st.plotly_chart(vis.get_comparison_chart(df, 'datetime', 'invoiced_revenue', 'calculated_revenue', 'Invoiced vs Calculated Revenue'))