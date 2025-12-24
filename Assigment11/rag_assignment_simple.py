# ================================
# RAG ASSIGNMENT - SIMPLE VERSION
# ================================

import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

# ---------------- FOLDERS ----------------
os.makedirs("resumes", exist_ok=True)

# ---------------- EMBEDDING ----------------
embeddings = HuggingFaceEmbeddings(
    model_name="text-embedding-nomic-embed-text-v1.5"
)

# ---------------- VECTOR STORE ----------------
db = Chroma(
    collection_name="resume_db",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)

# ---------------- FUNCTIONS ----------------
def upload_resume(pdf):
    path = f"resumes/{pdf.name}"
    with open(path, "wb") as f:
        f.write(pdf.getbuffer())

    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    for c in chunks:
        c.metadata["resume"] = pdf.name

    db.add_documents(chunks)
    db.persist()

def shortlist(job_desc, k=3):
    docs = db.similarity_search(job_desc, k=k)
    return list(set(d.metadata["resume"] for d in docs))

# ---------------- STREAMLIT UI ----------------
st.title("AI Resume Shortlisting (RAG)")

tab1, tab2 = st.tabs(["Upload Resume", "Shortlist Resumes"])

# ---- UPLOAD ----
with tab1:
    pdf = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if pdf and st.button("Upload"):
        upload_resume(pdf)
        st.success("Resume uploaded and stored")

# ---- SHORTLIST ----
with tab2:
    jd = st.text_area("Enter Job Description")
    if st.button("Shortlist"):
        results = shortlist(jd)
        st.write("### Shortlisted Resumes")
        for r in results:
            st.write("✅", r)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

# 1. Resume text
text = """
Python Developer with experience in AI, ML, LangChain, and ChromaDB.
Worked on resume shortlisting using RAG pipelines.
"""

# 2. Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_text(text)

# 3. Embedding model (PUBLIC + SAFE)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectors = embeddings.embed_documents(chunks)

# 4. Store in Chroma
client = chromadb.Client()
collection = client.get_or_create_collection("resumes")

collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=vectors
)

print("✅ Resume stored successfully!")

# 5. Query
query = "Python developer with machine learning experience"
results = collection.query(
    query_texts=[query],
    n_results=2
)

print("\n🔍 Search Results:")
for doc in results["documents"][0]:
    print("-", doc)
