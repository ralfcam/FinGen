import dash
from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    clientside_callback,
    ClientsideFunction,
    register_page,
)
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import request, Response
import json # Import json for error handling

# Import the LLM service functions
from utils.llm_service import stream_llm_response

# Register this page with Dash
register_page(
    __name__, 
    path='/chat',
    external_stylesheets=['/assets/external/markdown-code.css'],
    external_scripts=[
        '/assets/external/marked.min.js',
        '/assets/external/highlight.min.js'
    ]
)

# --- Layout ---
layout = dmc.Container(
    [
        dmc.Stack(
            [
                dmc.Title("AI Assistant", order=1, fw="bold", mb="lg"),
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        dmc.TextInput(
                                            id="chat-prompt",
                                            placeholder="Ask me anything...",
                                            style={"width": "100%"},
                                            leftSection=DashIconify(icon="radix-icons:chat-bubble"),
                                            size="md",
                                            radius="md",
                                            n_submit=0,  # Enable Enter key submissions
                                        ),
                                        dmc.Button(
                                            "Send",
                                            id="submit-chat",
                                            variant="filled",
                                            color="blue",
                                            radius="md",
                                            size="md",
                                            rightSection=DashIconify(icon="radix-icons:paper-plane"),
                                            n_clicks=0,
                                        ),
                                    ],
                                    align="flex-end",
                                    grow=True,
                                    style={"marginBottom": "20px"},
                                ),
                                dmc.Title("Response", order=5, c="dimmed", mb="md"),
                                dmc.Paper(
                                    id="chat-response-window",
                                    p="md",
                                    withBorder=True,
                                    radius="md",
                                    style={
                                        "minHeight": "300px",
                                        "maxHeight": "500px",
                                        "overflowY": "auto",
                                        "whiteSpace": "pre-wrap",
                                        "fontFamily": "monospace",
                                        "backgroundColor": "#f8f9fa",
                                    },
                                ),
                            ],
                            gap="md",
                        )
                    ],
                    shadow="sm",
                    p="xl",
                    withBorder=True,
                    radius="md",
                    style={"backgroundColor": "white"},
                ),
                dmc.Text(
                    "Powered by Ollama", 
                    ta="center", 
                    c="dimmed", 
                    size="sm", 
                    mt="lg"
                )
            ],
            align="stretch",
            gap="xl",
        )
    ],
    size="lg",
    px="md",
    py="xl",
    style={"maxWidth": "900px"},
)

# --- Backend Route for Streaming ---
# Use dash.get_app() to access the server instance in a multi-page app context
@dash.get_app().server.route("/streaming-chat", methods=["POST"])
def streaming_chat():
    try:
        user_prompt = request.json["prompt"]
        print(f"Received prompt: {user_prompt}") # Debug print

        def response_stream():
            # Use the stream_llm_response function from our service module
            yield from stream_llm_response(user_prompt)

        return Response(response_stream(), mimetype="text/event-stream") # Use text/event-stream for SSE

    except Exception as e:
        print(f"Error in /streaming-chat endpoint: {e}")
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


# --- Clientside Callbacks ---

# JS callback to send the question to the flask API and handle the response stream
clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="streaming_GPT"),
    Output("submit-chat", "disabled"), # Disable button during stream
    Input("submit-chat", "n_clicks"),
    State("chat-prompt", "value"),
    prevent_initial_call=True,
)

# Clears the input field after the user clicks submit, and disables submit button initially
clientside_callback(
    """
    function clearInput(n_clicks) {
        // When the submit button is clicked (n_clicks > 0),
        // clear the input and disable the button.
        // The streaming_GPT callback will re-enable it when done.
        if (n_clicks > 0) {
            return ["", true];
        }
        // Keep button enabled initially or if n_clicks is not updated properly
        return [dash_clientside.no_update, false];
    }
    """,
    Output("chat-prompt", "value"),
    Output("submit-chat", "disabled", allow_duplicate=True), # Allow multiple outputs to 'disabled'
    Input("submit-chat", "n_clicks"),
    prevent_initial_call=True, # Important: prevent running on page load
)

# Optional: Add a callback to handle Enter key press in the input field
clientside_callback(
    """
    function(inputValue) {
        // This function doesn't trigger the submit, but enables/disables it.
        // Actual submission is handled by the button click or another callback if needed.
        // We return no_update because this callback doesn't change component props directly.
        // The primary logic for submission remains tied to the button click.

        // If you want Enter key to trigger submission, you'd need a different setup,
        // likely involving dcc.Input's 'n_submit' property and potentially
        // combining callbacks or using pattern-matching callbacks if multiple
        // triggers are needed. For simplicity, we stick to the button click here.

        return window.dash_clientside.no_update; // Indicate no change to outputs
    }
    """,
    Output("submit-chat", "id"), # Dummy output, required by Dash
    Input("chat-prompt", "n_submit"),
    State("chat-prompt", "value"),
    prevent_initial_call=True,
) 