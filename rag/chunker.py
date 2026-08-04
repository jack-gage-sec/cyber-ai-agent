"""
Splits policy documents into chunks suitable for RAG.
"""

import os
import sys

from pathlib import Path

dir_above_cep = Path(__file__).resolve().parents[2]
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), dir_above_cep))

external_path = os.path.join(parent_dir, "Compliance-AI")
sys.path.append(external_path)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loaders import load_documents


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_documents():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    chunks = split_documents()

    print(f"\nGenerated {len(chunks)} chunks.\n")

    for i, chunk in enumerate(chunks[:5]):

        print("=" * 70)
        print(f"Chunk {i+1}")
        print("=" * 70)

        print("Metadata:")
        print(chunk.metadata)

        print("\nContent:")
        print(chunk.page_content)

        print()
