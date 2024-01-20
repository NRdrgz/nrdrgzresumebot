import streamlit as st
from openai import OpenAI
import os
from streamlit.logger import get_logger
from utils import load_resume_from_pdf

LOGGER = get_logger(__name__)

#TODO replace by secret key when deployed online
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Text version of your resume
resume_path = 'Resume_Nicolas_Rodriguez_ENG_Main.pdf'  
resume_text = load_resume_from_pdf(resume_path)
instruction_text = """ System: You are a CareerBot, a comprehensive, interactive resource for exploring Nicolas Rodriguez background, 
skills, and expertise. Be polite and provide answers based on the provided context only. Use only the provided data and not prior knowledge.
Human: Follow exactly these 3 steps:
1. Read the context below
2. Answer the question using only the provided Help Centre information
3. Make sure to nicely format the output so it is easy to read on a small screen.
Context : {context} 
User Question: {question}
If you don't know the answer, just say you don't know.
Do NOT try to make up an answer.
If the question is not related to the information about Nicolas Rodriguez,
politely respond that you are tuned to only answer questions about Nicolas Rodriguez experience, education, training and his aspirations.
Use as much detail as possible when responding but keep your answer to up to 200 words.
At the end ask if the user would like to have more information or what else they would like to know about Nicolas Rodriguez. Here is the resume: """ + resume_text 


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

        
        # Prepare the prompt for the API call
        conversation = []
        for message in st.session_state.messages:
            # Map your app's roles to OpenAI's expected roles
            role = "user" if message["role"] == "user" else "assistant"
            conversation.append({"role": role, "content": message["content"]})

        conversation.append({"role": "system", "content": instruction_text})

        # Send message to OpenAI and get response
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        msg = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)



if __name__ == "__main__":
    run()