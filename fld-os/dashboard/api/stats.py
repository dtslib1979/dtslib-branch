#!/usr/bin/env python3
"""FLD OS — Stats API proxy for dashboard"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from http.server import HTTPServer, BaseHTTPRequestHandler
from mcp_tools import handle_mcp_call

PORT = int(os.environ.get("FLD_API_PORT", 8091))

class StatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if self.path == "/stats":
            result = handle_mcp_call("fld_stats")
        else:
            result = handle_mcp_call("fld_list", {"state": self.path.strip("/")})
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass

HTTPServer(("0.0.0.0", PORT), StatsHandler).serve_forever()
