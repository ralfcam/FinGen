from dash import html, dcc, callback, Output, Input
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify

# Register this module as a page with Dash Pages
dash.register_page(
    __name__,
    path_template="/404",
    title="404 - Page Not Found",
    description="Page not found"
)

# 404 error page layout
layout = dmc.Container([
    dmc.Stack([
        dmc.Title("404 - Page Not Found", order=1, ta="center"),
        dmc.Image(
            src="/assets/404.svg",
            alt="404 error",
            style={"maxWidth": "400px", "margin": "0 auto"}
        ),
        dmc.Text("The page you're looking for doesn't exist or has been moved.", ta="center"),
        dmc.Group([
            dmc.Button(
                "Return to Dashboard",
                leftSection=DashIconify(icon="radix-icons:dashboard"),
                color="blue",
                radius="md",
                id="return-to-dashboard-button"
            )
        ], justify="center", mt="xl")
    ], align="center", gap="lg"),
    dcc.Location(id='not-found-redirect', refresh=True)
], py="xl", style={"minHeight": "80vh", "display": "flex", "alignItems": "center"})

# Callback to handle button click
@callback(
    Output('not-found-redirect', 'pathname'),
    Input('return-to-dashboard-button', 'n_clicks'),
    prevent_initial_call=True
)
def redirect_to_dashboard(n_clicks):
    if n_clicks:
        return "/"
    return dash.no_update

# Custom 404 handler
def layout_404(pathname):
    return dmc.Container([
        dmc.Stack([
            dmc.Title("404 - Page Not Found", order=1, ta="center"),
            dmc.Text(f"The path '{pathname}' was not found on this server.", ta="center"),
            dmc.Group([
                dmc.Button(
                    "Return to Dashboard",
                    leftSection=DashIconify(icon="radix-icons:dashboard"),
                    color="blue",
                    radius="md",
                    id="return-to-dashboard-button-custom"
                )
            ], justify="center", mt="xl"),
            dcc.Location(id='not-found-redirect-custom', refresh=True)
        ], align="center", gap="lg")
    ], py="xl", style={"minHeight": "80vh", "display": "flex", "alignItems": "center"})

# Callback for custom 404 button
@callback(
    Output('not-found-redirect-custom', 'pathname'),
    Input('return-to-dashboard-button-custom', 'n_clicks'),
    prevent_initial_call=True
)
def redirect_to_dashboard_custom(n_clicks):
    if n_clicks:
        return "/"
    return dash.no_update 