"""Local web UI for PlainRay (stdlib http.server - no frameworks).

Serves static/index.html and one POST endpoint /api/explain.
Binds to 127.0.0.1 only on purpose: this tool is meant for the
clinic's own machine, not a public server.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .app import explain

STATIC = Path(__file__).resolve().parent.parent / "static"
MAX_BODY = 200_000


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, (STATIC / "index.html").read_bytes())
        elif path == "/health":
            self._send(200, json.dumps({"ok": True, "model": "local"}).encode(), "application/json")
        else:
            self._send(404, b"not found")

    def do_POST(self):
        if self.path.split("?")[0] != "/api/explain":
            self._send(404, b"not found", "application/json")
            return
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY:
            self._send(413, b'{"error": "report too long"}', "application/json")
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            report = str(payload.get("report", ""))
            result = explain(report)
            self._send(200, json.dumps(result).encode("utf-8", "replace"), "application/json")
        except Exception as exc:  # noqa: BLE001 - return the error string to the UI
            self._send(502, json.dumps({"error": str(exc)}).encode(), "application/json")

    def log_message(self, *args):  # keep PHI out of any logs
        pass


def serve(port: int = 7860):
    url = f"http://127.0.0.1:{port}"
    print(f"PlainRay running at {url}  (local only - nothing leaves this machine)")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
