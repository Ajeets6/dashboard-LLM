from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
import os
import tempfile
from pathlib import Path

def create_vectorstore(temp_file_path="data.csv"):

    loader = CSVLoader(file_path=temp_file_path)
    docs = loader.load()
    os.remove(temp_file_path)
    embeddings = OllamaEmbeddings(model="granite-embedding:latest")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Embed and store in ChromaDB
    embeddings = OllamaEmbeddings(model="granite-embedding:latest")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vectorstore
