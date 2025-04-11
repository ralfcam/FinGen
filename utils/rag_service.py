"""
RAG (Retrieval Augmented Generation) Service module.
Provides functionality for document ingestion, storage, retrieval,
and generation of responses based on retrieved context.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Generator, Optional, Union

# Langchain imports - using specific packages to prevent deprecation
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# Use OllamaEmbeddings for nomic model, or HuggingFaceEmbeddings if using a different local model
from langchain_community.embeddings import OllamaEmbeddings # Changed from HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

# Import our llm_service for LLM access
from .llm_service import get_llm_client

# Get logger
logger = logging.getLogger(__name__)

# Configuration from environment variables with defaults
DOCS_DIR = os.environ.get("FINGEN_DOCS_DIR", "./docs")
VECTOR_STORE_DIR = os.environ.get("FINGEN_VECTOR_STORE_DIR", "./chroma_db")
CHUNK_SIZE = int(os.environ.get("FINGEN_CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.environ.get("FINGEN_CHUNK_OVERLAP", "200"))
EMBEDDING_MODEL_NAME = os.environ.get("FINGEN_EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434") # Needed for OllamaEmbeddings
VECTOR_DB_COLLECTION_NAME = "fingen_docs"

# Singleton instances
_vector_store = None
_embedding_function = None

def get_embedding_function():
    """Initializes and returns the embedding function."""
    global _embedding_function
    if _embedding_function is None:
        try:
            # Assuming nomic-embed-text runs via Ollama
            _embedding_function = OllamaEmbeddings(
                model=EMBEDDING_MODEL_NAME,
                base_url=OLLAMA_BASE_URL
            )
            logger.info(f"Initialized OllamaEmbeddings with model: {EMBEDDING_MODEL_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize OllamaEmbeddings: {e}. Falling back to default CPU embeddings (this may be slow).")
            # Fallback or raise error - using HF embeddings as a fallback example
            # from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
            # _embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            raise RuntimeError(f"Could not initialize embedding model {EMBEDDING_MODEL_NAME}: {e}") from e
    return _embedding_function

def get_vector_store() -> Optional[Chroma]:
    """
    Get or initialize the Chroma vector store.
    Uses pre-configured embedding function and persistence path.
    Configures collection metadata for cosine similarity search.
    
    Returns:
        Optional[Chroma]: The initialized Chroma vector store instance.
    """
    global _vector_store
    if _vector_store is None:
        if not os.path.exists(VECTOR_STORE_DIR):
            logger.warning(
                f"Vector store directory {VECTOR_STORE_DIR} not found. "
                f"Please run initialize_documents() first or ensure it exists."
            )
            return None
        try:
            embedding_func = get_embedding_function()
            _vector_store = Chroma(
                collection_name=VECTOR_DB_COLLECTION_NAME,
                embedding_function=embedding_func,
                persist_directory=VECTOR_STORE_DIR,
                collection_metadata={"hnsw:space": "cosine"} # Optimize for cosine similarity
            )
            logger.info(f"Initialized Chroma vector store from {VECTOR_STORE_DIR} with collection '{VECTOR_DB_COLLECTION_NAME}'")
        except Exception as e:
            logger.exception(f"Failed to initialize Chroma vector store from {VECTOR_STORE_DIR}: {e}")
            _vector_store = None # Ensure it's None if init fails
            
    return _vector_store

def initialize_documents() -> bool:
    """
    Load documents from the DOCS_DIR, split them, embed them,
    and store them in the Chroma vector store.
    Will create the vector store if it doesn't exist.
    
    Returns:
        bool: True if successful, False otherwise
    """
    global _vector_store
    try:
        if not os.path.exists(DOCS_DIR) or not os.listdir(DOCS_DIR):
            logger.warning(f"Documents directory '{DOCS_DIR}' is empty or does not exist. No documents to initialize.")
            return False

        logger.info(f"Initializing documents from directory: {DOCS_DIR}")
        # Simple loader for text files - expand with UnstructuredFileLoader for more types
        loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
        docs = loader.load()
        
        if not docs:
            logger.warning(f"No documents found in {DOCS_DIR}. Vector store not initialized.")
            return False

        logger.info(f"Loaded {len(docs)} documents.")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        splits = text_splitter.split_documents(docs)
        logger.info(f"Split documents into {len(splits)} chunks.")

        embedding_func = get_embedding_function()
        logger.info(f"Creating new Chroma vector store at {VECTOR_STORE_DIR}...")
        
        # Use Chroma.from_documents to create and persist in one step
        _vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embedding_func,
            collection_name=VECTOR_DB_COLLECTION_NAME,
            persist_directory=VECTOR_STORE_DIR,
            collection_metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Successfully initialized and persisted vector store with {len(splits)} document chunks.")
        return True

    except Exception as e:
        logger.exception(f"Error during document initialization: {e}")
        _vector_store = None # Ensure vector store is not considered initialized
        return False

def stream_rag_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream responses using RAG (Retrieval Augmented Generation).
    (Placeholder - to be fully implemented in Phase 2)
    
    Args:
        prompt (str): User prompt to send to the RAG chain
        
    Yields:
        str: Content chunks from the RAG response
    """
    vector_store = get_vector_store()
    if vector_store is None:
        logger.error("Vector store not initialized. Cannot perform RAG.")
        yield "[Error: Knowledge base not available. Please initialize documents first.]"
        return
        
    # Placeholder implementation - will be expanded in Phase 2
    logger.info("stream_rag_response() is currently a placeholder - RAG chain not built")
    # Example of retrieval (without full chain)
    try:
        retriever = vector_store.as_retriever()
        relevant_docs = retriever.invoke(prompt)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        logger.info(f"Retrieved context for prompt '{prompt[:50]}...':\n{context[:200]}...")
        yield f"(Placeholder RAG) Context retrieved: {len(relevant_docs)} documents. LLM generation step not implemented."
    except Exception as e:
        logger.exception("Error during placeholder RAG retrieval")
        yield f"[Error retrieving context: {e}]" 