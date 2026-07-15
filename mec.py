import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(
    page_title="MEC Student Assistant",
    page_icon="🎓"
)

st.title("🎓 MEC Student Assistant")
st.caption("Muthayammal Engineering College AI Assistant")

with open("knowledge.txt","r",encoding="utf-8") as f:
    college_info = f.read()

def fetch_mec_homepage():
    try:
        url = "https://mec.edu.in/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text,"html.parser")
        text = soup.get_text(separator="\n")
        return text[:12000]
    except:
        return "Unable to fetch website."

website_content = fetch_mec_homepage()

SYSTEM_PROMPT = f"""
You are an AI Assistant for Muthayammal Engineering College.

Answer only questions related to MEC.

College Information:

{college_info}

Website Data:

{website_content}

Rules:

1. Be professional.

2. If the answer is unavailable, say:
'I couldn't find that information.'

3. Never invent attendance, marks or CGPA.

4. If user asks personal academic data tell them login is required.
"""

if "messages" not in st.session_state:
    st.session_state.messages=[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything about MEC")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ]

    messages.extend(st.session_state.messages)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )

    answer=response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        } 
    )

    with st.chat_message("assistant"):
        st.write(answer)