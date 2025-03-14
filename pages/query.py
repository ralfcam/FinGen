from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/query')

# Sample query templates
QUERY_TEMPLATES = [
    {"value": "revenue_analysis", "label": "Revenue Analysis", "description": "Analyze revenue trends and patterns"},
    {"value": "profit_margins", "label": "Profit Margins", "description": "Calculate and compare profit margins"},
    {"value": "cash_flow", "label": "Cash Flow Analysis", "description": "Review cash flow patterns and projections"},
    {"value": "market_comparison", "label": "Market Comparison", "description": "Compare performance against market benchmarks"},
    {"value": "risk_assessment", "label": "Risk Assessment", "description": "Evaluate financial risks and opportunities"}
]

# Define the page layout directly
layout = dmc.Container([
    # Header
    dmc.Group([
        html.Div([
            html.H1("Financial Analysis Query", className="mb-4"),
            html.P("Ask questions about your financial data in natural language", className="text-muted")
        ])
    ]),
    
    # Main Query Interface
    dmc.SimpleGrid(
        cols=4,
        spacing="md",
        children=[
            # Query Input Section
            dmc.Paper([
                dmc.Stack([
                    dmc.Title("Enter Your Query", order=5),
                    dmc.Textarea(
                        id="query-input",
                        placeholder="Example: Analyze revenue trends for the last quarter and compare with industry benchmarks",
                        minRows=3,
                    ),
                    dmc.Group([
                        dmc.Button(
                            "Analyze",
                            id="analyze-button",
                            leftSection=DashIconify(icon="radix-icons:magnifying-glass"),
                            color="blue",
                        ),
                        dmc.Button(
                            "Clear",
                            id="clear-button",
                            leftSection=DashIconify(icon="radix-icons:reset"),
                            color="gray",
                            variant="outline",
                        )
                    ], justify="flex-end", mt="md")
                ], gap="md")
            ], p="md", shadow="sm", radius="md", withBorder=True, className="span-3"),
            
            # Template Gallery
            dmc.Paper([
                dmc.Stack([
                    dmc.Title("Query Templates", order=5),
                    dmc.Select(
                        id="template-select",
                        data=QUERY_TEMPLATES,
                        placeholder="Select a template",
                    ),
                    html.Div(id="template-description-query", className="text-muted"),
                    dmc.Button(
                        "Use Template",
                        id="use-template-button",
                        leftSection=DashIconify(icon="radix-icons:copy"),
                        color="teal",
                        variant="light",
                        mt="md",
                        fullWidth=True
                    )
                ], gap="md")
            ], p="md", shadow="sm", radius="md", withBorder=True)
        ],
    ),
    
    # Query History
    dmc.Paper([
        dmc.Stack([
            dmc.Title("Recent Queries", order=5),
            dmc.List([
                dmc.ListItem(
                    dmc.Stack([
                        dmc.Group([
                            dmc.Text("Revenue Analysis", fw=700),
                            dmc.Text("2 hours ago", c="dimmed", size="xs")
                        ], justify="space-between"),
                        dmc.Text("Analyze revenue trends for Q4 2023", c="dimmed", size="sm")
                    ], gap="xs")
                ),
                dmc.ListItem(
                    dmc.Stack([
                        dmc.Group([
                            dmc.Text("Market Comparison", fw=700),
                            dmc.Text("5 hours ago", c="dimmed", size="xs")
                        ], justify="space-between"),
                        dmc.Text("Compare performance against industry benchmarks", c="dimmed", size="sm")
                    ], gap="xs")
                ),
                dmc.ListItem(
                    dmc.Stack([
                        dmc.Group([
                            dmc.Text("Risk Assessment", fw=700),
                            dmc.Text("1 day ago", c="dimmed", size="xs")
                        ], justify="space-between"),
                        dmc.Text("Evaluate financial risks in current market conditions", c="dimmed", size="sm")
                    ], gap="xs")
                )
            ])
        ], gap="md")
    ], p="md", shadow="sm", radius="md", withBorder=True, mt="xl")
], fluid=True, px="md", py="lg")

# Callback functions defined directly in the page file
@callback(
    Output("template-description-query", "children"),
    Input("template-select", "value")
)
def update_template_description(value):
    if value:
        template = next((t for t in QUERY_TEMPLATES if t["value"] == value), None)
        return template["description"] if template else ""
    return ""

@callback(
    Output("query-input", "value"),
    Input("use-template-button", "n_clicks"),
    State("template-select", "value")
)
def use_template(n_clicks, value):
    if n_clicks and value:
        template = next((t for t in QUERY_TEMPLATES if t["value"] == value), None)
        return f"Please {template['description'].lower()}" if template else ""
    return "" 