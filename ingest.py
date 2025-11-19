# ingest.py

import os
from dotenv import load_dotenv

# Correct imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DATA_DIR = "data"
PERSIST_DIR = "chroma_db"


def load_files():
    docs = []
    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs


def build_vectorstore():
    print("📄 Loading files...")
    raw_docs = load_files()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    split_docs = splitter.create_documents(raw_docs)

    print("⚡ Using FastEmbed (no TensorFlow, no PyTorch)...")
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    print("📦 Creating Chroma vectorstore...")

    # IMPORTANT: use embedding=  (not embedding_function=)
    db = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    

    db.persist()
    print(f"✅ Stored {len(split_docs)} chunks in '{PERSIST_DIR}'")

    return db


if __name__ == "__main__":
    build_vectorstore()
