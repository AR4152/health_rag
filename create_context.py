# ------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2025 Arjun Raj
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

"""
MLHub Toolkit for health_rag - create_context.

Author: Arjun Raj
Date: 2025-06-02
Version: 0.0.1

Command-line utility for generating FAISS vector stores from document files.
This tool reads documents from specified file paths or directories, processes
them into chunks, generates embeddings using an LLM model via Ollama, and saves
them into a FAISS vector store for efficient similarity search.

Usage:
    ml create_context health_rag <path1> <path2> ... [--save_dir <directory>]
        [--embedding_model <model_name>]
"""

import argparse
import os
import glob
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings


def create_vector_store(input_paths, save_dir="vector_store", embedding_model="nomic-embed-text"):
    """
    Create a vector store from a list of files and/or folders.

    Args:
        input_paths (list[str]): List of file or folder paths.
        save_dir (str): Directory path to save the vector store.
        embedding_model (str): Model name for embeddings.

    Supported file formats: .pdf, .txt, .docx, .md
    """
    supported_extensions = {".pdf", ".txt", ".docx", ".md"}
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    file_list = []

    # Gather all files
    for path in input_paths:
        if not os.path.exists(path):
            print(f"Path not found: {path}")
            continue

        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            # Recursively add all supported files from the folder
            for ext in supported_extensions:
                file_list.extend(glob.glob(os.path.join(path, f"**/*{ext}"), recursive=True))

    if not file_list:
        print("No valid files found to process.")
        return

    for file_path in file_list:
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif ext == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
            elif ext == ".docx":
                loader = Docx2txtLoader(file_path)
            elif ext == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                print(f"Unsupported file type: {ext}")
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
        input_paths=args.input, save_dir=args.save_dir, embedding_model=args.embedding_model
    )
