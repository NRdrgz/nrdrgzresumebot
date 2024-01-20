import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Resume Bot",
        page_icon="🤖",
    )

    st.write("# Welcome to Nicolas Rodriguez's Resume Bot! 👋")


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Welcome! I'm Nico's Resume Bot, specialized in providing information about Nicolas Rodriguez's professional background and qualifications. Feel free to ask me questions such as:"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        ##TODO Send message to a LLM and get response
        #client = OpenAI(api_key=openai_api_key)
        #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        #msg = response.choices[0].message.content

        msg = "ok"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)


if __name__ == "__main__":
    run()