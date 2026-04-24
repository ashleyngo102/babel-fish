from http.server import HTTPServer, BaseHTTPRequestHandler
import csv
import io
import json
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

    def do_POST(self):
        if self.path == '/run_model':
            try:
                base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
                csv_path = os.path.join(base_path, 'Translation 2 - sample dataset-v1_generated_200.csv')
                
                # Read mappings to identify columns
                mappings_path = os.path.join(base_path, 'complex_mappings.csv')
                location_col = 'location'
                credit_col = 'credit_score'
                
                if os.path.exists(mappings_path):
                    with open(mappings_path, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if row.get('Is Selected') == 'True':
                                if row.get('Client Column') == 'location':
                                    location_col = 'location'
                                elif row.get('Client Column') == 'credit_score':
                                    credit_col = 'credit_score'
                
                # Read data
                data = []
                with open(csv_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
                        data.append(clean_row)
                
                # Group by location
                location_data = {}
                for row in data:
                    loc = row.get(location_col, 'Unknown')
                    try:
                        score = float(row.get(credit_col, 0))
                    except ValueError:
                        score = 0
                        
                    if loc not in location_data:
                        location_data[loc] = {"total_users": 0, "scores": [], "high_scores": []}
                    
                    location_data[loc]["total_users"] += 1
                    location_data[loc]["scores"].append(score)
                    if score >= 750:
                        location_data[loc]["high_scores"].append(score)
                
                # Calculate metrics
                summary = []
                for loc, d in location_data.items():
                    total = d["total_users"]
                    high_count = len(d["high_scores"])
                    percentage = (high_count / total) * 100 if total > 0 else 0
                    
                    if d["high_scores"]:
                        sorted_high = sorted(d["high_scores"])
                        n = len(sorted_high)
                        if n % 2 == 1:
                            median = sorted_high[n//2]
                        else:
                            median = (sorted_high[n//2 - 1] + sorted_high[n//2]) / 2
                    else:
                        median = 0
                        
                    summary.append({
                        "location": loc,
                        "total_users": total,
                        "high_score_count": high_count,
                        "percentage_high_scores": percentage,
                        "median_score_of_top_tier": median
                    })
                
                # Normalization (Min-Max)
                def get_min_max(key):
                    vals = [x[key] for x in summary]
                    return min(vals), max(vals)
                
                min_count, max_count = get_min_max("high_score_count")
                min_perc, max_perc = get_min_max("percentage_high_scores")
                min_med, max_med = get_min_max("median_score_of_top_tier")
                
                weights = {'percentage': 0.5, 'count': 0.3, 'median_score': 0.2}
                
                for x in summary:
                    norm_count = (x["high_score_count"] - min_count) / (max_count - min_count) if max_count > min_count else 0
                    norm_perc = (x["percentage_high_scores"] - min_perc) / (max_perc - min_perc) if max_perc > min_perc else 0
                    norm_med = (x["median_score_of_top_tier"] - min_med) / (max_med - min_med) if max_med > min_med else 0
                    
                    x["value_score"] = (norm_perc * weights['percentage'] + 
                                        norm_count * weights['count'] + 
                                        norm_med * weights['median_score'])
                
                # Scale to 0-100
                min_score = min([x["value_score"] for x in summary])
                max_score = max([x["value_score"] for x in summary])
                
                for x in summary:
                    x["dma_value_100"] = ((x["value_score"] - min_score) / (max_score - min_score)) * 100 if max_score > min_score else 0
                    x["dma_value_100"] = round(x["dma_value_100"], 2)
                    x["percentage_high_scores"] = round(x["percentage_high_scores"], 2)
                
                # Sort by score
                summary.sort(key=lambda x: x["dma_value_100"], reverse=True)
                
                self._set_headers()
                self.wfile.write(json.dumps(summary).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif self.path == '/assign_value':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                req_data = json.loads(post_data.decode('utf-8'))
                approach = req_data.get('approach')
                data = req_data.get('data', [])
                
                if approach == 'min-max':
                    result = data
                elif approach == 'quantile':
                    ranked = [x for x in data if x.get('dma_value_100', 0) > 0]
                    unranked = [x for x in data if x.get('dma_value_100', 0) == 0]
                    
                    ranked.sort(key=lambda x: x.get('dma_value_100', 0))
                    n = len(ranked)
                    labels = ['Bronze', 'Silver', 'Gold', 'Platinum']
                    
                    binned = []
                    for index, x in enumerate(ranked):
                        q = int((index / n) * 4)
                        if q > 3: q = 3
                        x['dma_tier'] = labels[q]
                        binned.append(x)
                        
                    for x in unranked:
                        x['dma_tier'] = 'Unranked'
                        binned.append(x)
                        
                    binned.sort(key=lambda x: x.get('dma_value_100', 0), reverse=True)
                    result = binned
                else:
                    raise ValueError(f"Unknown approach: {approach}")
                
                self._set_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif self.path == '/save_results':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Results received successfully"}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run(port=8006):
    print(f'Starting Model Backend on port {port}...')
    HTTPServer(('', port), RequestHandler).serve_forever()

if __name__ == '__main__':
    run()
