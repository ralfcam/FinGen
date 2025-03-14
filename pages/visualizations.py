from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash

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

# Create sample data and figures
df = create_sample_data()

# Time series analysis
time_series_fig = go.Figure()
time_series_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['revenue'],
    name='Revenue',
    line=dict(color='#2ecc71')
))
time_series_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['expenses'],
    name='Expenses',
    line=dict(color='#e74c3c')
))
time_series_fig.update_layout(
    title='Revenue vs Expenses Over Time',
    height=400,
    template='plotly_white'
)

# Comparative analysis
comparative_fig = go.Figure()
comparative_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['revenue'],
    name='Our Revenue',
    line=dict(color='#2ecc71')
))
comparative_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['competitor_a'],
    name='Competitor A',
    line=dict(color='#3498db')
))
comparative_fig.add_trace(go.Scatter(
    x=df.index,
    y=df['competitor_b'],
    name='Competitor B',
    line=dict(color='#e74c3c')
))
comparative_fig.update_layout(
    title='Market Position Comparison',
    height=400,
    template='plotly_white'
)

# Risk assessment heat map
risk_data = np.random.rand(5, 5)
risk_fig = go.Figure(data=go.Heatmap(
    z=risk_data,
    x=['Market', 'Financial', 'Operational', 'Regulatory', 'Strategic'],
    y=['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'],
    colorscale='RdYlGn_r'
))
risk_fig.update_layout(
    title='Risk Assessment Heat Map',
    height=400,
    template='plotly_white'
)

# Define the page layout directly
layout = dmc.Container([
    # Header
    dmc.Grid([
        dmc.GridCol([
            html.H1("Detailed Visualizations", className="mb-4"),
            html.P("Interactive charts and relationship analysis", className="text-muted")
        ], span=12)
    ]),
    
    # Visualization Controls
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Visualization Controls", className="card-title mb-3"),
                dmc.Grid([
                    dmc.GridCol([
                        html.Label("Time Range"),
                        dcc.Dropdown(
                            id='time-range-dropdown',
                            options=[
                                {'label': 'Last 3 Months', 'value': '3m'},
                                {'label': 'Last 6 Months', 'value': '6m'},
                                {'label': 'Last Year', 'value': '1y'},
                                {'label': 'Custom Range', 'value': 'custom'}
                            ],
                            value='1y',
                            className="mb-3"
                        )
                    ], span=6),
                    dmc.GridCol([
                        html.Label("Chart Type"),
                        dcc.Dropdown(
                            id='chart-type-dropdown',
                            options=[
                                {'label': 'Line Chart', 'value': 'line'},
                                {'label': 'Bar Chart', 'value': 'bar'},
                                {'label': 'Area Chart', 'value': 'area'},
                                {'label': 'Scatter Plot', 'value': 'scatter'}
                            ],
                            value='line',
                            className="mb-3"
                        )
                    ], span=6)
                ])
            ], p="md")
        ], span=12)
    ], className="mb-4"),
    
    # Time Series Analysis
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Time Series Analysis", className="card-title"),
                dcc.Graph(
                    id='time-series-chart',
                    figure=time_series_fig,
                    config={'displayModeBar': True}
                )
            ], p="md")
        ], span=12)
    ], className="mb-4"),
    
    # Comparative Analysis
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Market Position Comparison", className="card-title"),
                dcc.Graph(
                    id='comparative-chart',
                    figure=comparative_fig,
                    config={'displayModeBar': True}
                )
            ], p="md")
        ], span=12)
    ], className="mb-4"),
    
    # Risk Assessment
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Risk Assessment", className="card-title"),
                dcc.Graph(
                    id='risk-heatmap',
                    figure=risk_fig,
                    config={'displayModeBar': True}
                )
            ], p="md")
        ], span=12)
    ], className="mb-4"),
    
    # GraphRAG Relationship Explorer
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Financial Entity Relationships", className="card-title"),
                html.Div([
                    html.P("This section will display the GraphRAG relationship explorer showing connections between financial entities."),
                    dmc.Button([
                        DashIconify(icon="radix-icons:graph"),
                        " Load Relationship Graph"
                    ], color="primary", id="load-graph-button")
                ])
            ], p="md")
        ], span=12)
    ])
], fluid=True, className="py-4")

# Callback functions defined directly in the page file
@callback(
    [Output("time-series-chart", "figure"),
     Output("comparative-chart", "figure")],
    [Input("time-range-dropdown", "value"),
     Input("chart-type-dropdown", "value")]
)
def update_charts(time_range, chart_type):
    df = create_sample_data()
    
    # Update time series chart
    time_series_fig = go.Figure()
    time_series_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Revenue',
        line=dict(color='#2ecc71')
    ))
    time_series_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['expenses'],
        name='Expenses',
        line=dict(color='#e74c3c')
    ))
    time_series_fig.update_layout(
        title='Revenue vs Expenses Over Time',
        height=400,
        template='plotly_white'
    )
    
    # Update comparative chart
    comparative_fig = go.Figure()
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['revenue'],
        name='Our Revenue',
        line=dict(color='#2ecc71')
    ))
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['competitor_a'],
        name='Competitor A',
        line=dict(color='#3498db')
    ))
    comparative_fig.add_trace(go.Scatter(
        x=df.index,
        y=df['competitor_b'],
        name='Competitor B',
        line=dict(color='#e74c3c')
    ))
    comparative_fig.update_layout(
        title='Market Position Comparison',
        height=400,
        template='plotly_white'
    )
    
    return time_series_fig, comparative_fig 