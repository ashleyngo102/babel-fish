from http.server import HTTPServer, BaseHTTPRequestHandler
import csv
import io
import json

cached_data = {"goal": None, "headers": [], "rows": [], "total_rows": 0}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                goal = data.get('goal')
                csv_content = data.get('file_content')
                
                f = io.StringIO(csv_content)
                reader = csv.reader(f)
                headers = [h.strip() for h in next(reader) if h.strip()]
                
                rows = [row[:len(headers)] for row in reader if any(row)]
                
                global cached_data
                cached_data = {"goal": goal, "headers": headers, "rows": rows, "total_rows": len(rows)}
                
                self._set_headers()
                self.wfile.write(json.dumps({
                    "goal": goal, 
                    "headers": headers, 
                    "top_5_rows": rows[:5], 
                    "total_rows": len(rows)
                }).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run(port=8003):
    print(f'Starting Babel Fish Backend on port {port}...')
    HTTPServer(('', port), RequestHandler).serve_forever()

if __name__ == '__main__':
    run()
