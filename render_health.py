"""
Tiny HTTP health-check server for Render.
Render requires a service to bind PORT to stay alive.
Run this in background thread from __main__.py
"""
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from config import PORT


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK - MusicBot Running")

    def log_message(self, *args):
        pass  # silence access logs


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), _Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print(f"[HealthServer] Listening on port {PORT}")
