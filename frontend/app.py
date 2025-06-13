import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION ---
FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="Project Insight", page_icon="🧠", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR FOR FILE UPLOAD ---
with st.sidebar:
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader(
        "Upload a PDF, Word, CSV, or Excel file",
        type=['csv', 'xls', 'xlsx', 'pdf', 'doc', 'docx']
    )

    if uploaded_file:
        with st.spinner("Processing file..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                response = requests.post(f"{FASTAPI_URL}/upload", files=files)
                if response.status_code == 200:
                    st.session_state.dataset = response.json()
                    st.session_state.messages = []  # Reset chat
                    st.success("File processed successfully!")
                else:
                    st.error(f"Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Connection failed. Is the FastAPI backend running?")

# --- MAIN PANEL FOR PREVIEW AND CHAT ---
st.title("🧠 Project Insight: Natural Language Data Analysis")

if st.session_state.dataset:
    st.header("Data Preview")
    if st.session_state.dataset["type"] == "dataframe":
        st.dataframe(pd.DataFrame(st.session_state.dataset["data"]))
    else:
        st.text_area("File Content", st.session_state.dataset["data"], height=300)

    st.header("Chat with Your Data")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                payload = {"message": prompt, "context": st.session_state.dataset["context"]}
                response = requests.post(f"{FASTAPI_URL}/chat", data=payload)
                if response.status_code == 200:
                    bot_response = response.json()["reply"]
                else:
                    bot_response = f"Error: {response.json().get('detail')}"
                st.markdown(bot_response)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
else:
    st.info("Please upload a file using the sidebar to get started.")
