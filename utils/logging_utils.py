"""
Logging utilities for the FinGen application.
Provides configuration for logging and error handling.
"""

import traceback
import logging
import json
import os
import sys
from datetime import datetime
from dash import callback_context

def setup_logger(log_name='fingen_front', log_dir=None):
    """
    Configure and return a logger instance for the application.
    
    Args:
        log_name (str): Base name for the log file
        log_dir (str): Directory to store log files, defaults to 'logs' in the project root
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Determine log directory
    if log_dir is None:
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(project_root, 'logs')
    
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Setup log file path
    log_file = os.path.join(log_dir, f'{log_name}.log')
    
    # Create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Try to add file handler, but don't fail if there's a permission error
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, IOError) as e:
        console_handler.setLevel(logging.WARNING)
        logger.warning(f"Could not create log file at {log_file}: {str(e)}")
        logger.warning("Logging to console only")
    
    return logger

def create_error_handler(logger):
    """
    Create and return a global error handler function for Dash callbacks.
    
    Args:
        logger (logging.Logger): Logger instance to use for error logging
        
    Returns:
        function: Error handler function to use with Dash's on_error parameter
    """
    def global_error_handler(err):
        # Get callback context information if available
        try:
            trigger_info = json.dumps(callback_context.triggered)
            input_values = json.dumps(callback_context.inputs)
            context_info = f"Triggered by: {trigger_info}\nInput values: {input_values}"
        except:
            context_info = "No context information available"
        
        # Log detailed error information
        error_details = traceback.format_exc()
        logger.error(
            f"Callback Error: {str(err)}\n"
            f"Timestamp: {datetime.now().isoformat()}\n"
            f"Error Type: {type(err).__name__}\n"
            f"{context_info}\n"
            f"Traceback: {error_details}"
        )
        
        # Return user-friendly message
        return "An error occurred processing your request. The development team has been notified."
    
    return global_error_handler 