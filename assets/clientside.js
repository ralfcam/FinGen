// Client-side callback functions for the FinGen application
// These functions run in the browser and can improve performance
// by handling simple interactions without server requests

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    // Main clientside namespace used in callbacks
    clientside: {
        // Example client-side callback
        updateOutput: function(n_clicks, value) {
            if (n_clicks === null) {
                return window.dash_clientside.no_update;
            }
            return `Client-side processed: ${value}`;
        }
        // Note: streaming_GPT function is defined in streamingGPT.js
    }
}); 