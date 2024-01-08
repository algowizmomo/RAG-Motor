# docs_processor.py
from langchain.document_loaders import DirectoryLoader
from transformers import GPT2TokenizerFast
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings  # Import other embeddings as needed

import os

def index_docs(model_name, embedding_model):
    INDEX_DIR = f"faiss_index_{model_name}"
    
    if os.path.exists(INDEX_DIR):
        db = FAISS.load_local(INDEX_DIR, embedding_model)
    else:
        documents = prepare_docs()
        db = FAISS.from_documents(documents, embedding_model)
        db.save_local(INDEX_DIR)
    return db

def prepare_docs():
    # Loading
    loader = DirectoryLoader('./docs/bare/')
    docs = loader.load()

    # Chunking
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=100, chunk_overlap=10
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


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
