"""
Core callback implementations for the FinGen application.
Contains the main business logic for processing user inputs and generating outputs.
"""

def process_input(value):
    """
    Process user input and return appropriate response.
    
    Args:
        value: The input value to process
        
    Returns:
        Processed result
    """
    if not value:
        return "Please enter a value"
    return f"Processed: {value}" 