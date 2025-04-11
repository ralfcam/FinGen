"""
LLM Service module for handling interactions with Ollama.
Provides centralized functionality for initializing the client and streaming responses.
"""

import os
import logging
from typing import Generator, Dict, Any
from ollama import Client

# Get logger
logger = logging.getLogger(__name__)

# Get configuration from environment variables with defaults
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-r1:14b")

# Singleton client instance
_ollama_client = None

def get_ollama_client() -> Client:
    """
    Get or initialize the Ollama client.
    Uses a singleton pattern to avoid reinitializing on every call.
    
    Returns:
        Client: Initialized Ollama client
        
    Raises:
        ConnectionError: If client initialization fails
    """
    global _ollama_client
    if _ollama_client is None:
        try:
            _ollama_client = Client(host=OLLAMA_BASE_URL)
            logger.info(f"Ollama client initialized successfully for host {OLLAMA_BASE_URL}")
        except Exception as e:
            logger.error(f"Error initializing Ollama client at {OLLAMA_BASE_URL}: {e}")
            raise ConnectionError(f"Failed to initialize Ollama client: {e}") from e
    return _ollama_client

def stream_llm_response(prompt: str) -> Generator[str, None, None]:
    """
    Stream responses from the LLM based on the given prompt.
    
    Args:
        prompt (str): User prompt to send to the LLM
        
    Yields:
        str: Content chunks from the LLM response
    """
    try:
        client = get_ollama_client()
        messages = [{'role': 'user', 'content': prompt}]
        
        logger.info(f"Starting Ollama stream with model {OLLAMA_MODEL}")
        stream = client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            # Handle the response structure from ollama Client
            if hasattr(chunk, 'message') and hasattr(chunk.message, 'content'):
                content = chunk.message.content
                yield content
            # Fallback to dictionary access if it's returned as a dict
            elif isinstance(chunk, dict):
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    yield content
                # Handle potential errors in the stream
                elif 'error' in chunk:
                    logger.error(f"Error in Ollama stream chunk: {chunk['error']}")
                    yield f"\n\n[Error: {chunk['error']}]\n"
        
        logger.info("Ollama stream finished successfully")
        
    except ConnectionError as e:
        logger.error(f"Connection error during Ollama streaming: {e}")
        yield f"\n\n[Error: Could not connect to Ollama service. Please ensure it's running and accessible at {OLLAMA_BASE_URL}]\n"
    except Exception as e:
        logger.exception(f"Unexpected error during Ollama streaming: {e}")
        yield f"\n\n[Error generating response: {e}]\n" 