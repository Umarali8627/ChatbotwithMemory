import streamlit as st
from backend import chatbot,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


messages=[]
# utility function which create unique id 
def genrate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def generate_chat_title(text, max_len=30):
    if not text:
        return "New Chat"
    cleaned = " ".join(str(text).strip().split())
    if not cleaned:
        return "New Chat"
    return cleaned if len(cleaned) <= max_len else cleaned[:max_len].rstrip() + "..."

def reset_chat():
    thread_id= genrate_thread_id()
    st.session_state['thread_id']=thread_id
    store_thread_id(st.session_state.thread_id)
    st.session_state.messages=[]
def store_thread_id(thread_id, title="New Chat"):
    for chat in st.session_state.chat_threads:
        if chat["thread_id"] == thread_id:
            return
    st.session_state.chat_threads.append({"thread_id": thread_id, "title": title})

def rename_chat_thread(thread_id, text):
    for chat in st.session_state.chat_threads:
        if chat["thread_id"] == thread_id:
            chat["title"] = generate_chat_title(text)
            return

def infer_chat_title_from_messages(messages):
    for message in messages:
        if isinstance(message, HumanMessage):
            return generate_chat_title(message.content)
    return "New Chat"

def load_conversations(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])




st.set_page_config(page_title="LangGraph ChatBot",page_icon=":mortar_board",layout='centered')

st.title("U-Chat")
st.caption("U-Chat Remember everyting")
# messages states
# **** session state*****
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=genrate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state.chat_threads=retrieve_all_threads()
# migrate old format: [thread_id, ...] to [{"thread_id": ..., "title": ...}]
if st.session_state.chat_threads and not isinstance(st.session_state.chat_threads[0], dict):
    st.session_state.chat_threads = [
        {"thread_id": tid, "title": f"Chat {idx + 1}"}
        for idx, tid in enumerate(st.session_state.chat_threads)
    ]
store_thread_id(st.session_state.thread_id)
# *****Side bar UI *******
st.sidebar.title('U-Chat')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')
# st.sidebar.markdown(st.session_state['thread_id'])
for chat in st.session_state.chat_threads[::-1]:
    thread_id = chat["thread_id"]
    label = chat.get("title", "New Chat")
    if label == "New Chat" or label.startswith("Chat "):
        inferred_title = infer_chat_title_from_messages(load_conversations(thread_id))
        if inferred_title != label:
            rename_chat_thread(thread_id, inferred_title)
            label = inferred_title
    if st.sidebar.button(label, key=f"thread_{thread_id}"):
        st.session_state.thread_id=thread_id
        messages= load_conversations(thread_id)

        # now set the messages 
        temp_dict= []
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_dict.append({'role':role,'content':message.content})
        st.session_state.messages=temp_dict



# adding messsages in Dashboard****
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
user_question=st.chat_input("Ask Something")

if user_question:
    st.session_state.messages.append({"role":'user',"content":user_question})
    rename_chat_thread(st.session_state['thread_id'], user_question)
    with st.chat_message('user'):
        st.markdown(user_question)
    
    CONFIG= {'configurable':{'thread_id':st.session_state['thread_id']}}
    with st.chat_message('assistant'):
       
         ai_message= st.write_stream(
             message_chunk.content for message_chunk,metadata in  chatbot.stream(
              {'messages':[HumanMessage(content=user_question)]},
             config= CONFIG,
              stream_mode='messages')
          )


    st.session_state.messages.append({'role':'assistant','content':ai_message})
