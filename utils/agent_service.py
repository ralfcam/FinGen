"""
Agent Service module for handling stateful agent interactions.
Provides functionality for building and running LangGraph-based agents
with persistent memory and advanced workflows.
"""

import os
import logging
import datetime
from typing import List, Dict, Any, Generator, Optional, Union, Literal
from pydantic import BaseModel, Field

# Langchain imports
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.documents import Document

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import AsyncSqliteSaver

# Local imports
from .llm_service import get_llm_client
from .rag_service import get_vector_store, initialize_documents # Assuming initialize_documents might be called elsewhere

# Get logger
logger = logging.getLogger(__name__)

# Configuration
LONG_TERM_MEMORY_CUTOFF_DAYS = int(os.environ.get("FINGEN_MEMORY_CUTOFF_DAYS", "30"))
MAX_LONG_TERM_MEMORIES_IN_STATE = int(os.environ.get("FINGEN_MAX_MEMORIES_IN_STATE", "5"))
MEMORY_PRUNING_THRESHOLD = int(os.environ.get("FINGEN_MEMORY_PRUNING_THRESHOLD", "10")) # When to trigger prune node

# --- Agent State Definition ---

class EnhancedMessageState(BaseModel):
    """Defines the state for our stateful agent, including memory.
    
    Uses Pydantic for validation and structure.
    Separates short-term (message history) and long-term (retrieved context) memory.
    Includes session ID for isolation and a persistence mode.
    """
    short_term: List[BaseMessage] = Field(default_factory=list)
    long_term: List[str] = Field(default_factory=list) # Stores retrieved page_content strings
    session_id: str
    # memory_type: Literal["volatile", "persistent"] = "persistent" # Deferring pruning trigger logic

# --- Checkpointer for Short-Term Memory / State Persistence ---

# Use in-memory SQLite for simplicity in this example.
SQLITE_CHECKPOINT_PATH = os.environ.get("FINGEN_SQLITE_CHECKPOINT_PATH", ":memory:")
memory_checkpointer = AsyncSqliteSaver.from_conn_string(SQLITE_CHECKPOINT_PATH)
logger.info(f"LangGraph checkpointer configured with: {SQLITE_CHECKPOINT_PATH}")

# --- Helper Functions ---

def get_temporal_cutoff() -> float:
    """Calculate the timestamp cutoff for long-term memory retrieval."""
    cutoff_delta = datetime.timedelta(days=LONG_TERM_MEMORY_CUTOFF_DAYS)
    return (datetime.datetime.now(datetime.timezone.utc) - cutoff_delta).timestamp()

def get_old_memories(session_id: str) -> Optional[List[str]]:
    """Retrieve IDs of memories older than the cutoff for a specific session.
    
    Note: This assumes the vector store *contains* timestamp metadata.
    The actual addition of this metadata needs to happen when memories are saved.
    This function only implements the *retrieval* logic for pruning.
    """
    vector_store = get_vector_store()
    if not vector_store:
        logger.error("Cannot get old memories: Vector store not available.")
        return None
        
    try:
        cutoff_timestamp = get_temporal_cutoff()
        # This assumes metadata keys 'session_id' and 'timestamp' exist
        # Chroma filtering syntax might vary slightly based on version
        filter_criteria = {
            "$and": [
                {"session_id": {"$eq": session_id}},
                {"timestamp": {"$lt": cutoff_timestamp}}
            ]
        }
        
        # Fetch documents with metadata (including IDs) matching the filter
        # The exact method might depend on the Chroma version and API.
        # This is a conceptual example; direct ID retrieval might require a different approach.
        results = vector_store.get(where=filter_criteria, include=["metadatas"]) # Fetch metadata to confirm, then IDs
        
        if results and results.get('ids'):
            logger.info(f"Found {len(results['ids'])} old memories to potentially prune for session {session_id}.")
            return results['ids']
        else:
            logger.info(f"No old memories found for pruning for session {session_id}.")
            return []
            
    except Exception as e:
        logger.exception(f"Error retrieving old memory IDs for pruning: {e}")
        return None

# --- Graph Nodes ---

def retrieve_context(state: EnhancedMessageState) -> Dict[str, Any]:
    """Node to retrieve relevant context from long-term memory (vector store).
    Performs hybrid search with temporal and session filtering.
    """
    logger.info(f"Node: retrieve_context for session {state.session_id}")
    vector_store = get_vector_store()
    if not vector_store:
        logger.error("Cannot retrieve context: Vector store not available.")
        return {"long_term": []}
        
    last_message = state.short_term[-1]
    if not isinstance(last_message, HumanMessage):
        logger.warning("Last message is not HumanMessage, skipping context retrieval.")
        return {"long_term": []}

    query = last_message.content
    session_id = state.session_id
    # cutoff_timestamp = get_temporal_cutoff() # Temporarily disable temporal cutoff for broader retrieval

    try:
        # Filter by session_id. Temporal filter disabled for now.
        # Add timestamp filter back when memory saving includes timestamps.
        filter_criteria = {"session_id": {"$eq": session_id}}
        
        logger.debug(f"Retrieving context for query: '{query[:50]}...' with filter: {filter_criteria}")
        
        # Perform similarity search
        results: List[Document] = vector_store.similarity_search(
            query=query,
            k=MAX_LONG_TERM_MEMORIES_IN_STATE,
            filter=filter_criteria 
            # Filter syntax might vary slightly, e.g., using `where` in newer versions
            # filter={ 
            #     "$and": [
            #         {"session_id": {"$eq": session_id}},
            #         # {"timestamp": {"$gte": cutoff_timestamp}} # Re-enable later
            #     ]
            # }
        )
        
        retrieved_content = [doc.page_content for doc in results]
        logger.info(f"Retrieved {len(retrieved_content)} long-term memories.")
        return {"long_term": retrieved_content}
        
    except Exception as e:
        logger.exception(f"Error during context retrieval: {e}")
        return {"long_term": []} # Return empty list on error

def generate_verified_response(state: EnhancedMessageState) -> Dict[str, Any]:
    """Node to generate a response using the LLM.
    Includes a step to verify the relevance of retrieved long-term context.
    """
    logger.info(f"Node: generate_verified_response for session {state.session_id}")
    llm = get_llm_client()
    query = state.short_term[-1].content
    retrieved_context_str = "\n---\n".join(state.long_term)
    verified_context = retrieved_context_str # Default if verification fails or no context

    if state.long_term:
        try:
            # 1. Verify Context Step (Optional but recommended)
            verification_prompt = (
                f"You are a helpful assistant verifying context relevance."
                f"Given the User Query and the Retrieved Context, identify and return ONLY the parts of the context that are directly relevant to answering the query."
                f"If no part of the context is relevant, return 'No relevant context found.'."
                f"\n\nUser Query:\n{query}\n\nRetrieved Context:\n{retrieved_context_str}"
            )
            logger.debug("Invoking LLM for context verification.")
            verification_result = llm.invoke([HumanMessage(content=verification_prompt)])
            verified_context = verification_result.content
            if "No relevant context found." in verified_context:
                 logger.info("LLM verification found no relevant context.")
                 verified_context = "" # Use empty string if none found
            else:
                 logger.info("LLM verification successful, using verified context.")
        except Exception as e:
            logger.exception("Error during context verification step. Using unverified context.")
            verified_context = retrieved_context_str # Fallback to using all retrieved context
    else:
        logger.info("No long-term context retrieved, skipping verification.")
        verified_context = "" # No context to verify

    try:
        # 2. Generate Final Response
        system_prompt = "You are a helpful AI assistant. Answer the user's question based on the provided conversation history and relevant context." 
        if verified_context:
             system_prompt += "\n\nRelevant Context:\n" + verified_context

        # Construct message history for the final prompt
        # This assumes state.short_term contains the history up to the *last user message*
        messages_for_llm = [HumanMessage(content=system_prompt)] + state.short_term

        logger.debug(f"Invoking LLM for final response generation with {len(messages_for_llm)} messages.")
        response = llm.invoke(messages_for_llm)
        ai_response_content = response.content
        logger.info("LLM generation successful.")
        
    except Exception as e:
        logger.exception("Error during final response generation.")
        ai_response_content = "Sorry, I encountered an error trying to generate a response." 

    # Update the short-term memory with the latest AI response
    # LangGraph expects the *new* value for the state key
    updated_short_term = state.short_term + [AIMessage(content=ai_response_content)]
    
    # NOTE: This node *uses* long_term memory but doesn't modify it for the next state.
    # The long_term memory in the state dictionary represents the *retrieved* context for this turn.
    # If we wanted to *add* the generated response to long-term memory, that would be a different node/step.
    return {"short_term": updated_short_term}

def prune_memories(state: EnhancedMessageState) -> Dict:
    """Node to automatically prune old or irrelevant memories from the vector store.
    Triggered conditionally based on memory size (logic handled in graph edges).
    """
    logger.info(f"Node: prune_memories for session {state.session_id}")
    vector_store = get_vector_store()
    if not vector_store:
        logger.error("Cannot prune memories: Vector store not available.")
        return {}
        
    session_id = state.session_id
    memory_ids_to_prune = get_old_memories(session_id)

    if memory_ids_to_prune:
        try:
            logger.info(f"Pruning {len(memory_ids_to_prune)} memories for session {session_id}...")
            vector_store.delete(ids=memory_ids_to_prune)
            # Note: Deleting from Chroma requires IDs. Ensure get_old_memories returns correct IDs.
            # We might need to adjust filtering/retrieval in get_old_memories if it only returns docs.
            logger.info("Memory pruning successful.")
        except Exception as e:
            logger.exception(f"Error during memory pruning: {e}")
    else:
        logger.info("No memories met the criteria for pruning.")
        
    # This node modifies the external vector store, not the state dictionary directly
    # for the *next* node, so we return an empty dict.
    return {}

# --- Graph Construction & Compilation ---

_agent_executor = None # Singleton for the compiled graph

def should_prune_memory(state: EnhancedMessageState) -> Literal["prune", "end"]:
    """Conditional logic to decide whether to prune long-term memory."""
    # Note: This condition currently relies on the count of *retrieved* memories
    # in the current state turn, not the total size of the vector store for the session.
    # A more robust check might involve querying the vector store count directly,
    # but that adds latency. Using the state count is a simpler proxy.
    if len(state.long_term) >= MEMORY_PRUNING_THRESHOLD:
        logger.info(f"Memory pruning condition met (>= {MEMORY_PRUNING_THRESHOLD} retrieved memories). Routing to prune.")
        return "prune"
    else:
        logger.info("Memory pruning condition not met. Routing to end.")
        return "end"

def get_agent_executor():
    """Builds and compiles the stateful agent graph using LangGraph.
    
    Returns:
        Compiled LangGraph application, or None if compilation fails.
    """
    global _agent_executor
    if _agent_executor is not None:
        return _agent_executor
        
    logger.info("Building agent graph...")
    try:
        builder = StateGraph(EnhancedMessageState)

        # Add nodes
        builder.add_node("retrieve", retrieve_context)
        builder.add_node("generate", generate_verified_response)
        builder.add_node("prune", prune_memories)

        # Define edges
        builder.set_entry_point("retrieve")
        builder.add_edge("retrieve", "generate")
        
        # Conditional edge after generation: either prune or end
        builder.add_conditional_edges(
            "generate",
            should_prune_memory, # Function to decide the next node
            {
                "prune": "prune",  # If should_prune_memory returns "prune", go to prune node
                "end": END       # If should_prune_memory returns "end", finish the graph
            }
        )
        
        # After pruning, the graph ends
        builder.add_edge("prune", END)

        # Compile the graph
        logger.info("Compiling agent graph with checkpointer and interrupt...")
        _agent_executor = builder.compile(
            checkpointer=memory_checkpointer,
            interrupt_before=["prune"], # Allow interruption before pruning step
            debug=os.environ.get("FINGEN_LANGGRAPH_DEBUG", "False").lower() == "true"
        )
        logger.info("Agent graph compiled successfully.")
        return _agent_executor
        
    except Exception as e:
        logger.exception("Failed to build or compile agent graph!")
        return None

async def handle_agent_message(session_id: str, message: str) -> Generator[str, None, None]:
    """
    Placeholder for handling a message using the stateful agent.
    """
    logger.info(f"Handling agent message for session {session_id}: {message[:50]}...")
    app = get_agent_executor()
    if app is None:
         yield "Stateful agent functionality is not yet implemented (Graph not compiled)."
         return
         
    thread = {"configurable": {"thread_id": session_id}}
    # LangGraph loads state based on thread_id, we provide the input delta
    input_state = {"short_term": [HumanMessage(content=message)], "session_id": session_id}
    
    try:
        # Use astream_events for detailed streaming, or ainvoke for final result
        async for event in app.astream_events(input_state, thread, version="v2"):
            kind = event["event"]
            # Handle different event types (on_chat_model_stream, on_tool_end, etc.)
            # For now, just yield AIMessage chunks from the generation node
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield content
            # Add more event handling as needed (e.g., for tool calls, state changes)
            # logger.debug(f"Agent Event: {kind} | Data: {event['data']}")
            
    except Exception as e:
        logger.exception(f"Error invoking agent for session {session_id}")
        yield f"[Error processing agent request: {e}]" 