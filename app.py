"""
Main entry point for the FinGen application.
Initializes the Dash application and registers callbacks.
"""

from dash import Dash, html, dcc, _dash_renderer
import dash
from dash_iconify import DashIconify
from dash_mantine_components import MantineProvider, NavLink, Stack, Container, Paper
from utils.logging_utils import setup_logger, create_error_handler
import os
import tempfile

# Use a specific React version that's compatible with dash-mantine-components
_dash_renderer._set_react_version("18.2.0")

# Setup application logger with a unique log name from environment variable
# If environment variable is not set, use a unique temporary file to avoid permission issues
log_name = os.environ.get('FINGEN_LOG_NAME', None)
if log_name is None:
    # Generate a unique log name with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    log_name = f"fingen_{timestamp}"

# Ensure the logs directory exists with proper permissions
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)
try:
    # Test if we can write to the logs directory
    test_file = os.path.join(logs_dir, '.write_test')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    logger = setup_logger(log_name=log_name, log_dir=logs_dir)
except (PermissionError, IOError):
    # If we can't write to the logs directory, use a temporary directory
    temp_dir = tempfile.gettempdir()
    logger = setup_logger(log_name=log_name, log_dir=temp_dir)
    logger.warning(f"Using temporary directory for logs: {temp_dir}")

# Initialize the Dash app with support for pages
app = Dash(
    __name__,
    use_pages=True,  # Enable Dash Pages
    suppress_callback_exceptions=True,
    on_error=create_error_handler(logger),  # Add global error handler
)

# Import pages AFTER app instantiation
# This is important because dash.register_page must be called after app is created
import pages.home
import pages.query
import pages.analysis
import pages.visualizations
import pages.reports
import pages.chat  # Added import for chat page

# Define the main layout
app.layout = MantineProvider(
    theme={
        "colorScheme": "light",
        "primaryColor": "blue",
        "fontFamily": "'Inter', sans-serif",
    },
    children=[
        html.Div([
            # Location component for URL routing
            dcc.Location(id='url', refresh=False),
            
            # Sidebar navigation using Paper component
            Paper(
                p="md",
                shadow="sm",
                withBorder=True,
                style={"width": "250px", "height": "100vh", "position": "fixed", "left": 0, "top": 0},
                className="sidebar-nav",
                children=Stack([
                    NavLink(
                        label="Dashboard",
                        leftSection=DashIconify(icon="radix-icons:dashboard"),
                        href="/",
                        active=True,
                        className="nav-link"
                    ),
                    NavLink(
                        label="Query",
                        leftSection=DashIconify(icon="radix-icons:magnifying-glass"),
                        href="/query",
                        className="nav-link"
                    ),
                    NavLink(
                        label="Analysis",
                        leftSection=DashIconify(icon="radix-icons:chart-bar"),
                        href="/analysis",
                        className="nav-link"
                    ),
                    NavLink(
                        label="Visualizations",
                        leftSection=DashIconify(icon="radix-icons:pie-chart"),
                        href="/visualizations",
                        className="nav-link"
                    ),
                    NavLink(
                        label="Reports",
                        leftSection=DashIconify(icon="radix-icons:file-text"),
                        href="/reports",
                        className="nav-link"
                    ),
                    NavLink(
                        label="Chat",
                        leftSection=DashIconify(icon="radix-icons:chat-bubble"),
                        href="/chat",
                        className="nav-link"
                    ),
                ], gap="md")
            ),
            # Main content - use dash.page_container instead of custom callback
            Container(
                dash.page_container,
                className="page-content",
                fluid=True,
                p="md",
                style={"marginLeft": "250px"}
            )
        ], className="app-container")
    ]
)

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode to see more detailed error messages