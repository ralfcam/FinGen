import dash
import uuid # For generating session IDs
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
from flask import request, Response, jsonify # Added jsonify for potential async errors
import json
import asyncio # Needed for running async agent handler

# Import the LLM and Agent service functions
from utils.llm_service import stream_llm_response
from utils.agent_service import handle_agent_message, get_agent_executor # Import agent handler

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

# Initialize the agent executor on startup (optional, but can catch compile errors early)
# get_agent_executor()

# --- Layout ---
layout = dmc.Container(
    [
        dcc.Store(id='session-id-store'), # Store for the unique session ID
        dmc.Stack(
            [
                dmc.Title("AI Assistant", order=1, fw="bold", mb="lg"),
                dmc.Paper(
                    [
                        dmc.Stack(
                            [
                                dmc.SegmentedControl(
                                    id="chat-mode-selector",
                                    value="direct", # Default mode
                                    data=[
                                        {"label": "Direct Chat", "value": "direct"},
                                        {"label": "Agent Chat (with Memory)", "value": "agent"},
                                    ],
                                    mb="lg",
                                    color="blue",
                                    fullWidth=True,
                                ),
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
                    "Powered by Ollama & LangGraph", 
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

# --- Backend Route for Streaming (Now Async) ---
@dash.get_app().server.route("/streaming-chat", methods=["POST"])
async def streaming_chat(): # Make the route async
    data = await request.get_json()
    user_prompt = data.get("prompt")
    mode = data.get("mode", "direct") # Default to direct chat
    session_id = data.get("session_id")

    if not user_prompt:
        return Response(json.dumps({"error": "Prompt is required"}), status=400, mimetype='application/json')
    if mode == "agent" and not session_id:
         return Response(json.dumps({"error": "Session ID is required for agent mode"}), status=400, mimetype='application/json')

    print(f"Received request - Mode: {mode}, Session: {session_id}, Prompt: {user_prompt[:50]}...")

    async def response_stream_generator():
        try:
            if mode == "agent":
                # Call the async agent message handler
                async for chunk in handle_agent_message(session_id, user_prompt):
                    yield chunk
            else: # Default to direct chat
                # Call the synchronous LLM response stream (needs to be run in executor or adapted)
                # For simplicity here, we'll assume stream_llm_response can yield directly
                # In a real async app, you might run sync generators in an executor
                 for chunk in stream_llm_response(user_prompt):
                    yield chunk
        except Exception as e:
            print(f"Error during streaming generation ({mode} mode): {e}")
            yield f"\n\n[Error: Server error processing request in {mode} mode.]\n"
            
    return Response(response_stream_generator(), mimetype="text/event-stream")

# --- Clientside Callbacks --- 

# Generate or retrieve session ID on load
clientside_callback(
    """
    function(n_intervals) {
        // Runs only once on initial load (n_intervals === 1)
        if (n_intervals === 1) {
            let sessionId = sessionStorage.getItem('finGenSessionId');
            if (!sessionId) {
                sessionId = crypto.randomUUID();
                sessionStorage.setItem('finGenSessionId', sessionId);
                console.log('Generated new session ID:', sessionId);
            }
             console.log('Using session ID:', sessionId);
            return sessionId;
        }
        return dash_clientside.no_update;
    }
    """,
    Output('session-id-store', 'data'),
    Input('url', 'pathname'), # Trigger on initial page load via URL change
    # Use dcc.Interval as a trigger if url doesn't work reliably for initial load
    # Input(dcc.Interval(id='init-interval', max_intervals=1, interval=1), 'n_intervals')
    prevent_initial_call=False # Run on load
)

# JS callback to send the question to the flask API and handle the response stream
clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="streaming_Chat_Handler"),
    Output("submit-chat", "disabled"), # Disable button during stream
    Input("submit-chat", "n_clicks"),
    [State("chat-prompt", "value"),
     State("chat-mode-selector", "value"), # Get the selected mode
     State("session-id-store", "data")], # Get the session ID
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
    function(n_submit, inputValue) { // Need inputValue to pass it along
        // This function only *enables* submission via Enter key
        // It doesn't directly call the streaming function, but relies on the 
        // streaming_GPT clientside function being triggered by the button's n_clicks changing.
        // To make Enter work directly, we'd need to simulate a button click or refactor.
        
        // A simple approach to trigger submit on Enter:
        if (n_submit > 0) {
            // Find the button and click it programmatically
            const button = document.getElementById('submit-chat');
            if (button) {
                button.click();
            }
        }
        return window.dash_clientside.no_update; // Indicate no change to outputs
    }
    """,
    Output("submit-chat", "n_clicks"), # Output to the button's n_clicks to trigger it
    Input("chat-prompt", "n_submit"),
    State("chat-prompt", "value"),
    prevent_initial_call=True,
) 