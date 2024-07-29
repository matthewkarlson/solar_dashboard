from AI import AI
from ContextData import ContextData
import streamlit as st

api_key = st.secrets["openai_api_key"]

aiClient = AI(api_key)

aiClient.initialise_context([
    ContextData("../app/data/test_data.csv", "Revenue Data")
])

res = aiClient.create_summary(
    [
        "What are the most imporant factors impacting generation? I am particularly interested in the impact of weather.",
        "What are the trends in revenue based on the time of year? When would be a good time for maintenance?"
    ],
)

print(res.choices[0].message.content)