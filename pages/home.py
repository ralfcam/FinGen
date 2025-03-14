from dash import html, dcc, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import dash
import pandas as pd
import numpy as np

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/')

# Sample data for demonstration
def create_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    data = {
        'revenue': np.random.normal(1000, 100, len(dates)),
        'expenses': np.random.normal(800, 80, len(dates)),
        'profit': np.random.normal(200, 20, len(dates))
    }
    return pd.DataFrame(data, index=dates)

# Create sample financial metrics
def create_metrics():
    return {
        'revenue': {'value': '$1.2M', 'change': '+12%', 'trend': 'up'},
        'profit': {'value': '$240K', 'change': '+8%', 'trend': 'up'},
        'margins': {'value': '20%', 'change': '+2%', 'trend': 'up'},
        'cash_flow': {'value': '$180K', 'change': '-5%', 'trend': 'down'}
    }

# Create sample chart
def create_sample_chart():
    df = create_sample_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Revenue',
        line=dict(color='#2ecc71')
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['expenses'],
        name='Expenses',
        line=dict(color='#e74c3c')
    ))
    fig.update_layout(
        title='Revenue vs Expenses',
        template='plotly_white',
        height=300
    )
    return fig

# Define the page layout directly
layout = dmc.Container([
    # Header
    dmc.Group([
        html.Div([
            html.H1("Financial Dashboard", className="mb-4"),
            html.P("Overview of your financial performance", className="text-muted")
        ])
    ]),
    
    # Key Metrics Cards
    dmc.SimpleGrid(
        cols=4,
        spacing="md",
        children=[
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("Revenue", fw=500, size="sm"),
                    dmc.Title(create_metrics()['revenue']['value'], order=3),
                    dmc.Group([
                        DashIconify(icon="radix-icons:arrow-up" if create_metrics()['revenue']['trend'] == 'up' else "radix-icons:arrow-down"),
                        dmc.Text(create_metrics()['revenue']['change'], c="green" if create_metrics()['revenue']['trend'] == 'up' else "red")
                    ])
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("Profit", fw=500, size="sm"),
                    dmc.Title(create_metrics()['profit']['value'], order=3),
                    dmc.Group([
                        DashIconify(icon="radix-icons:arrow-up" if create_metrics()['profit']['trend'] == 'up' else "radix-icons:arrow-down"),
                        dmc.Text(create_metrics()['profit']['change'], c="green" if create_metrics()['profit']['trend'] == 'up' else "red")
                    ])
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("Margins", fw=500, size="sm"),
                    dmc.Title(create_metrics()['margins']['value'], order=3),
                    dmc.Group([
                        DashIconify(icon="radix-icons:arrow-up" if create_metrics()['margins']['trend'] == 'up' else "radix-icons:arrow-down"),
                        dmc.Text(create_metrics()['margins']['change'], c="green" if create_metrics()['margins']['trend'] == 'up' else "red")
                    ])
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("Cash Flow", fw=500, size="sm"),
                    dmc.Title(create_metrics()['cash_flow']['value'], order=3),
                    dmc.Group([
                        DashIconify(icon="radix-icons:arrow-up" if create_metrics()['cash_flow']['trend'] == 'up' else "radix-icons:arrow-down"),
                        dmc.Text(create_metrics()['cash_flow']['change'], c="green" if create_metrics()['cash_flow']['trend'] == 'up' else "red")
                    ])
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True)
        ],
        className="mb-4"
    ),
    
    # Charts Row
    dmc.SimpleGrid(
        cols=3,
        spacing="md",
        children=[
            dmc.Paper([
                dmc.Stack([
                    dmc.Title("Revenue vs Expenses", order=5),
                    dcc.Graph(figure=create_sample_chart())
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, className="span-2"),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Title("Recent Analyses", order=5),
                    dmc.List([
                        dmc.ListItem("Q4 Financial Performance Review"),
                        dmc.ListItem("Market Trend Analysis"),
                        dmc.ListItem("Competitor Benchmarking")
                    ])
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True)
        ],
        mb="md"
    ),
    
    # Quick Actions
    dmc.Group(
        justify="space-between",
        mt="md",
        children=[
            dmc.Title("Quick Actions", order=5),
            dmc.Group([
                dmc.Button(
                    "Generate Report",
                    leftSection=DashIconify(icon="radix-icons:file-text"),
                    color="blue",
                ),
                dmc.Button(
                    "New Analysis",
                    leftSection=DashIconify(icon="radix-icons:chart-bar"),
                    color="gray",
                    variant="outline"
                ),
                dmc.Button(
                    "Set Alerts",
                    leftSection=DashIconify(icon="radix-icons:bell"),
                    color="teal",
                    variant="light"
                )
            ]),
        ]
    )
], fluid=True, px="md", py="lg") 