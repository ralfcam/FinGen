window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        streaming_GPT: async function streamingGPT(n_clicks, prompt) {
            
            // Use the ID from the new chat page layout
            const responseWindow = document.querySelector("#chat-response-window");
            
            // Check if the element exists
            if (!responseWindow) {
                console.error("Response window element (#chat-response-window) not found.");
                return true; // Return true to keep the button disabled if element not found
            }

            // Reset content
            responseWindow.innerHTML = "";
            
            // "marked.js" is used to parse the incoming stream
            // it is also a good idea to state in the prompt that the "response should be markdown formatted"
            // this definition changes the color scheme of the parsed code. If your use-case does not include parsing code, you can remove this part, as well as "asssets/external/highlight.min.js" and "asssets/external/markdown-code.css"
            // if your application use-case includes parsing code and wish to change color scheme of the parsed code, you can do so in "asssets/external/markdown-code.css"
            // alternatively, you can go to "https://highlightjs.org/static/demo/" to find a theme you like and then download it from "https://github.com/highlightjs/highlight.js/tree/main/src/styles"
            marked.setOptions({
                highlight: function(code) {
                    // Ensure hljs is loaded
                    if (typeof hljs !== 'undefined') {
                        return hljs.highlightAuto(code).value;
                    }
                    return code; // Return raw code if highlight.js is not available
                }
            });

            try {
                // Send the messages to the server to get the streaming response
                const response = await fetch("/streaming-chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ prompt }),
                });

                if (!response.ok) {
                     // Handle HTTP errors (e.g., 500, 503)
                     const errorData = await response.json().catch(() => ({ error: `HTTP error ${response.status}` }));
                     console.error("Server error:", errorData);
                     responseWindow.innerHTML = `<p style="color: red;">Error: ${errorData.error || `Failed to fetch stream (${response.status})`}</p>`;
                     return false; // Re-enable button on error
                }

                // Create a new TextDecoder to decode the streamed response text
                const decoder = new TextDecoder();
                
                // Set up a new ReadableStream to read the response body
                const reader = response.body.getReader();
                let chunks = "";
                
                // Read the response stream as chunks and append them to the chat log
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    chunks += decoder.decode(value, { stream: true }); // Pass stream: true for potentially better handling of multi-byte chars

                    // Debounce or throttle rendering if performance becomes an issue
                    const htmlText = marked.parse(chunks); // Parse markdown
                    responseWindow.innerHTML = htmlText;
                    // Optional: Scroll to bottom
                    responseWindow.scrollTop = responseWindow.scrollHeight;
                }
            } catch (error) {
                console.error("Streaming error:", error);
                responseWindow.innerHTML += `<p style="color: red;">\n\n[Error during streaming: ${error}]</p>`;
                 // Optional: Scroll to bottom even on error
                responseWindow.scrollTop = responseWindow.scrollHeight;
            }
            
            // return false to enable the submit button again (disabled=false)
            return false;
          }
    }
});