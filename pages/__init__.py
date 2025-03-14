"""
Pages package for the FinGen application.
Contains all the different pages and their associated callbacks.
All pages use dash_mantine_components (DMC) for UI components.
Each page registers itself with dash.register_page(__name__, path='...').
Each page defines a 'layout' variable and its callbacks.
Follows the multi-page app pattern using Dash Pages feature.
"""

# No imports needed here as pages register themselves
# and are automatically discovered by Dash Pages when using use_pages=True 