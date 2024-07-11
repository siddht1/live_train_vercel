from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import re
import caller

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Extract trainNo and date from query parameters
        trainNo = query_params.get('trainNo', [None])[0]
        date = query_params.get('date', [None])[0]

        if trainNo and self.is_valid_train(trainNo):
            # Handling empty date
            if date is None or date == "":
                date = None
            
            try:
                status = caller.call_site(trainNo, date)
                if status:
                    self.wfile.write(json.dumps(status).encode('utf-8'))
                else:
                    self.wfile.write(json.dumps({"error": "Failed to fetch Live Train status"}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": f"Exception occurred: {str(e)}"}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"error": "Invalid or missing Train number"}).encode('utf-8'))

    def is_valid_train(self, trainNo):
        return bool(re.match(r'^\d{5}$', trainNo))
