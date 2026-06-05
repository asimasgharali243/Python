import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="HealthGuard AI", page_icon="🏥", layout="wide")

st.title("🏥 HealthGuard AI")
st.warning("Educational information only. Not medical advice.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("HealthGuard AI")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask a health question")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt, st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})
