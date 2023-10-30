from docs_processor import index_docs
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(model="gpt-4")
db = index_docs()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools= [
    Tool(
        name="Retrieve Info", 
        description="Useful tool to retrieve information about Motor Vehicle and Road Transport Laws and Rules in India. query with a list of keywords for similarity search", 
        func=db.similarity_search
    )
]
agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=False)
q = input("Query: ")
while q:
    answer = agent.run(q)
    
    print("Answer".center(30, "="))
    print(answer)
    print("="*30)
          
    q = input("Query: ")