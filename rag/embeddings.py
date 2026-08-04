"""
Generate embeddings for policy document chunks and store
them in a persistent Chroma vector database.
"""

import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag.chunker import split_documents

# ----------------------------------------------------
# Project paths
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VECTOR_DB = PROJECT_ROOT / "vector_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_database():

    print("Loading policy chunks...")

    chunks = split_documents()

    print(f"{len(chunks)} chunks loaded.")

    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    print("Embedding model loaded.")

    print("\nCreating Chroma database...")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB),
    )

    print("\nVector database created successfully.")

    print(f"Stored {vectordb._collection.count()} vectors.")

    return vectordb


if __name__ == "__main__":

    build_vector_database()

def get_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    vectordb = Chroma(
        persist_directory=str(VECTOR_DB),
        embedding_function=embeddings,
    )

    return vectordb
