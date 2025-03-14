"""
Utility functions for the FinGen application.
Contains helper functions used across different pages.
"""

def format_currency(value):
    """Format a number as currency."""
    try:
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_percentage(value):
    """Format a number as percentage."""
    try:
        return f"{value:.2f}%"
    except (ValueError, TypeError):
        return "0.00%" 