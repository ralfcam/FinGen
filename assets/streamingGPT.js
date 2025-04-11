window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // Renamed function for clarity
        streaming_Chat_Handler: async function(n_clicks, states) {
            // states will be an array: [promptValue, chatMode, sessionId]
            const prompt = states[0];
            const chatMode = states[1];
            const sessionId = states[2];
            
            // Skip processing if no clicks, no prompt, or (in agent mode) no session ID
            if (!n_clicks || !prompt || (chatMode === 'agent' && !sessionId)) {
                // Check if it's just missing session ID temporarily during load
                if (chatMode === 'agent' && !sessionId) {
                    console.warn("Agent mode selected, but session ID not yet available. Please wait a moment and try again.");
                    // Optionally provide user feedback here
                    return true; // Keep button disabled briefly
                }
                return false; // Enable the button if no click or prompt
            }
            
            const responseWindow = document.querySelector("#chat-response-window");
            if (!responseWindow) {
                console.error("Response window element (#chat-response-window) not found.");
                return true; // Keep button disabled
            }

            // Clear only *before* starting a new stream
            responseWindow.innerHTML = ''; 
            
            // Configure marked.js (ensure it's loaded via external_scripts in chat.py)
            if (typeof marked !== 'undefined') {
                 marked.setOptions({
                    highlight: function(code) {
                        if (typeof hljs !== 'undefined') {
                            return hljs.highlightAuto(code).value;
                        }
                        return code; 
                    }
                 });
            } else {
                 console.warn("marked.js not loaded. Markdown rendering will be basic.");
            }

            try {
                // Send request to the backend endpoint
                const response = await fetch("/streaming-chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    // Send prompt, mode, and session ID
                    body: JSON.stringify({ 
                        prompt: prompt, 
                        mode: chatMode, 
                        session_id: sessionId 
                    }),
                });

                if (!response.ok) {
                     const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
                     console.error("Server error:", errorData);
                     responseWindow.innerHTML = `<p style="color: red;">Error: ${errorData.error || `Failed to fetch stream (${response.status})`}</p>`;
                     return false; // Re-enable button on error
                }

                const decoder = new TextDecoder();
                const reader = response.body.getReader();
                let accumulatedChunks = ""; // Accumulate chunks for parsing
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    accumulatedChunks += decoder.decode(value, { stream: true });

                    // Render accumulated markdown
                    try {
                        if (typeof marked !== 'undefined') {
                            responseWindow.innerHTML = marked.parse(accumulatedChunks);
                        } else {
                            // Basic rendering if marked is unavailable
                            responseWindow.innerText = accumulatedChunks;
                        }
                        responseWindow.scrollTop = responseWindow.scrollHeight;
                    } catch (parseError) {
                        console.error("Markdown parsing error:", parseError);
                        // Display raw text if parsing fails
                        responseWindow.innerText = accumulatedChunks;
                    }
                }
            } catch (error) {
                console.error("Streaming error:", error);
                responseWindow.innerHTML += `<p style="color: red;">\n\n[Error during streaming: ${error}]</p>`;
                responseWindow.scrollTop = responseWindow.scrollHeight;
            }
            
            // Return false to re-enable the submit button
            return false;
          }
    }
});