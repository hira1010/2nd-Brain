const http = require('http');
const WebSocket = require('ws');

http.get('http://127.0.0.1:9222/json', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const targets = JSON.parse(data);
            const page = targets.find(t => t.type === 'page' && t.url && t.url.includes('index.html'));
            if (!page) {
                console.log("No valid page found.");
                return;
            }
            const ws = new WebSocket(page.webSocketDebuggerUrl);
            ws.on('open', () => {
                ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
                ws.send(JSON.stringify({ id: 2, method: 'Log.enable' }));
                
                // Get caught exceptions
                ws.send(JSON.stringify({ 
                    id: 3, 
                    method: 'Runtime.evaluate', 
                    params: { expression: 'if(window.SceneManager && SceneManager._catchException) { SceneManager._catchException }' } 
                }));
                
                // Wait for logs
                setTimeout(() => {
                    console.log("Finished waiting for logs.");
                    ws.close();
                }, 2000);
            });
            ws.on('message', (msg) => {
                const parsed = JSON.parse(msg);
                if (parsed.method === 'Runtime.consoleAPICalled') {
                    const args = parsed.params.args.map(a => a.value || a.description).join(' ');
                    console.log(`[CONSOLE] ${parsed.params.type}: ${args}`);
                } else if (parsed.method === 'Runtime.exceptionThrown') {
                    console.log(`[EXCEPTION] ${parsed.params.exceptionDetails.exception.description}`);
                }
            });
        } catch(e) { console.error(e); }
    });
}).on('error', (err) => console.error("HTTP Error:", err.message));
