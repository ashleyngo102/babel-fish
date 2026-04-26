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
            self.handle_mappings()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == '/upload':
            self.handle_upload()
        elif self.path == '/save_csv':
            self.handle_save_csv()
        elif self.path == '/run_model':
            self.handle_run_model()
        elif self.path == '/assign_value':
            self.handle_assign_value()
        elif self.path == '/save_results':
            self.handle_save_results()
        elif self.path == '/transform_data':
            self.handle_transform_data()
        elif self.path == '/generate_script':
            self.handle_generate_script()
        elif self.path == '/evaluate_data':
            self.handle_evaluate_data()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # --- Handlers ---

    def handle_mappings(self):
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

    def handle_upload(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
            file_content = data.get('file_content', '')
            
            f = io.StringIO(file_content)
            reader = csv.reader(f)
            headers = [h.strip() for h in next(reader, []) if h.strip()]
            
            all_rows = list(reader)
            total_rows = len(all_rows)
            
            # Get top 5 rows for preview
            top_5 = all_rows[:5]
                    
            self._set_headers()
            self.wfile.write(json.dumps({
                "headers": headers,
                "rows": top_5,
                "total_rows": total_rows
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_save_csv(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
            base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
            csv_path = os.path.join(base_path, 'complex_mappings.csv')
            
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Client Column', 'Selected Signal', 'Relationship Logic', 'Is Selected', 'Original Column'])
                for item in data:
                    writer.writerow([
                        item.get('clientCol'),
                        item.get('selectedSignal'),
                        item.get('logic'),
                        item.get('isSelected'),
                        item.get('originalCol')
                    ])
            
            self._set_headers()
            self.wfile.write(json.dumps({"message": "CSV saved successfully", "path": csv_path}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_run_model(self):
        try:
            base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
            csv_path = os.path.join(base_path, 'transformed_data.csv')
            
            # Read mappings to identify columns
            mappings_path = os.path.join(base_path, 'complex_mappings.csv')
            location_col = 'location'
            credit_col = 'credit_score'
            
            if os.path.exists(mappings_path):
                with open(mappings_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Is Selected') == 'True':
                            sig = row.get('Selected Signal')
                            orig = row.get('Original Column', row.get('Client Column'))
                            
                            if sig == 'City_id' or orig == 'location':
                                location_col = sig if sig != 'Select mapping...' else orig
                            elif orig == 'credit_score':
                                credit_col = sig if sig != 'Undetected' else orig
            
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
                    location_col: loc,
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

    def handle_assign_value(self):
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

    def handle_save_results(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Results received successfully"}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_transform_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
            csv_path = os.path.join(base_path, 'Translation 2 - sample dataset-v1_generated_200.csv')
            out_path = os.path.join(base_path, 'transformed_data.csv')
            
            with open(csv_path, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                rows = list(reader)
            
            header_map = {}
            for item in req_data:
                orig = item.get('originalCol')
                new_name = item.get('clientCol')
                if orig and new_name:
                    header_map[orig.strip()] = new_name.strip()
            
            new_headers = []
            for h in headers:
                clean_h = h.strip()
                if clean_h in header_map:
                    new_headers.append(header_map[clean_h])
                else:
                    new_headers.append(clean_h)
            
            with open(out_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(new_headers)
                writer.writerows(rows)
            
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Data transformed successfully", "path": out_path}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_generate_script(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            
            base_path = "/Users/aaliakhnovich/Downloads/repo/babel-fish-main"
            mappings_path = os.path.join(base_path, 'complex_mappings.csv')
            
            signal_name = 'location'
            if os.path.exists(mappings_path):
                with open(mappings_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Is Selected') == 'True':
                            signal_name = row.get('Client Column')
                            break
            
            # Ensure signal_name is lowercase to match grammar tokens
            signal_name = signal_name.lower() if signal_name else 'city_id'
            
            script = f"""# BABEL FISH AI GENERATED LOGIC

# Custom variables must start with an underscore
_scores = {json.dumps(req_data, indent=4)}

if {signal_name} in _scores:
    return float(_scores[{signal_name}])

return 0.0
"""
            
            self._set_headers()
            self.wfile.write(json.dumps({"script": script}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def handle_evaluate_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            source = req_data.get('source')
            file_content = req_data.get('file_content', '')
            
            f = io.StringIO(file_content)
            reader = csv.reader(f)
            headers = [h.strip() for h in next(reader, []) if h.strip()]
            
            errors = []
            warnings = []
            notes = []
            passed = []
            
            reasons = {
                'Order ID': "Prevents duplicate uploads from being counted multiple times.",
                'Conversion Value': "Provides value signal for bidding.",
                'Conversion Currency': "Required if value is provided.",
                'Consent': "Recommended for privacy compliance.",
                'User IP Address': "Captures full breadth of measurement when attribution becomes available.",
                'Session Attributes': "Enables Google Ads to more accurately attribute conversions.",
                'Braid': "Maintains conversion reporting when GCLID is unavailable.",
                'revenue': "Monetary value associated with conversion.",
                'customVariables': "Allows custom data passing."
            }
            
            if source == 'data_manager':
                if 'Conversion Name' in headers:
                    passed.append("Conversion Name: Present and mapped.")
                else:
                    errors.append("Missing required field: Conversion Name")
                    
                if 'Conversion Time' in headers:
                    passed.append("Conversion Time: Present and mapped.")
                else:
                    errors.append("Missing required field: Conversion Time")
                    
                identifiers = ['Email', 'Phone Number', 'First Name', 'gclid']
                has_id = any(id in headers for id in identifiers)
                if has_id:
                    passed.append("Identifier: At least one user identifier is present.")
                else:
                    errors.append("Missing at least one required identifier (Email, Phone Number, First Name, or gclid)")
                    
                recommended = ['Order ID', 'Conversion Value', 'Conversion Currency', 'Consent', 'User IP Address', 'Session Attributes', 'Braid']
                for rec in recommended:
                    if rec not in headers:
                        warnings.append({
                            "field": rec,
                            "reason": reasons.get(rec, "Recommended for better performance.")
                        })
                    else:
                        passed.append(f"{rec}: Optional field present.")
                        
                if 'floodlightConfigurationId' in headers or 'floodlightActivityId' in headers:
                    notes.append("It looks like you uploaded a Campaign Manager (OCI) file while Data Manager was selected. Please verify your selection.")
                        
            elif source == 'campaign_manager':
                required = ['floodlightConfigurationId', 'floodlightActivityId', 'timestampMicros', 'ordinal', 'quantity']
                for req in required:
                    if req in headers:
                        passed.append(f"{req}: Core required field present.")
                    else:
                        errors.append(f"Missing core required field: {req}")
                        
                identifiers = ['encryptedUserId', 'mobileDeviceId', 'gclid', 'dclid', 'matchId', 'impressionId', 'session_attributes']
                has_id = any(id in headers for id in identifiers)
                if has_id:
                    passed.append("Identifier: At least one identifier field is present.")
                else:
                    errors.append("Missing at least one required identifier field")
                    
                recommended = ['revenue', 'customVariables']
                for rec in recommended:
                    if rec not in headers:
                        warnings.append({
                            "field": rec,
                            "reason": reasons.get(rec, "Recommended for better performance.")
                        })
                    else:
                        passed.append(f"{rec}: Optional field present.")
                        
                if 'Conversion Name' in headers:
                    notes.append("It looks like you uploaded a Data Manager file while Campaign Manager was selected. Please verify your selection.")
            else:
                raise ValueError(f"Unknown source: {source}")
                
            self._set_headers()
            self.wfile.write(json.dumps({
                "errors": errors,
                "warnings": warnings,
                "notes": notes,
                "passed": passed,
                "compliance_score": 100 - len(errors) * 10
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run(port=8006):
    print(f'Starting Consolidated Backend on port {port}...')
    HTTPServer(('', port), RequestHandler).serve_forever()

if __name__ == '__main__':
    run()
