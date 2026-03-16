import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="Chat | FinSight AI", page_icon="💬", layout="wide")

st.title("💬 AI Financial Chat")
st.caption("Ask anything about stocks, finance, or investing")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if st.button("Clear Chat"):
    st.session_state.chat_messages = []
    st.rerun()

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything about stocks or finance..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                llm = ChatGroq(
                    api_key=os.environ["GROQ_API_KEY"],
                    model="llama-3.1-8b-instant"
                )

                system = SystemMessage(content="""You are FinSight AI, an expert financial analyst assistant.
You help users understand stocks, financial metrics, investment strategies, and market trends.
Give clear, accurate, professional answers. Always mention this is not financial advice.""")

                history = [system]
                for m in st.session_state.chat_messages:
                    if m["role"] == "user":
                        history.append(HumanMessage(content=m["content"]))
                    else:
                        history.append(AIMessage(content=m["content"]))

                response = llm.invoke(history)
                st.markdown(response.content)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response.content
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")