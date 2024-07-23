import streamlit as st
from utils import get_answer_from_kb
@st.cache_resource
def initialize():
    return get_answer_from_kb

st.session_state.get_answer_from_kb = initialize()


st.title("MLSAide")
st.markdown("""
##### Welcome to MLSAide, your dedicated chatbot designed to assist MLSA students with all their questions and needs. Whether you're looking for information on courses, events, resources, or general academic advice, MLSAide is here to provide quick and accurate answers. Just type in your query, and let MLSAide guide you through your academic journey with ease and efficiency.
""")
with st.sidebar:
    st.header("About MLSAide")
    
    st.subheader("MLSAide can assist you with:")
    st.markdown("""
    - MLSA program details
    - Ambassador opportunities and tasks
    - Technical skills development
    """)
    
    st.subheader("Example questions:")
    st.markdown("""
    - "How do I become an MLSA?"
    - "Where can I find Azure learning paths?"
    """)
        
    st.subheader("Official Resources:")
    st.markdown("[MLSA Program Page](https://mvp.microsoft.com/studentambassadors)")
    st.markdown("[Microsoft Learn](https://docs.microsoft.com/learn)")
    st.markdown("[SA-Handbook](https://stdntpartners.sharepoint.com/sites/SAProgramHandbook)")
    st.markdown("<p style='text-align: center;'>Made with ❤️ by Mohammed Raza © 2024</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = st.session_state.get_answer_from_kb(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})    
