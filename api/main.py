from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if auth_header:
            self.wfile.write(f"<h1>Benvenuto Pippo!</h1><p>Ho ricevuto il tuo Token: {auth_header[:20]}...</p>".encode())
        else:
            self.wfile.write(b"<h1>Alt!</h1><p>Nessun Token fornito. Accedi tramite Keycloak!</p>")

print("API in ascolto su http://localhost:8000")
httpd = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
httpd.serve_forever()