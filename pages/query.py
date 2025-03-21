from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/query')

# Sample query templates
QUERY_TEMPLATES = [
    {"value": "revenue_analysis", "label": "Revenue Analysis", "description": "Analyze revenue trends and patterns", "icon": "carbon:chart-line"},
    {"value": "profit_margins", "label": "Profit Margins", "description": "Calculate and compare profit margins", "icon": "carbon:percentage"},
    {"value": "cash_flow", "label": "Cash Flow Analysis", "description": "Review cash flow patterns and projections", "icon": "carbon:flow"},
    {"value": "market_comparison", "label": "Market Comparison", "description": "Compare performance against market benchmarks", "icon": "carbon:comparison"},
    {"value": "risk_assessment", "label": "Risk Assessment", "description": "Evaluate financial risks and opportunities", "icon": "carbon:warning-alt"}
]

# Recent queries - sample data
RECENT_QUERIES = [
    {"text": "Analyze revenue trends for Q4 2023", "timestamp": "2 hours ago", "type": "Revenue Analysis", "icon": "carbon:chart-line"},
    {"text": "Compare performance against industry benchmarks", "timestamp": "5 hours ago", "type": "Market Comparison", "icon": "carbon:comparison"},
    {"text": "Evaluate financial risks in current market conditions", "timestamp": "1 day ago", "type": "Risk Assessment", "icon": "carbon:warning-alt"},
]

# Define the page layout
layout = dmc.Container([
    # Header with title and description
    dmc.Stack([
        dmc.Title("Financial Query Interface", order=1, c="#0A3D62", style={"fontSize": "28px"}),
        dmc.Text("Ask natural language questions about your financial data", c="#333F48", size="md"),
    ], gap="xs", mb="md"),
    
    # Main Query Interface 
    dmc.Paper([
        dmc.Group([
            DashIconify(icon="carbon:chat", width=24, color="#0A3D62"),
            dmc.Title("Ask a Financial Question", order=5, c="#333F48")
        ], gap="xs", mb="md"),
        
        # Query Input with Context Panel
        dmc.SimpleGrid([
            # Query Input
            dmc.Stack([
                dcc.Input(
                    id="query-input",
                    type="text",
                    placeholder="Example: What was our revenue growth year-over-year?",
                    style={
                        "width": "100%", 
                        "padding": "12px 16px",
                        "borderRadius": "8px",
                        "border": "1px solid #ced4da",
                        "fontSize": "16px"
                    }
                ),
                
                # Analysis Controls
                dmc.Group([
                    dmc.Button(
                        "Process Query", 
                        id="process-query",
                        leftSection=DashIconify(icon="carbon:play"),
                        color="#0A3D62",
                        radius="md"
                    ),
                    dmc.Button(
                        "Save Query", 
                        id="save-query",
                        leftSection=DashIconify(icon="carbon:bookmark"),
                        color="#0A3D62",
                        variant="outline",
                        radius="md"
                    ),
                    dmc.Button(
                        "Clear", 
                        id="clear-query",
                        leftSection=DashIconify(icon="carbon:close"),
                        color="gray",
                        variant="subtle",
                        radius="md"
                    )
                ], justify="flex-end", mt="md")
            ], style={"gridColumn": "span 8"}),
            
            # Context Panel
            dmc.Paper([
                dmc.Text("Active Parameters", fw=500, size="sm", c="#333F48", mb="xs"),
                dmc.Stack([
                    dmc.Group([
                        dmc.Badge("Time Period: 2023", color="blue", variant="light"),
                        dmc.Badge("Division: All", color="teal", variant="light"),
                    ], gap="xs"),
                    dmc.Group([
                        dmc.Badge("Currency: USD", color="violet", variant="light"),
                        dmc.Badge("Comparison: YoY", color="indigo", variant="light"),
                    ], gap="xs")
                ], gap="xs")
            ], p="md", withBorder=True, style={"backgroundColor": "#f8fafc", "gridColumn": "span 4"})
        ], cols=12, spacing="lg")
    ], p="lg", shadow="sm", radius="md", withBorder=True, mb="lg"),
    
    # Recent Queries and Templates
    dmc.SimpleGrid([
        # Recent Queries
        dmc.Paper([
            dmc.Group([
                dmc.Group([
                    DashIconify(icon="carbon:recently-viewed", width=20, color="#0A3D62"),
                    dmc.Title("Recent Queries", order=5, c="#333F48")
                ], gap="xs"),
                dmc.Badge(f"{len(RECENT_QUERIES)} Queries", color="blue", variant="light")
            ], justify="space-between", mb="md"),
            
            dmc.Stack([
                dmc.Paper([
                    dmc.Group([
                        DashIconify(
                            icon=query["icon"], 
                            width=18, 
                            color="#0A3D62"
                        ),
                        dmc.Stack([
                            dmc.Text(query["text"], fw=500, size="sm"),
                            dmc.Text(query["timestamp"], size="xs", c="dimmed")
                        ], gap=0)
                    ], gap="xs")
                ], p="sm", withBorder=True, mb="xs") for query in RECENT_QUERIES
            ], gap="xs")
        ], p="lg", shadow="sm", radius="md", withBorder=True, mb="lg", style={"gridColumn": "span 6"}),
        
        # Template Gallery
        dmc.Paper([
            dmc.Group([
                dmc.Group([
                    DashIconify(icon="carbon:template", width=20, color="#0A3D62"),
                    dmc.Title("Query Templates", order=5, c="#333F48")
                ], gap="xs"),
                dmc.Badge("Financial Analysis", color="blue", variant="light")
            ], justify="space-between", mb="md"),
            
            dmc.SimpleGrid(
                cols=2,
                children=[
                    dmc.Paper([
                        dmc.Group([
                            DashIconify(icon=template["icon"], width=24, color="#0A3D62"),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:add-alt", width=16),
                                size="sm",
                                variant="subtle",
                                color="blue"
                            )
                        ], justify="space-between"),
                        dmc.Text(template["label"], fw=500, size="sm", mt="xs"),
                        dmc.Text(template["description"], size="xs", c="dimmed", mt=4)
                    ], p="sm", withBorder=True) for template in QUERY_TEMPLATES
                ],
                spacing="md"
            )
        ], p="lg", shadow="sm", radius="md", withBorder=True, mb="lg", style={"gridColumn": "span 6"})
    ]),
    
    # Query Assistant (Help Panel)
    dmc.Paper([
        dmc.Group([
            DashIconify(icon="carbon:idea", width=24, color="#0A3D62"),
            dmc.Title("Query Assistant", order=5, c="#333F48")
        ], gap="xs", mb="md"),
        
        dmc.Text("Tips for better financial queries:", fw=500, size="sm", mb="xs"),
        dmc.List([
            dmc.ListItem(
                dmc.Text("Be specific about time periods: 'Q1 2023', 'last 6 months'", size="sm")
            ),
            dmc.ListItem(
                dmc.Text("Specify metrics clearly: 'revenue', 'profit margin', 'cash flow'", size="sm")
            ),
            dmc.ListItem(
                dmc.Text("Ask for comparisons: 'compared to previous year', 'vs industry average'", size="sm")
            ),
            dmc.ListItem(
                dmc.Text("Request specific visualizations: 'show as line chart', 'create heatmap'", size="sm")
            )
        ])
    ], p="lg", shadow="sm", radius="md", withBorder=True)
], fluid=True, px="md", py="lg", style={"backgroundColor": "#f8f9fa"})

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
    [Input(f"use-template-{template['value']}", "n_clicks") for template in QUERY_TEMPLATES],
    prevent_initial_call=True,
)
def use_template(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    template_value = trigger_id.replace("use-template-", "")
    template = next((t for t in QUERY_TEMPLATES if t["value"] == template_value), None)
    
    if template:
        return f"Please {template['description'].lower()}"
    return "" 