from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"\n--- [GET Заявка] --- Path: {self.path}")
        print(f"Headers:\n{self.headers}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        print(f"\n--- [POST Заявка] --- Path: {self.path}")
        print(f"Headers:\n{self.headers}")
        print(f"Body:\n{body}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

print("Сървърът е стартиран на порт 8080...")
HTTPServer(('0.0.0.0', 8080), RequestHandler).serve_forever()
