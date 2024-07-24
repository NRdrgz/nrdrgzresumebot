import streamlit as st
from openai import OpenAI
import os
from streamlit.logger import get_logger
from utils import load_resume_from_pdf

LOGGER = get_logger(__name__)


#Saved in secrets.toml or in Streamlit secrets
#secrets.toml is not merged online thanks to .gitignore
openai_api_key = st.secrets['OPENAI_API_KEY']

# Text version of your resume
resume_path = 'Resume_Nicolas_Rodriguez_ENG_Main.pdf'  
resume_text = load_resume_from_pdf(resume_path)
instruction_text = """ System: You are a CareerBot, a comprehensive, interactive resource for exploring Nicolas Rodriguez background, 
skills, and expertise and answer questions from a Hiring Manager. Be polite and provide answers based on the provided context only. Use only the provided data and not prior knowledge.
Human: Follow exactly these 3 steps:
1. Read the context below
2. Answer the question using only the provided Help Centre information
3. Do not just copy the information from the document. Rephrase it and reformat it.
4. Make sure to nicely format the output so it is easy to read on a small screen.

If you don't know the answer, just say you don't know.
Do NOT try to make up an answer.
If the question is not related to the information about Nicolas Rodriguez,
politely respond that you are tuned to only answer questions about Nicolas Rodriguez experience, education, training and his aspirations.
Use as much detail as possible when responding but keep your answer to up to 200 words.
Remember you should help Nico find a job so answer the Hiring Manager's question to do so.
At the end ask if the user would like to have more information or what else they would like to know about Nicolas Rodriguez. Here is the resume: """ + resume_text 


predefined_questions = [
    "What are Nico's strong and soft skills?",
    "What can you tell me about Nico's latest working experience?",
    "Should I hire Nico?",
    # Add more predefined questions here
]

def run():
    
    st.set_page_config(
        page_title="Resume Bot",
        page_icon="🤖",
    )

    st.write("# Welcome to Nicolas Rodriguez's Resume Bot! 👋")


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Welcome! I'm Nico's Resume Bot, specialized in providing information about Nicolas Rodriguez's professional background and qualifications.\n Feel free to ask me anything or click on pre-defined questions such as:"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    for question in predefined_questions:
        #If click on the button
        if st.button(question):
            handle_question(question, st.session_state)


    if prompt := st.chat_input():
        handle_question(prompt, st.session_state)

#Function to handle the LLM answering a question
def handle_question(question, st_session_state):
    #Add the question to the Streamlit session state
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Placeholder for response message
    response_placeholder = st.empty()

    # Display 'Generating answer...' in the placeholder
    response_placeholder.text("Generating answer...")

    
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
        model="gpt-4o-mini",
        messages=conversation
    )
    msg = response.choices[0].message.content

    #Update with empty text
    response_placeholder.text("")

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


if __name__ == "__main__":
    run()