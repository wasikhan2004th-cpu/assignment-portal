from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

SAVE_PATH = "testreport.json"

class ReportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/report':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            try:
                report = json.loads(body)
                with open(SAVE_PATH, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"\n✅ Report received and saved to {SAVE_PATH}")
                print(f"   Commit: {report.get('commit_sha', 'N/A')}")
                print(f"   Status: {report.get('overall_status', 'N/A')}")
                print(f"   Passed: {report.get('passed_count', 0)} / {report.get('total_count', 0)}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "saved"}).encode())
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logs

if __name__ == '__main__':
    port = 5001
    print(f"🎯 Report receiver running on http://localhost:{port}/report")
    print(f"📁 Reports will be saved to: {os.path.abspath(SAVE_PATH)}")
    print("   Press Ctrl+C to stop.\n")
    server = HTTPServer(('0.0.0.0', port), ReportHandler)
    server.serve_forever()