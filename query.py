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
MLHub Toolkit for health_rag - query.

Author: Arjun Raj
Date: 2025-06-02
Version: 0.0.1

Command-line tool to execute queries with a Language Model (LLM) with optional FAISS-based
retrieval.

Usage:
    ml query health_rag <query_string> [--vectorstore-path <path_to_vectorstore>]
"""

import os
import argparse
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA


def run_query(query: str, vectorstore_path: str | None):
    """
    Executes a query using a local LLM model, optionally utilizing a FAISS vector store for
    retrieval-augmented generation (RAG).

    Args:
        query (str): The query string to execute.
        vectorstore_path (str | None): Path to the FAISS vector store directory. If None, direct
                                       LLM querying is performed.
    """

    # initialize llm
    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0.8,
        num_predict=256,
    )

    # check if vectorstore is provided and exists
    if vectorstore_path and os.path.exists(vectorstore_path):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        result = qa_chain.run(query)
        print(result)
    else:
        # Perform direct LLM invocation
        messages = [("human", query)]
        response = llm.invoke(messages)
        print(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute a query using an LLM with optional FAISS vector store retrieval."
    )
    parser.add_argument("query", nargs="+", help="The query string to execute.")
    parser.add_argument(
        "--vectorstore-path",
        type=str,
        default=None,
        help="Optional path to the FAISS vector store directory.",
    )
    args = parser.parse_args()

    full_query = " ".join(args.query)
    print(f"Executing Query: {full_query}\n")
    run_query(full_query, args.vectorstore_path)
