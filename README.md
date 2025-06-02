# An MLHub Package for Personalized Health Queries

This [MLHub](https://mlhub.au/) package is designed to create a **Retrieval-Augmented Generation (RAG)** system for personalized healthcare queries using large language models (LLMs) and private health data. The system operates locally to ensure privacy is preserved.

## Overview

The system consists of several components working together and makes use of public libraries (such as *LangChain* to orchestrate the retrieval and integration of private health data and *Ollama* as the underlying large language model (LLM) provider) to enable personalized health queries:

1. **Document Ingestion**: Documents (such as lab reports or health records) are loaded and processed into smaller chunks. Supported formats include PDF, TXT, DOCX, and MD.

2. **Vector Store Creation**: The chunks of text are then converted into embeddings using an LLM, such as nomic-embed-text, and stored in a FAISS vector store. This allows for fast similarity-based searches on the data.

3. **Query Execution**: When a user submits a query, the system uses the vector store to find relevant information and generate a response. The query can be processed using RAG techniques, combining the retrieved information with the language model’s generation capabilities.

This system ensures that healthcare queries can be answered using personal data without compromising privacy, as all computations happen locally.

## Quick Start

First, you'll need to install the [mlhub](https://github.com/mlhubber/mlhub) package and [health_rag](https://github.com/ar4152/health_rag), then configure them. This process may take some time depending on your system and internet speed.

```bash
# Install and configure mlhub
pip3 install mlhub
ml configure

# Install and configure health_rag
ml install ar4152/health_rag@main
ml configure health_rag
```

Now, run a simple example. This should execute quickly.

```bash
# Download sample health data
wget https://www.testing.com/wp-content/uploads/2021/07/CBC-sample-report-with-notes_0.pdf -O sample_lab_report.pdf

# Create a context with the downloaded report
ml create_context health_rag sample_lab_report.pdf

# Ask a query related to the report
ml query health_rag "What is my RBC count? Is it normal?"
```

## Detailed Usage - Command Line Tools


### `create_context` - Create FAISS Vector Store

This script generates a **FAISS vector store** from your documents, which enables fast, similarity-based query processing. To create the vector store:

```bash
ml create_context health_rag <path_to_documents> --save_dir <path_to_save_vectorstore>
```

It supports various document formats (PDF, TXT, DOCX, and MD).

### `pull_model` - Pull LLM Models

You can pull additional models using the `pull_model.py` script:

```bash
ml pull_model health_rag <model_name>
```

### `remove_model` - Remove LLM Models

If you need to remove a model, use the `remove_model.py` script:

```bash
ml remove_model health_rag <model_name>
```

### Execute Queries

Once your vector store is ready, you can query the system. You can either use the vector store for RAG or directly query the model. Use the `query.py` script to run a query:

```bash
ml query health_rag <query_string> [--vectorstore-path <path_to_vectorstore>]
```

### Default Models

- Embedding Model: The default model for generating embeddings from the document chunks is [`nomic-embed-text`](https://ollama.com/library/nomic-embed-text). You can replace it with any other model if preferred by using the --embedding_model flag when creating the context.

- Query Model: By default, queries are processed using [`llama3.2:1b`](https://ollama.com/library/llama3.2:1b).



## License
This code is licensed under the [MIT License](./LICENSE).
