from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import sys
import json
import caller  # assuming caller is your module

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Parse query parameters from URL
        url_parts = urlparse(self.path)
        query_params = parse_qs(url_parts.query)

        # Extract trainNo and date from query parameters
        trainNo = query_params.get('trainNo', [None])[0]
        date = query_params.get('date', [None])[0]

        # Call main function with obtained trainNo and date
        result = main(trainNo, date)
        
        # Convert result to JSON and send as response
        self.wfile.write(json.dumps(result).encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parse query parameters from POST data
        query_params = parse_qs(post_data)
        
        # Extract trainNo and date from query parameters
        trainNo = query_params.get('trainNo', [None])[0]
        date = query_params.get('date', [None])[0]

        # Call main function with obtained trainNo and date
        result = main(trainNo, date)

        # Convert result to JSON and send as response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

def main(trainNo, date):
    try:
        # Set date to None if empty string is provided
        if date == "":
            date = None

        # Call the external function (caller) with trainNo and date
        return caller.call_site(trainNo, date)
    except Exception as e:
        # Handle exceptions here, log them or return an appropriate error response
        print(f"Error in main function: {e}")
        return {"error": str(e)}

def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python index.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    run(port=port)
