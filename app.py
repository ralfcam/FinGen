"""
Main entry point for the FinGen application.
Initializes the Dash application and registers callbacks.
"""

import dash
from dash_mantine_components import MantineProvider

from layout import create_layout
from pages.callbacks import register_callbacks

# Initialize the Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True
)

# Set the app layout with Mantine theme
app.layout = MantineProvider(
    theme={
        "colorScheme": "light",
        "primaryColor": "blue",
        "fontFamily": "Inter, sans-serif"
    },
    children=create_layout()
)

# Register all callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True) 