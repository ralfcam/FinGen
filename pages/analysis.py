from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/analysis')

# Sample data for demonstration
def create_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    data = {
        'revenue': np.random.normal(1000, 100, len(dates)),
        'expenses': np.random.normal(800, 80, len(dates)),
        'profit': np.random.normal(200, 20, len(dates)),
        'market_index': np.random.normal(100, 10, len(dates))
    }
    return pd.DataFrame(data, index=dates)

# Create sample insights
def create_sample_insights():
    return [
        {
            "title": "Revenue Growth",
            "description": "Revenue has shown consistent growth of 12% YoY",
            "impact": "positive",
            "confidence": "high"
        },
        {
            "title": "Expense Management",
            "description": "Operating expenses are 5% below budget",
            "impact": "positive",
            "confidence": "medium"
        },
        {
            "title": "Market Position",
            "description": "Market share has increased by 2% in Q4",
            "impact": "positive",
            "confidence": "high"
        },
        {
            "title": "Risk Factors",
            "description": "Supply chain costs are trending upward",
            "impact": "negative",
            "confidence": "medium"
        }
    ]

# Prepare data and charts for the layout
insights = create_sample_insights()
df = create_sample_data()

# Create sample charts
revenue_chart = px.line(df, y='revenue', title='Revenue Trend')
revenue_chart.update_layout(height=300, template='plotly_white')

profit_margin_chart = go.Figure()
profit_margin_chart.add_trace(go.Scatter(
    x=df.index,
    y=df['profit'] / df['revenue'] * 100,
    name='Profit Margin %',
    line=dict(color='#2ecc71')
))
profit_margin_chart.update_layout(
    title='Profit Margin Trend',
    yaxis_title='Margin %',
    height=300,
    template='plotly_white'
)

# Define the page layout directly
layout = dmc.Container([
    # Header
    dmc.Grid([
        dmc.GridCol([
            html.H1("Analysis Results", className="mb-4"),
            html.P("Key insights and visualizations from your financial data", className="text-muted")
        ], span=12)
    ]),
    
    # Key Insights
    dmc.Grid([
        dmc.GridCol([
            html.H5("Key Insights", className="mb-3"),
            dmc.Grid([
                dmc.GridCol([
                    dmc.Card([
                        html.H6(insight["title"], className="card-title"),
                        html.P(insight["description"], className="card-text"),
                        html.Div([
                            html.Span(
                                "Impact: ",
                                className="text-muted"
                            ),
                            html.Span(
                                insight["impact"].title(),
                                className=f"text-{'success' if insight['impact'] == 'positive' else 'danger'}"
                            ),
                            html.Span(
                                " | Confidence: ",
                                className="text-muted"
                            ),
                            html.Span(
                                insight["confidence"].title(),
                                className="text-info"
                            )
                        ], className="mt-2")
                    ], className="mb-3", p="md")
                ], span=6) for insight in insights
            ])
        ], span=12)
    ], className="mb-4"),
    
    # Charts
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Revenue Analysis", className="card-title"),
                dcc.Graph(figure=revenue_chart, id="revenue-chart")
            ], p="md")
        ], span=8),
        dmc.GridCol([
            dmc.Card([
                html.H5("Profit Margins", className="card-title"),
                dcc.Graph(figure=profit_margin_chart)
            ], p="md")
        ], span=4)
    ], className="mb-4"),
    
    # Data Sources and Parameters
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Analysis Parameters", className="card-title"),
                html.Div([
                    html.Div([
                        html.Strong("Time Period: "),
                        "Jan 2023 - Dec 2023"
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Data Sources: "),
                        "Internal Financial Records, Market Data API"
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Analysis Type: "),
                        "Trend Analysis, Comparative Analysis"
                    ])
                ])
            ], p="md")
        ], span=6),
        dmc.GridCol([
            dmc.Card([
                html.H5("Actions", className="card-title"),
                dmc.ButtonGroup([
                    dmc.Button([
                        DashIconify(icon="radix-icons:download"),
                        " Export Data"
                    ], color="primary", className="me-2", id="export-button"),
                    dmc.Button([
                        DashIconify(icon="radix-icons:share-1"),
                        " Share Analysis"
                    ], color="secondary", className="me-2", id="share-button"),
                    dmc.Button([
                        DashIconify(icon="radix-icons:refresh"),
                        " Refresh"
                    ], color="info", id="refresh-button")
                ])
            ], p="md")
        ], span=6)
    ])
], fluid=True, className="py-4")

# Callback functions defined directly in the page file
@callback(
    Output("revenue-chart", "figure"),
    Input("refresh-button", "n_clicks")
)
def refresh_charts(n_clicks):
    if n_clicks:
        df = create_sample_data()
        fig = px.line(df, y='revenue', title='Revenue Trend')
        fig.update_layout(height=300, template='plotly_white')
        return fig
    return revenue_chart 