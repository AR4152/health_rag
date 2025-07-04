# MLHub Health RAG Toolkit - Commands

This toolkit provides **five main commands** to help you work with personal health information and large language models (**LLMs**) locally.

Below you’ll find a **command-by-command reference**.


## Table of Contents

1. [chat\_mode](#chat_mode) - Interactive chat assistant with memory
2. [query](#query) - Answer medical queries with optional retrieval
3. [pull\_model](#pull_model) - Download LLM models
4. [remove\_model](#remove_model) - Remove LLM models
5. [create\_context](#create_context) - Create a FAISS vector store


## `chat_mode`

**Interactive chat assistant with memory.**

**Description:**
Starts an interactive conversation with the model. All prompts and responses are remembered within the same session for contextual continuity.

**Usage:**

```bash
ml chat_mode health_rag [--session-id <session_id>]
```

**Examples:**

* Start default session:

  ```bash
  ml chat_mode health_rag
  ```
* Start named session:

  ```bash
  ml chat_mode health_rag --session-id my_session
  ```

**Notes:**

* To exit, type `exit` or `quit`.
* Default model: `llama3.2:1b`
* Session memory is stored in memory (not persisted to disk).


## `query`

**Answer medical queries using personal health information with optional retrieval-augmented generation (RAG).**

**Description:**
Executes a query using a local LLM (default: `llama3.2:1b`). If a **FAISS vector store** path is provided, the query uses **retrieval-augmented generation** to combine your stored health documents with the model’s output.

**Usage:**

```bash
ml query health_rag "<query_string>" [--vectorstore_path <path_to_vectorstore>]
```

**Examples:**

* Direct query:

  ```bash
  ml query health_rag "Explain my RBC count."
  ```
* Query with retrieval:

  ```bash
  ml query health_rag "What is my cholesterol level?" --vectorstore_path vector_store/
  ```

**Notes:**

* If `--vectorstore_path` is omitted, the query goes directly to the model without using your data.
* Embedding model for retrieval defaults to `nomic-embed-text`.


## `pull_model`

**Download (pull) a specified LLM model locally via Ollama.**

**Description:**
Fetches and installs an LLM so it can be used offline.

**Usage:**

```bash
ml pull_model health_rag <model_name>
```

**Examples:**

```bash
ml pull_model health_rag llama3.2:1b
```

**Notes:**

* Make sure the Ollama CLI is installed and configured.
* You can pull any compatible model (e.g., `nomic-embed-text`, `llama3.2:70b`, etc.).

## `remove_model`

**Remove a specified LLM model from your local storage.**

**Description:**
Deletes a previously pulled model to free disk space.

**Usage:**

```bash
ml remove_model health_rag <model_name>
```

**Examples:**

```bash
ml remove_model health_rag llama3.2:1b
```

**Notes:**

* Use this when you no longer need a model locally.


## `create_context`

**Create a FAISS vector store from documents for efficient retrieval.**

**Description:**
Loads files or folders, splits them into text chunks, generates embeddings, and saves them to a FAISS vector store for later queries.

**Usage:**

```bash
ml create_context health_rag <path1> <path2> ... [--save_dir <directory>] [--embedding_model <model_name>]
```

**Examples:**

* Create a vector store from a folder:

  ```bash
  ml create_context health_rag ~/Documents/HealthData --save_dir vector_store
  ```
* Use a different embedding model:

  ```bash
  ml create_context health_rag report.pdf --embedding_model nomic-embed-text
  ```

**Notes:**

* **Supported file formats:**
  `.pdf`, `.txt`, `.docx`, `.md`, `.csv`, `.eml`, `.xlsx`, `.xls`, `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`
* Default embedding model: `nomic-embed-text`
* Default save directory: `vector_store`
