from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
import networkx as nx

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/visualizations')

# Sample data for demonstration
def create_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    data = {
        'revenue': np.random.normal(1000, 100, len(dates)),
        'expenses': np.random.normal(800, 80, len(dates)),
        'profit': np.random.normal(200, 20, len(dates)),
        'market_index': np.random.normal(100, 10, len(dates)),
        'competitor_a': np.random.normal(900, 90, len(dates)),
        'competitor_b': np.random.normal(1100, 110, len(dates))
    }
    return pd.DataFrame(data, index=dates)

# Create sample data
df = create_sample_data()

# Time series analysis with financial visualization best practices
def create_time_series_chart():
    time_series_fig = go.Figure()
    time_series_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Revenue',
        line=dict(color='#147D64')  # muted green from design doc
    ))
    time_series_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['expenses'],
        name='Expenses',
        line=dict(color='#BF2600')  # muted red from design doc
    ))
    time_series_fig.update_layout(
        title=None,
        height=420,
        template='plotly_white',
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=None,
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title='Amount ($)',
            gridcolor='#E0E0E0',
            tickprefix='$'
        )
    )
    return time_series_fig

# Comparative analysis
def create_comparative_chart():
    comparative_fig = go.Figure()
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Our Revenue',
        line=dict(color='#147D64')
    ))
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['competitor_a'],
        name='Competitor A',
        line=dict(color='#0A3D62')
    ))
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['competitor_b'],
        name='Competitor B',
        line=dict(color='#FF8800')
    ))
    comparative_fig.update_layout(
        title=None,
        height=420,
        template='plotly_white',
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=None,
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title='Amount ($)',
            gridcolor='#E0E0E0',
            tickprefix='$'
        )
    )
    return comparative_fig

# Risk assessment heat map
def create_risk_heatmap():
    # More realistic risk data for finance
    categories = ['Market', 'Credit', 'Operational', 'Liquidity', 'Regulatory']
    impact_levels = ['Critical', 'High', 'Medium', 'Low', 'Minimal']
    
    # Example risk data (higher value = higher risk)
    risk_data = [
        [0.9, 0.7, 0.6, 0.4, 0.8],  # Critical impact
        [0.8, 0.6, 0.5, 0.3, 0.7],  # High impact
        [0.6, 0.4, 0.5, 0.2, 0.5],  # Medium impact
        [0.3, 0.2, 0.3, 0.1, 0.4],  # Low impact
        [0.1, 0.1, 0.2, 0.1, 0.2],  # Minimal impact
    ]
    
    risk_fig = go.Figure(data=go.Heatmap(
        z=risk_data,
        x=categories,
        y=impact_levels,
        colorscale=[
            [0, '#147D64'],    # Low risk (muted green)
            [0.5, '#FFB703'],  # Medium risk (amber)
            [1, '#BF2600']     # High risk (muted red)
        ],
        showscale=True,
        colorbar=dict(
            title="Risk Level",
            tickmode='array',
            tickvals=[0.1, 0.5, 0.9],
            ticktext=['Low', 'Medium', 'High'],
        )
    ))
    
    risk_fig.update_layout(
        title=None,
        height=420,
        template='plotly_white',
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='Risk Category',
            side='top'
        ),
        yaxis=dict(
            title='Impact Level',
            autorange='reversed'
        )
    )
    return risk_fig

# Network graph to demonstrate GraphRAG relationships
def create_relationship_graph():
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add financial entities
    entities = [
        'Our Company', 'Supplier A', 'Supplier B', 'Customer X', 
        'Customer Y', 'Bank', 'Competitor A', 'Distributor'
    ]
    
    # Add nodes
    for entity in entities:
        G.add_node(entity)
    
    # Add relationships
    edges = [
        ('Our Company', 'Supplier A', 'Sources from'),
        ('Our Company', 'Supplier B', 'Sources from'),
        ('Customer X', 'Our Company', 'Buys from'),
        ('Customer Y', 'Our Company', 'Buys from'),
        ('Bank', 'Our Company', 'Finances'),
        ('Our Company', 'Distributor', 'Ships through'),
        ('Distributor', 'Customer X', 'Delivers to'),
        ('Distributor', 'Customer Y', 'Delivers to'),
        ('Supplier A', 'Competitor A', 'Also supplies'),
        ('Competitor A', 'Customer X', 'Also sells to')
    ]
    
    for source, target, relation in edges:
        G.add_edge(source, target, relationship=relation)
    
    # Create positions
    pos = nx.spring_layout(G, seed=42)
    
    # Create edges
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_trace.append(
            go.Scatter(
                x=[x0, x1], y=[y0, y1],
                line=dict(width=1, color='#4C5862'),
                mode='lines',
                hoverinfo='none'
            )
        )
    
    # Create nodes
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            size=15,
            color=[
                '#0A3D62' if node == 'Our Company' 
                else '#147D64' if 'Supplier' in node 
                else '#FF8800' if 'Customer' in node
                else '#4C5862'
                for node in G.nodes()
            ],
            line=dict(width=2, color='white')
        ),
        text=list(G.nodes()),
        textposition='top center',
        hoverinfo='text'
    )
    
    # Create the figure
    fig = go.Figure(data=edge_trace + [node_trace])
    fig.update_layout(
        title=None,
        showlegend=False,
        height=420,
        template='plotly_white',
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(family="IBM Plex Sans, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

# Define the page layout
layout = dmc.Container([
    # Header with context
    dmc.Stack([
        dmc.Title("Financial Visualizations", order=1, c="#0A3D62", style={"fontSize": "28px"}),
        dmc.Text("Interactive charts for financial analysis and insights", c="#333F48", size="md"),
    ], gap="xs", mb="md"),
    
    # Visualization Controls
    dmc.Paper([
        dmc.Group([
            dmc.Group([
                DashIconify(icon="carbon:chart-area", width=24, color="#0A3D62"),
                dmc.Title("Visualization Controls", order=5, c="#333F48")
            ], gap="xs"),
            dmc.Group([
                dmc.Select(
                    label="Time Range",
                    placeholder="Select time range",
                    id="time-range-select",
                    value="12m",
                    data=[
                        {"value": "3m", "label": "Last 3 Months"},
                        {"value": "6m", "label": "Last 6 Months"},
                        {"value": "12m", "label": "Last 12 Months"},
                        {"value": "ytd", "label": "Year to Date"},
                        {"value": "all", "label": "All Time"}
                    ],
                    style={"width": 200}
                ),
                dmc.Select(
                    label="Chart Type",
                    placeholder="Select chart type",
                    id="chart-type-select",
                    value="all",
                    data=[
                        {"value": "all", "label": "All Charts"},
                        {"value": "time", "label": "Time Series"},
                        {"value": "comparison", "label": "Comparatives"},
                        {"value": "risk", "label": "Risk Analysis"},
                        {"value": "relationship", "label": "Relationships"}
                    ],
                    style={"width": 200}
                ),
                dmc.Button(
                    "Update Visualizations",
                    id="update-viz-button",
                    leftSection=DashIconify(icon="carbon:update-now"),
                    color="#0A3D62",
                    radius="md"
                )
            ], gap="md")
        ], justify="space-between", align="flex-end")
    ], p="md", shadow="sm", radius="md", withBorder=True, mb="md"),
    
    # Main Visualizations Grid
    dmc.SimpleGrid(
        cols=2,
        spacing="md",
        children=[
            # Time Series Chart
            dmc.Paper([
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Revenue & Expenses Over Time", order=5, c="#333F48"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="subtle",
                            size="md"
                        )
                    ], justify="space-between"),
                    dcc.Graph(
                        id="time-series-chart",
                        figure=create_time_series_chart(),
                        config={"displayModeBar": False}
                    )
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, mb="lg"),
            
            # Comparative Analysis Chart
            dmc.Paper([
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Competitive Comparison", order=5, c="#333F48"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray", 
                            variant="subtle",
                            size="md"
                        )
                    ], justify="space-between"),
                    dcc.Graph(
                        id="comparative-chart",
                        figure=create_comparative_chart(),
                        config={"displayModeBar": False}
                    )
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, mb="lg"),
            
            # Risk Assessment Heatmap
            dmc.Paper([
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Risk Assessment Heatmap", order=5, c="#333F48"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="subtle",
                            size="md"
                        )
                    ], justify="space-between"),
                    dcc.Graph(
                        id="risk-heatmap",
                        figure=create_risk_heatmap(),
                        config={"displayModeBar": False}
                    )
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, mb="lg"),
            
            # Financial Relationship Graph
            dmc.Paper([
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Financial Relationship Graph", order=5, c="#333F48"),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="subtle",
                            size="md"
                        )
                    ], justify="space-between"),
                    dcc.Graph(
                        id="relationship-graph",
                        figure=create_relationship_graph(),
                        config={"displayModeBar": False}
                    )
                ], gap="xs")
            ], p="md", shadow="sm", radius="md", withBorder=True, mb="lg")
        ]
    )
], fluid=True, px="md", py="lg", style={"backgroundColor": "#f8f9fa"})

# Callback functions defined directly in the page file
@callback(
    [Output("time-series-chart", "figure"),
     Output("comparative-chart", "figure")],
    [Input("update-viz-button", "n_clicks")],
    [State("time-range-select", "value"),
     State("chart-type-select", "value")]
)
def update_charts(n_clicks, time_range, chart_type):
    # Default return if no clicks yet
    if n_clicks is None:
        return create_time_series_chart(), create_comparative_chart()
    
    # Just return the same charts for demonstration
    # In a real implementation, we would filter data based on time_range,
    # change the chart_type, and show only the selected metrics
    return create_time_series_chart(), create_comparative_chart() 