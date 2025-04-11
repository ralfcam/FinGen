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
from ollama import Client  # Changed from ollama_python.client import Ollama
import json # Import json for error handling

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

# --- Ollama Configuration ---
# Consider moving these to a config file or environment variables
OLLAMA_BASE_URL = "http://localhost:11434" # Default Ollama API URL
OLLAMA_MODEL = "deepseek-r1:14b" # Default model to use

try:
    # Initialize the Ollama client properly
    ollama_client = Client(host=OLLAMA_BASE_URL)  # Changed from Ollama to Client
except Exception as e:
    print(f"Error initializing Ollama client: {e}")
    ollama_client = None # Handle initialization error

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
    if not ollama_client:
        return Response(json.dumps({"error": "Ollama client not initialized"}), status=503, mimetype='application/json')

    try:
        user_prompt = request.json["prompt"]
        print(f"Received prompt: {user_prompt}") # Debug print

        # Format messages for Ollama chat endpoint
        messages = [{'role': 'user', 'content': user_prompt}]

        def response_stream():
            try:
                # Use the chat method from ollama client with stream=True
                stream = ollama_client.chat(
                    model=OLLAMA_MODEL,
                    messages=messages,
                    stream=True
                )
                print("Stream started...") # Debug print
                for chunk in stream:
                    # Handle the response structure from ollama Client
                    if hasattr(chunk, 'message') and hasattr(chunk.message, 'content'):
                        content = chunk.message.content
                        yield content
                    # Fallback to dictionary access if it's returned as a dict
                    elif isinstance(chunk, dict):
                        if 'message' in chunk and 'content' in chunk['message']:
                            content = chunk['message']['content']
                            yield content
                        # Handle potential errors in the stream
                        elif 'error' in chunk:
                            print(f"Error in stream chunk: {chunk['error']}")
                            yield f"\n\n[Error: {chunk['error']}]\n"
                print("Stream finished.") # Debug print
            except Exception as e:
                print(f"Error during streaming: {e}")
                yield f"\n\n[Error generating response: {e}]\n"

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