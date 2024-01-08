from docs_processor import index_docs
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings

class MVDAssistant:
    def __init__(self, embedding_model=("OpenAIEmbeddings",OpenAIEmbeddings()), chat_model="gpt-4-1106-preview"):
        self.llm = self.initialize_language_model(chat_model)
        self.db = self.process_documents(*embedding_model)
        self.memory = self.initialize_memory("chat_history", True)
        self.tools = self.setup_tools(self.db)
        self.agent = self.setup_agent(self.tools, self.llm, self.memory, False)

    def initialize_language_model(self, model_name):
        return ChatOpenAI(model_name=model_name)

    def process_documents(self, model_name, embedding_model):
        return index_docs(model_name, embedding_model)

    def initialize_memory(self, memory_key, return_messages):
        return ConversationBufferMemory(memory_key=memory_key, return_messages=return_messages)

    def setup_tools(self, db):
        return [
            Tool(
                name="Retrieve Info",
                description="Tool to retrieve information from the indexed documents.",
                func=lambda q: db.similarity_search(q)
            )
        ]

    def setup_agent(self, tools, llm, memory, verbose):
        return initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=verbose)

    def run_query(self, query):
        for x in range(10): # retry n times
            try:
                res = self.agent.run(query)
                break;
            except Exception as e:
                print("Error:", e)
        return res


def main():
    agent = MVDAssistant()

    q = input("Query: ")
    while q:
        answer = agent.run_query(q)
        print("Answer".center(30, "="))
        print(answer)
        print("="*30)
        q = input("Query: ")

if __name__ == "__main__":
    main()