import streamlit as st
import requests

# Groq API Key
GROQ_API_KEY = "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"

# Function to communicate with Groq API
def chat_with_groq(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.json()}"

# Streamlit UI Setup
st.set_page_config(page_title="CampusBuddy Chatbot", layout="centered")
st.title("🤖 CampusBuddy AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = chat_with_groq(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
