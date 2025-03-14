"""
Main entry point for the FinGen application.
Initializes the Dash application and registers callbacks.
"""

from dash import Dash, html, dcc
import dash
from dash_iconify import DashIconify
from dash_mantine_components import MantineProvider, NavLink, Stack, Container, Paper

# Initialize the Dash app with support for pages
app = Dash(
    __name__,
    use_pages=True,  # Enable Dash Pages
    suppress_callback_exceptions=True
)

# Import pages AFTER app instantiation
# This is important because dash.register_page must be called after app is created
import pages.home
import pages.query
import pages.analysis
import pages.visualizations
import pages.reports

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
    app.run_server(debug=True)