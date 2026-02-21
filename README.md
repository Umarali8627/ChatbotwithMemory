## 🤖 LangGraph ChatBot with Streamlit & Groq

A conversational AI chatbot built using:

🧠 LangGraph for stateful workflow management

🔗 LangChain for message handling

⚡ Groq LLM (LLaMA 3.3 70B) for fast inference

🌐 Streamlit for interactive web UI

This project demonstrates how to build a stateful conversational chatbot using graph-based orchestration.

## 🚀 Features

✅ Stateful conversation using LangGraph

✅ Memory persistence via InMemorySaver

✅ Real-time chat interface with Streamlit

✅ Powered by Groq LLM API

✅ Uses LLaMA 3.3 70B Versatile model

✅ Clean and minimal UI

🏗️ Project Structure
├── app.py              # Streamlit frontend
├── backend.py          # LangGraph chatbot logic
├── .env                # Environment variables (API key)
├── requirements.txt
└── README.md
## 🧠 Architecture Overview
1️⃣ Frontend (Streamlit)

Displays chat history

Accepts user input

Sends message to LangGraph backend

Displays assistant response

2️⃣ Backend (LangGraph)

Defines ChatState

Uses StateGraph

Processes messages via chat_node

Maintains memory using InMemorySaver

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/langgraph-chatbot.git
cd langgraph-chatbot
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key_here

You can get your API key from:
👉 https://console.groq.com/

▶️ Running the Application
streamlit run app.py

The app will start at:

http://localhost:8501
🧩 How It Works
🔹 Chat State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

Maintains conversation history.

🔹 Chat Node
def chat_node(state: ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}

Sends full conversation to LLM

Returns assistant message

Appends to graph state

🔹 Graph Flow
START → chat_node → END

Graph is compiled with memory checkpointing.

🛠 Tech Stack

Python 3.10+

Streamlit

LangChain

LangGraph

Groq API

📦 Required Packages

Add this to your requirements.txt:

streamlit
langchain
langgraph
langchain-groq
python-dotenv
📌 Future Improvements

🔄 Add persistent database memory (Redis / PostgreSQL)

🌐 Add Web Search Tool

🧠 Add RAG (Retrieval Augmented Generation)

🛡️ Add authentication system

📦 Dockerize the application

🧪 Example Usage

User:

What is LangGraph?

Assistant:

LangGraph is a framework for building stateful multi-step LLM applications...
🧑‍💻 Author

Umar Ali
AI Engineer | LangChain & LLM Developer

📜 License

This project is open-source and available under the MIT License.
