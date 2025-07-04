"""MLHub Toolkit for health_rag - query.

Command-line tool to execute queries with a Language Model (LLM) with FAISS-based retrieval.

Usage:
    ml query health_rag <query_string> [--vectorstore_path <path_to_vectorstore>]
"""

import argparse
import os

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings


def run_query(query: str, vectorstore_path: str | None) -> None:
    """Execute a query using a local LLM model, optionally utilizing a FAISS vector store for
    retrieval-augmented generation (RAG).

    Args:
        query (str): The query string to execute.
        vectorstore_path (str | None): Path to the FAISS vector store directory. If None, direct
                                       LLM querying is performed.

    """  # noqa: D205
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
        result = qa_chain.invoke(query)
        print(result.get("result"))
    else:
        # Perform direct LLM invocation
        messages = [("human", query)]
        response = llm.invoke(messages)
        print(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute a query using an LLM with optional FAISS vector store retrieval.",
        usage="ml query health_rag <query_string> [--vectorstore-path <path_to_vectorstore>]",
    )
    parser.add_argument("query", nargs="+", help="The query string to execute.")
    parser.add_argument(
        "--vectorstore_path",
        type=str,
        default=None,
        help="Optional path to the FAISS vector store directory.",
    )
    args = parser.parse_args()

    full_query = " ".join(args.query)
    run_query(full_query, args.vectorstore_path)
