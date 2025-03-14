"""
Callback handlers for the FinGen application.
Contains all Dash callback functions for handling user interactions.
Uses dash_mantine_components for UI elements.
"""

from dash import Input, Output, State
from dash.exceptions import PreventUpdate

def register_callbacks(app):
    """Register all callbacks for the application."""
    
    @app.callback(
        Output('output-container', 'children'),
        Input('submit-button', 'n_clicks'),
        State('input-field', 'value')
    )
    def update_output(n_clicks, value):
        """Example callback function."""
        if n_clicks is None:
            raise PreventUpdate
        return f"Processed value: {value}" 