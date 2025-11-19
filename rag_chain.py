# rag_chain.py
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.vectorstores import Chroma
from prompts import ITINERARY_PROMPT
from dotenv import load_dotenv
load_dotenv()

PERSIST_DIR = "chroma_db"

def load_db():
    # Open existing Chroma DB
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=None)  # embedding_function none since persisted
    return db

def generate_itinerary(days: int, preferences: str, top_k: int = 6):
    # Load DB and retriever
    db = load_db()
    retriever = db.as_retriever(search_kwargs={"k": top_k})

    # Build query from user preferences
    query = f"{preferences} travel attractions, restaurants, tips"

    docs = retriever.get_relevant_documents(query)
    snippet_texts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        snippet_texts.append(f"({src}) {d.page_content[:400].strip()}")

    retrieved_snippets = "\n\n".join(snippet_texts)

    # LLM chain
    llm = OpenAI(temperature=0.7, max_tokens=600)
    chain = LLMChain(llm=llm, prompt=ITINERARY_PROMPT)
    result = chain.run({"days": days, "preferences": preferences, "retrieved_snippets": retrieved_snippets})
    return result
