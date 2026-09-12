from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
r=Path(__file__).parent
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  with (r/'requests.log').open('a') as f:f.write(self.path+'\n')
  path=r/'candidate-v2.pdf' if self.path=='/candidate-v2.pdf' else r/'candidate-v1.pdf' if self.path=='/current.pdf' else None
  if path and path.exists():
   self.send_response(200);self.send_header('Content-Type','application/pdf');self.end_headers();self.wfile.write(path.read_bytes())
  else:self.send_response(503);self.end_headers();self.wfile.write(b'Fixture storage unavailable')
HTTPServer(('127.0.0.1',18768),Handler).serve_forever()
