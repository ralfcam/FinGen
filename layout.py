"""
Main layout components for the FinGen application.
Defines the overall structure and appearance of the application using Mantine components.
"""

from dash import html
from dash_mantine_components import Container, Stack, Text, TextInput, Button, Paper

def create_layout():
    """Create and return the main application layout."""
    return Container([
        Stack([
            Text("FinGen", size="xl", weight=700, align="center", mb="md"),
            Paper([
                Text("Financial Data Visualization", size="lg", align="center", mb="md"),
                TextInput(
                    id="input-field",
                    placeholder="Enter value...",
                    size="md",
                    mb="md"
                ),
                Button(
                    "Submit",
                    id="submit-button",
                    variant="filled",
                    color="blue",
                    size="md"
                )
            ], p="md", radius="md", withBorder=True),
            html.Div(id="output-container")
        ], spacing="md")
    ], size="md", py="xl") 