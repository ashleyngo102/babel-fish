from http.server import HTTPServer, BaseHTTPRequestHandler
import csv
import io
import json
import difflib
import os

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

    def do_GET(self):
        if self.path == '/mappings':
            try:
                base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
                
                # Load signals
                with open(os.path.join(base_path, 'google_signal.json'), 'r') as f:
                    schema = json.load(f)

                signal_names = []
                for cat, data in schema['Signals'].items():
                    if isinstance(data, dict):
                        for subcat, signals in data.items():
                            signal_names.extend([s['name'] for s in signals])
                    elif isinstance(data, list):
                        signal_names.extend([s['name'] for s in data])

                # Load CSV headers
                csv_path = os.path.join(base_path, 'Translation 2 - sample dataset-v1_generated_200.csv')
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    headers = [h.strip() for h in next(reader) if h.strip()]

                mappings = []
                for header in headers:
                    matched_exact = [s for s in signal_names if s.lower() == header.lower()]
                    if matched_exact:
                        mappings.append({
                            "client_column": header,
                            "matched_signal": matched_exact[0],
                            "logic": "One-to-One",
                            "action": "Approve"
                        })
                    else:
                        matches = difflib.get_close_matches(header, signal_names, n=1, cutoff=0.8)
                        if matches:
                            mappings.append({
                                "client_column": header,
                                "matched_signal": matches[0],
                                "logic": "One-to-One",
                                "action": "Approve"
                            })
                        else:
                            mappings.append({
                                "client_column": header,
                                "matched_signal": "None",
                                "logic": "Undetected",
                                "action": "Manual Mapping"
                            })

                self._set_headers()
                self.wfile.write(json.dumps(mappings).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == '/save_csv':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
                csv_path = os.path.join(base_path, 'complex_mappings.csv')
                
                with open(csv_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Client Column', 'Selected Signal', 'Relationship Logic', 'Is Selected'])
                    for item in data:
                        writer.writerow([
                            item.get('clientCol'),
                            item.get('selectedSignal'),
                            item.get('logic'),
                            item.get('isSelected')
                        ])
                
                self._set_headers()
                self.wfile.write(json.dumps({"message": "CSV saved successfully", "path": csv_path}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run(port=8004):
    print(f'Starting Mapping Backend on port {port}...')
    HTTPServer(('', port), RequestHandler).serve_forever()

if __name__ == '__main__':
    run()
