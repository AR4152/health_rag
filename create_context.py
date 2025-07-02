"""MLHub Toolkit for health_rag - create_context.

Command-line utility for generating FAISS vector stores from document files.
This tool reads documents from specified file paths or directories, processes
them into chunks, generates embeddings using an LLM model via Ollama, and saves
them into a FAISS vector store for efficient similarity search.

Usage:
    ml create_context health_rag <path1> <path2> ... [--save_dir <directory>]
        [--embedding_model <model_name>]
"""

import argparse
import glob
import os
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from constant import SUPPORTED_FILE_TYPES
from document_loader import DocumentLoader
from util import normalize_path


def create_vector_store(
    input_paths: List[str],
    save_dir: str = "vector_store",
    embedding_model: str = "nomic-embed-text",
) -> None:
    """Create a vector store from a list of files and/or folders.

    Args:
        input_paths (list[str]): List of file or folder paths.
        save_dir (str): Directory path to save the vector store.
        embedding_model (str): Model name for embeddings.

    Supported file formats: .pdf, .txt, .docx, .md

    """
    # normalise input paths
    input_paths = [normalize_path(p) for p in input_paths]

    all_chunks: List[Document] = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    file_list: List[str] = []

    # Gather all files
    for path in input_paths:
        if not os.path.exists(path):
            print(f"Path not found: {path}")
            continue

        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            # Add all supported files from the folder
            for ext in SUPPORTED_FILE_TYPES:
                file_list.extend(glob.glob(os.path.join(path, f"**/*{ext}")))

    if not file_list:
        print("No valid files found to process.")
        return

    for file_path in file_list:
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in SUPPORTED_FILE_TYPES:
                loader = DocumentLoader(file_path)
            else:
                print(f"Unsupported file type: {file_path}")
                continue

            documents = loader.load()
            chunks = text_splitter.split_documents(documents)
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"Failed to load {file_path}: {e}")

    if not all_chunks:
        print("No valid documents processed.")
        return

    embeddings = OllamaEmbeddings(model=embedding_model)
    db = FAISS.from_documents(all_chunks, embeddings)
    db.save_local(save_dir)

    print(f"Vector store saved to '{save_dir}' with {len(all_chunks)} chunks.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a FAISS vector store from documents.")
    parser.add_argument("input_paths", nargs="+", help="Paths to input files and/or folders.")
    parser.add_argument(
        "--save_dir",
        "-s",
        default="vector_store",
        help="Directory to save the vector store (default: 'vector_store').",
    )
    parser.add_argument(
        "--embedding_model",
        "-m",
        default="nomic-embed-text",
        help="Embedding model to use (default: 'nomic-embed-text').",
    )

    args = parser.parse_args()

    create_vector_store(
        input_paths=args.input_paths, save_dir=args.save_dir, embedding_model=args.embedding_model
    )
