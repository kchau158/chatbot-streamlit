import openai
import re
import streamlit as st
from PIL import Image

#from callcenter_prompts import get_system_prompt
#from cybersyn_prompts import get_system_prompt
from customer_prompts import get_system_prompt

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


st.title(":man-surfing: Chatbot with Snowflake Streamlit and OpenAI")
image = Image.open('./snowflake_chatbot.png')
st.image(image, caption='Data flows illustration')
conn = st.experimental_connection("snowpark")

with st.chat_message("assistant"):
    st.write("Hello human! I'm a chatbot powered by OpenAI's GPT-3. I can answer questions about your data. Try asking me anything.")

# Initialize the chat messages history
if "messages" not in st.session_state:
    if not (openai_api_key):
        st.info("Please provide required information on sidebar to continue.")
        st.stop()
 #   openai.api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = openai_api_key
    # the get_system_prompt() will connect to Snowflake to get table metadata and user's provided hints
    # then passes information to the LLM to produce a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response += delta.choices[0].delta.get("content", "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)
            
            message["results"] = conn.query(sql)
            st.dataframe(message["results"])

        st.session_state.messages.append(message)

