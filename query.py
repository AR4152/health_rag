# MLHub toolkit for health_rag - query
# ml query health_rag

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import click
import os
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("query", required=True)
@click.option("--vectorstore-path", default=None, help="Optional path to FAISS vector store directory.")

def cli(query: str, vectorstore_path: str | None):
    """
    Run a query using the LLM, optionally with a FAISS vector store for retrieval.
    """

    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0.8,
        num_predict=256,
    )

    if vectorstore_path and os.path.exists(vectorstore_path):
        embeddings = OllamaEmbeddings(model="llama3.2:1b")
        db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        result = qa_chain.run(query)
        print(result)
    else:
        messages = [("human", query)]
        ai_msg = llm.invoke(messages)
        print(ai_msg.content)

if __name__ == "__main__":
    cli(prog_name="query")
