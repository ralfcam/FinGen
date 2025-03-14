from dash import html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_mantine_components import Select, MultiSelect, Textarea, Switch, Paper, Stack
import dash

# Register this module as a page with Dash Pages
dash.register_page(__name__, path='/reports')

# Sample report templates
REPORT_TEMPLATES = [
    {"value": "executive_summary", "label": "Executive Summary", "description": "High-level overview of financial performance"},
    {"value": "quarterly_report", "label": "Quarterly Report", "description": "Detailed quarterly financial analysis"},
    {"value": "annual_report", "label": "Annual Report", "description": "Comprehensive annual financial review"},
    {"value": "market_analysis", "label": "Market Analysis", "description": "Market position and competitive analysis"},
    {"value": "risk_report", "label": "Risk Report", "description": "Risk assessment and mitigation strategies"}
]

# Sample content sections
CONTENT_SECTIONS = [
    {"value": "financial_metrics", "label": "Financial Metrics", "description": "Key financial indicators and trends"},
    {"value": "market_position", "label": "Market Position", "description": "Competitive analysis and market share"},
    {"value": "risk_assessment", "label": "Risk Assessment", "description": "Risk factors and mitigation strategies"},
    {"value": "forecast", "label": "Forecast", "description": "Financial projections and scenarios"},
    {"value": "recommendations", "label": "Recommendations", "description": "Strategic recommendations and action items"}
]

# Define the layout directly
layout = dmc.Container([
    # Header
    dmc.Grid([
        dmc.GridCol([
            html.H1("Report Generation", className="mb-4"),
            html.P("Create and customize financial reports", className="text-muted")
        ], span=12)
    ]),
    
    # Main Report Interface
    dmc.Grid([
        # Template Selection and Customization
        dmc.GridCol([
            dmc.Card([
                html.H5("Report Template", className="card-title mb-3"),
                Select(
                    id='template-select',
                    data=REPORT_TEMPLATES,
                    placeholder="Select a template",
                    className="mb-3"
                ),
                html.Div(id='template-description-reports', className="text-muted mb-3"),
                
                html.H5("Content Sections", className="card-title mt-4 mb-3"),
                MultiSelect(
                    id='content-sections',
                    data=CONTENT_SECTIONS,
                    placeholder="Select sections to include",
                    className="mb-3"
                ),
                
                html.H5("Report Options", className="card-title mt-4 mb-3"),
                dmc.Stack([
                    dmc.Checkbox(
                        label="Include Executive Summary",
                        value=True,
                        id="option-exec-summary"
                    ),
                    dmc.Checkbox(
                        label="Include Charts and Graphs",
                        value=True,
                        id="option-charts"
                    ),
                    dmc.Checkbox(
                        label="Include Detailed Analysis",
                        value=False,
                        id="option-detailed"
                    ),
                    dmc.Checkbox(
                        label="Include Recommendations",
                        value=False,
                        id="option-recommendations"
                    )
                ], gap="xs", className="mb-3"),
                
                html.H5("Additional Notes", className="card-title mt-4 mb-3"),
                Textarea(
                    id='report-notes',
                    placeholder="Add any specific notes or requirements for the report",
                    minRows=3,
                    className="mb-3"
                ),
                
                dmc.ButtonGroup([
                    dmc.Button([
                        DashIconify(icon="radix-icons:eye-open"),
                        " Preview Report"
                    ], color="primary", id="preview-button", className="me-2"),
                    dmc.Button([
                        DashIconify(icon="radix-icons:download"),
                        " Generate Report"
                    ], color="success", id="generate-button", className="me-2"),
                    dmc.Button([
                        DashIconify(icon="radix-icons:reset"),
                        " Reset"
                    ], color="secondary", id="reset-button")
                ])
            ], p="md")
        ], span=4),
        
        # Report Preview
        dmc.GridCol([
            dmc.Card([
                html.H5("Report Preview", className="card-title mb-3"),
                html.Div([
                    html.Div([
                        html.H6("Executive Summary", className="preview-section"),
                        html.P("This section will show a preview of the executive summary...")
                    ], className="preview-content mb-4"),
                    
                    html.Div([
                        html.H6("Financial Metrics", className="preview-section"),
                        html.P("This section will show a preview of the financial metrics...")
                    ], className="preview-content mb-4"),
                    
                    html.Div([
                        html.H6("Market Position", className="preview-section"),
                        html.P("This section will show a preview of the market position analysis...")
                    ], className="preview-content mb-4"),
                    
                    html.Div([
                        html.H6("Risk Assessment", className="preview-section"),
                        html.P("This section will show a preview of the risk assessment...")
                    ], className="preview-content mb-4"),
                    
                    html.Div([
                        html.H6("Recommendations", className="preview-section"),
                        html.P("This section will show a preview of the recommendations...")
                    ], className="preview-content")
                ], id="report-preview")
            ], p="md")
        ], span=8)
    ], className="mb-4"),
    
    # Export Options
    dmc.Grid([
        dmc.GridCol([
            dmc.Card([
                html.H5("Export Options", className="card-title mb-3"),
                dmc.Grid([
                    dmc.GridCol([
                        dmc.Button([
                            DashIconify(icon="radix-icons:file-pdf"),
                            " Export as PDF"
                        ], color="danger", className="me-2"),
                        dmc.Button([
                            DashIconify(icon="radix-icons:file-excel"),
                            " Export as Excel"
                        ], color="success", className="me-2"),
                        dmc.Button([
                            DashIconify(icon="radix-icons:file-powerpoint"),
                            " Export as PowerPoint"
                        ], color="warning")
                    ], span=12)
                ])
            ], p="md")
        ], span=12)
    ])
], fluid=True, className="py-4")

# Define callbacks directly in the page
@callback(
    Output("template-description-reports", "children"),
    Input("template-select", "value")
)
def update_template_description(value):
    if value:
        template = next((t for t in REPORT_TEMPLATES if t["value"] == value), None)
        return template["description"] if template else ""
    return ""

@callback(
    Output("report-preview", "children"),
    [Input("template-select", "value"),
     Input("content-sections", "value"),
     Input("option-exec-summary", "checked"),
     Input("option-charts", "checked"),
     Input("option-detailed", "checked"),
     Input("option-recommendations", "checked"),
     Input("report-notes", "value")]
)
def update_report_preview(template, sections, exec_summary, charts, detailed, recommendations, notes):
    preview_sections = []
    
    if exec_summary:
        preview_sections.append(
            html.Div([
                html.H6("Executive Summary", className="preview-section"),
                html.P("This section will show a preview of the executive summary...")
            ], className="preview-content mb-4")
        )
    
    if sections:
        for section in sections:
            section_data = next((s for s in CONTENT_SECTIONS if s["value"] == section), None)
            if section_data:
                preview_sections.append(
                    html.Div([
                        html.H6(section_data["label"], className="preview-section"),
                        html.P(section_data["description"])
                    ], className="preview-content mb-4")
                )
    
    if notes:
        preview_sections.append(
            html.Div([
                html.H6("Additional Notes", className="preview-section"),
                html.P(notes)
            ], className="preview-content mb-4")
        )
    
    return preview_sections if preview_sections else "Select options to preview the report" 