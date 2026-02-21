import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG= {'configurable':{'thread_id':'thread-1'}}
st.set_page_config(page_title="LangGraph ChatBot",page_icon=":mortar_board",layout='centered')

st.title("")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
user_question=st.chat_input("Ask Something")

if user_question:
    st.session_state.messages.append({"role":'user',"content":user_question})
    with st.chat_message('user'):
        st.markdown(user_question)
    
    with st.chat_message('assistant'):
       with st.spinner('Thinking...'):
        ai_message=''
        try:
           response= chatbot.invoke({'messages':[HumanMessage(content=user_question)]},config=CONFIG)
           ai_message=response['messages'][-1].content
        except Exception as ex:
            st.markdown(ex)
        st.markdown(ai_message)
        st.session_state.messages.append({'role':'assistant','content':ai_message})