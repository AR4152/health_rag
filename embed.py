from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os

def create_vector_store_from_files(file_paths, save_dir="vector_store", embedding_model="nomic-embed-text"):
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for path in file_paths:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue

        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(path)
            elif ext == ".txt":
                loader = TextLoader(path, encoding="utf-8")
            elif ext == ".docx":
                loader = Docx2txtLoader(path)
            elif ext == ".md":
                loader = UnstructuredMarkdownLoader(path)
            else:
                print(f"Unsupported file type: {ext}")
                continue

            documents = loader.load()
            chunks = text_splitter.split_documents(documents)
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"Failed to load {path}: {e}")

    if not all_chunks:
        print("No valid documents processed.")
        return

    embeddings = OllamaEmbeddings(model=embedding_model)
    db = FAISS.from_documents(all_chunks, embeddings)
    db.save_local(save_dir)

    print(f"Vector store saved to '{save_dir}' with {len(all_chunks)} chunks.")

create_vector_store_from_files(['/home/arjun/Documents/comp3740/health_rag/CBC-sample-report-with-notes_0.pdf'])
