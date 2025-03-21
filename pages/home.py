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

# Create sample revenue vs expenses chart
def create_revenue_chart():
    df = create_sample_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Revenue',
        line=dict(color='#147D64')  # Muted green from design doc
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['expenses'],
        name='Expenses',
        line=dict(color='#BF2600')  # Muted red from design doc
    ))
    fig.update_layout(
        title=None,
        template='plotly_white',
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# Create sample profit margin chart
def create_profit_chart():
    df = create_sample_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['profit'],
        name='Profit',
        line=dict(color='#0A3D62'),  # Deep blue from design doc
        fill='tozeroy',
        fillcolor='rgba(10, 61, 98, 0.1)'
    ))
    fig.update_layout(
        title=None,
        template='plotly_white',
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# Define the page layout directly
layout = dmc.Container([
    # Header with welcome and overview
    dmc.Stack([
        dmc.Title("Financial Dashboard", order=1, c="#0A3D62", style={"fontSize": "28px"}),
        dmc.Text("Overview of your financial performance and key insights", c="#333F48", size="md"),
    ], gap="xs", mb="md"),
    
    # Key Metrics Cards - following financial data visualization best practices
    dmc.SimpleGrid(
        cols=4,
        spacing="md",
        children=[
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("REVENUE", fw=500, size="xs", c="#333F48"),
                    dmc.Title(create_metrics()['revenue']['value'], order=3, c="#0A3D62"),
                    dmc.Group([
                        DashIconify(
                            icon="carbon:growth" if create_metrics()['revenue']['trend'] == 'up' else "carbon:decrease",
                            color="#147D64" if create_metrics()['revenue']['trend'] == 'up' else "#BF2600",
                            width=18
                        ),
                        dmc.Text(
                            create_metrics()['revenue']['change'], 
                            c="#147D64" if create_metrics()['revenue']['trend'] == 'up' else "#BF2600",
                            fw=500
                        )
                    ], gap="xs")
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, style={"borderTop": "4px solid #0A3D62"}),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("PROFIT", fw=500, size="xs", c="#333F48"),
                    dmc.Title(create_metrics()['profit']['value'], order=3, c="#0A3D62"),
                    dmc.Group([
                        DashIconify(
                            icon="carbon:growth" if create_metrics()['profit']['trend'] == 'up' else "carbon:decrease",
                            color="#147D64" if create_metrics()['profit']['trend'] == 'up' else "#BF2600",
                            width=18
                        ),
                        dmc.Text(
                            create_metrics()['profit']['change'], 
                            c="#147D64" if create_metrics()['profit']['trend'] == 'up' else "#BF2600",
                            fw=500
                        )
                    ], gap="xs")
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, style={"borderTop": "4px solid #0A3D62"}),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("MARGINS", fw=500, size="xs", c="#333F48"),
                    dmc.Title(create_metrics()['margins']['value'], order=3, c="#0A3D62"),
                    dmc.Group([
                        DashIconify(
                            icon="carbon:growth" if create_metrics()['margins']['trend'] == 'up' else "carbon:decrease",
                            color="#147D64" if create_metrics()['margins']['trend'] == 'up' else "#BF2600",
                            width=18
                        ),
                        dmc.Text(
                            create_metrics()['margins']['change'], 
                            c="#147D64" if create_metrics()['margins']['trend'] == 'up' else "#BF2600",
                            fw=500
                        )
                    ], gap="xs")
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, style={"borderTop": "4px solid #0A3D62"}),
            
            dmc.Paper([
                dmc.Stack([
                    dmc.Text("CASH FLOW", fw=500, size="xs", c="#333F48"),
                    dmc.Title(create_metrics()['cash_flow']['value'], order=3, c="#0A3D62"),
                    dmc.Group([
                        DashIconify(
                            icon="carbon:growth" if create_metrics()['cash_flow']['trend'] == 'up' else "carbon:decrease",
                            color="#147D64" if create_metrics()['cash_flow']['trend'] == 'up' else "#BF2600",
                            width=18
                        ),
                        dmc.Text(
                            create_metrics()['cash_flow']['change'], 
                            c="#147D64" if create_metrics()['cash_flow']['trend'] == 'up' else "#BF2600",
                            fw=500
                        )
                    ], gap="xs")
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, style={"borderTop": "4px solid #0A3D62"})
        ],
        mb="xl"
    ),
    
    # Charts Row - following financial data visualization best practices
    dmc.SimpleGrid(
        cols=12,
        spacing="md",
        children=[
            dmc.Paper([
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Revenue vs Expenses", order=5, c="#333F48"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="subtle",
                            size="md"
                        )
                    ], justify="space-between"),
                    dcc.Graph(figure=create_revenue_chart(), config={'displayModeBar': False})
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, style={"gridColumn": "span 8"}),
            
            dmc.Stack([
                dmc.Paper([
                    dmc.Stack([
                        dmc.Group([
                            dmc.Title("Profit Trend", order=5, c="#333F48"),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="subtle",
                                size="md"
                            )
                        ], justify="space-between"),
                        dcc.Graph(figure=create_profit_chart(), config={'displayModeBar': False})
                    ], gap="xs")
                ], p="md", shadow="sm", radius="md", withBorder=True, mb="md"),
                
                dmc.Paper([
                    dmc.Stack([
                        dmc.Group([
                            dmc.Title("Recent Analyses", order=5, c="#333F48"),
                            dmc.Badge("3 New", color="blue", variant="light", size="sm")
                        ], justify="space-between"),
                        dmc.List([
                            dmc.ListItem(
                                dmc.Group([
                                    DashIconify(icon="carbon:document", width=16, color="#0A3D62"),
                                    dmc.Text("Q4 Financial Performance", size="sm")
                                ], gap="xs")
                            ),
                            dmc.ListItem(
                                dmc.Group([
                                    DashIconify(icon="carbon:chart-line", width=16, color="#0A3D62"),
                                    dmc.Text("Market Trend Analysis", size="sm")
                                ], gap="xs")
                            ),
                            dmc.ListItem(
                                dmc.Group([
                                    DashIconify(icon="carbon:comparison", width=16, color="#0A3D62"),
                                    dmc.Text("Competitor Benchmarking", size="sm")
                                ], gap="xs")
                            )
                        ])
                    ], gap="xs")
                ], p="md", shadow="sm", radius="md", withBorder=True)
            ], style={"gridColumn": "span 4"})
        ],
        mb="md"
    ),
    
    # Quick Actions - prominent, accessible controls
    dmc.Paper([
        dmc.Group(
            justify="space-between",
            align="center",
            children=[
                dmc.Group([
                    DashIconify(icon="carbon:lightning", width=24, color="#0A3D62"),
                    dmc.Title("Quick Actions", order=5, c="#333F48")
                ], gap="xs"),
                dmc.Group([
                    dmc.Button(
                        "Generate Report",
                        leftSection=DashIconify(icon="carbon:document"),
                        color="#0A3D62",
                        radius="md",
                    ),
                    dmc.Button(
                        "New Analysis",
                        leftSection=DashIconify(icon="carbon:analytics"),
                        color="#0A3D62",
                        variant="outline",
                        radius="md",
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:notification", width=20),
                        color="#0A3D62",
                        variant="subtle",
                        size="lg"
                    )
                ], gap="md"),
            ]
        )
    ], p="md", shadow="sm", radius="md", withBorder=True)
], fluid=True, px="md", py="lg", style={"backgroundColor": "#f8f9fa"}) 