"""
LLM Service module for handling interactions with Large Language Models.
Provides centralized functionality for initializing clients and streaming responses.
Uses Langchain for better integration with other components.
"""

import os
import logging
from typing import Generator, Dict, Any, List, Optional

# Langchain imports
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig

# Get logger
logger = logging.getLogger(__name__)

# Get configuration from environment variables with defaults
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-r1:14b")
OLLAMA_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.7"))

# Singleton client instance
_langchain_ollama_client = None

def get_llm_client() -> ChatOllama:
    """
    Get or initialize the Langchain ChatOllama client.
    Uses a singleton pattern to avoid reinitializing on every call.
    
    Returns:
        ChatOllama: Initialized Langchain ChatOllama client
        
    Raises:
        ConnectionError: If client initialization fails
    """
    global _langchain_ollama_client
    if _langchain_ollama_client is None:
        try:
            _langchain_ollama_client = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL,
                temperature=OLLAMA_TEMPERATURE,
            )
            logger.info(f"Langchain ChatOllama client initialized successfully for model {OLLAMA_MODEL} at {OLLAMA_BASE_URL}")
        except Exception as e:
            logger.error(f"Error initializing Langchain ChatOllama client: {e}")
            raise ConnectionError(f"Failed to initialize Langchain ChatOllama client: {e}") from e
    return _langchain_ollama_client

def stream_llm_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream responses from the LLM based on the given prompt.
    Uses Langchain for streaming.
    
    Args:
        prompt (str): User prompt to send to the LLM
        
    Yields:
        str: Content chunks from the LLM response
    """
    try:
        llm = get_llm_client()
        messages = [HumanMessage(content=prompt)]
        
        logger.info(f"Starting Langchain stream with model {OLLAMA_MODEL}")
        
        # Stream the response
        for chunk in llm.stream(messages):
            if hasattr(chunk, 'content'):
                yield chunk.content
        
        logger.info("Langchain stream finished successfully")
        
    except ConnectionError as e:
        logger.error(f"Connection error during Langchain streaming: {e}")
        yield f"\n\n[Error: Could not connect to Ollama service. Please ensure it's running and accessible at {OLLAMA_BASE_URL}]\n"
    except Exception as e:
        logger.exception(f"Unexpected error during Langchain streaming: {e}")
        yield f"\n\n[Error generating response: {e}]\n"

# For backward compatibility
def get_ollama_client() -> ChatOllama:
    """
    Legacy function for backward compatibility.
    Now returns the Langchain ChatOllama client.
    
    Returns:
        ChatOllama: The Langchain ChatOllama client
    """
    logger.warning("get_ollama_client() is deprecated, use get_llm_client() instead")
    return get_llm_client() 