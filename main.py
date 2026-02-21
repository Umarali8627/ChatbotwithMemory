import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG= {'configurable':{'thread_id':'thread-1'}}
st.set_page_config(page_title="LangGraph ChatBot",page_icon=":mortar_board",layout='centered')

st.title("U-Chat")
st.caption("U-Chat Remember everyting")
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
       
         ai_message= st.write_stream(
             message_chunk.content for message_chunk,metadata in  chatbot.stream(
              {'messages':[HumanMessage(content=user_question)]},
             config= {'configurable':{'thread_id':'thread-1'}},
              stream_mode='messages')
          )


    st.session_state.messages.append({'role':'assistant','content':ai_message})