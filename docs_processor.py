from langchain.document_loaders import DirectoryLoader
from transformers import GPT2TokenizerFast
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

import os
clear = lambda:os.system("clear")

INDEX_DIR = "faiss_index"
embeddings = OpenAIEmbeddings()

def prepare_docs():
    # Loading
    loader = DirectoryLoader('docs')
    docs = loader.load()

    # Chunking
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=100, chunk_overlap=10
    )
    chunks = text_splitter.split_documents(docs)
    return chunks

def index_docs():
    if os.path.exists(INDEX_DIR):
        db = FAISS.load_local("faiss_index", embeddings)
    else:
        documents = prepare_docs()
        db = FAISS.from_documents(documents, OpenAIEmbeddings())
        db.save_local(INDEX_DIR)
    return db


def main():

    db = index_docs()
    q = ""
    while q!="q":
        q = input("Query:")
        documents = db.similarity_search(q)
        for doc in documents:
            print(doc.page_content)
            print(doc.metadata)
            print("="*30)

if __name__ == "__main__":
    main()
