import streamlit as st
import openai

st.title(":man-surfing: Validating Credentials")

openai.api_key = st.secrets["OPENAI_API_KEY"]

with st.chat_message("assistant"):
    st.write("Hello human! Let's validate connection to OpenAPI using your API key. What is Streamlit, Snowpark and OpenAPI?")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What are Streamlit, Snowflake's Snowpark and ChatGPT's OpenAPI?"}
  ]
)
st.write(completion.choices[0].message.content)

with st.chat_message("assistant"):
    st.write("Now we'll validate Snowflake connection.")

conn = st.experimental_connection("snowpark")
df = conn.query("select current_warehouse()")
st.write(df)