import pandas as pd
import numpy as np
import streamlit as st
import vis
import utils
from AI.ContextData import ContextData
from AI.AI import AI
from langchain.schema import SystemMessage,HumanMessage
from openai import OpenAI
st.set_page_config(layout="wide")
# Load the data
df_unfiltered = pd.read_csv('test_data.csv')
df_unfiltered['datetime'] = pd.to_datetime(df_unfiltered['datetime'])

st.sidebar.image('src/images/logo_transparent.png', use_column_width=True, output_format='auto')
start_date = st.sidebar.date_input('Start Date', min_value=df_unfiltered['datetime'].min(), max_value=df_unfiltered ['datetime'].max(), value=df_unfiltered['datetime'].min())
end_date = st.sidebar.date_input('End Date', min_value=df_unfiltered['datetime'].min(), max_value=df_unfiltered['datetime'].max(), value=df_unfiltered['datetime'].max())

# Filter the data based on selected dates and convert both to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
df = df_unfiltered[(df_unfiltered['datetime'] >= start_date) & (df_unfiltered['datetime'] <= end_date)]

alterprice = st.sidebar.checkbox("View Dynamic Site with fixed pricing?", value=False)
vis.display_custom_block('Revenue Summary for Site One', st)
df['date'] = df['datetime'].dt.strftime('%Y-%m')
if alterprice: 
    fixed_price = st.sidebar.number_input('Fixed Price', value=75)
    df['new_revenue'] = fixed_price * df['Generation']
    st.plotly_chart(vis.get_bar_chart(df, 'datetime', 'new_revenue', 'Altered Revenue'))
    # The fixed price required to match the dynamic revenue
    required_price = df['invoiced_revenue'].sum() / df['Generation'].sum()
    st.write(f'The fixed price required to match the dynamic revenue is: £{required_price.round(2)}')
    st.dataframe(df[['date','invoiced_revenue','calculated_revenue','Generation']], height=300,hide_index=True,use_container_width=True)
else:
    st.plotly_chart(vis.get_comparison_chart(df, 'datetime', 'invoiced_revenue', 'calculated_revenue', 'Invoiced vs Calculated Revenue'))
    st.dataframe(df[['date','invoiced_revenue','calculated_revenue','Generation']], height=300,hide_index=True, use_container_width=True)
selected_supplementary_data = st.selectbox('Select the additional data to display', ['energy_yield','system_losses','inverter_efficiency','mean_array_efficiency','reference_yield'])

st.plotly_chart(vis.get_line_chart(df, 'datetime', selected_supplementary_data, selected_supplementary_data))

st.title("AI Data Science Agents")

model = utils.create_openai_chat(api_key=st.secrets["OPENAI_API_KEY"], model = "gpt-4o", temperature = 0)

aiClient = AI(st.secrets["OPENAI_API_KEY"])
aiClient.initialise_context([
    ContextData("test_data.csv", "Revenue Data")
])

# Initialize a session state variable to track if the initial function has run
if 'initial_run_done' not in st.session_state:
    st.session_state.initial_run_done = False

# Only run the initial function if it hasn't been run yet
if not st.session_state.initial_run_done:
    with st.spinner("AI is thinking..."):
        result = aiClient.create_summary(
            [
                "What are the most important factors impacting generation? I am particularly interested in the impact of weather.",
                "What are the trends in revenue based on the time of year? When would be a good time for maintenance?",
                "How can we increase our revenue going forward based on this data?"
            ]
        )
    # Store the result in session state
    st.session_state.initial_result = result.choices[0].message.content
    st.session_state.initial_run_done = True

# Display the initial result if it exists
if 'initial_result' in st.session_state:
    response = st.session_state.initial_result
    with st.chat_message("Output"):
        st.write(response)

# Chat input should be at the bottom
prompt = st.chat_input("User")

if prompt:
    system_prompt = "Base your answer on this given information: {}".format(response)
    st.write(prompt)
    response = model([SystemMessage(system_prompt), HumanMessage(prompt)])
    st.write(response.content)
