#!/usr/bin/env python3
"""
FLD OS — MCP SSE Server
Claude Desktop 및 MCP 호스트와 통신
"""
import sys, os, json, asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
from mcp_tools import handle_mcp_call, tool_list

PORT = int(os.environ.get("FLD_MCP_PORT", 8090))

class FLDMCPHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "fld-os"}).encode())
        elif self.path == "/tools":
            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps(tool_list()).encode())
        elif self.path == "/stats":
            self.send_response(200)
            self._cors()
            self.end_headers()
            from ledger import get_ledger
            self.wfile.write(json.dumps(get_ledger().stats()).encode())
        else:
            self.send_response(404)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            req = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid json"}).encode())
            return

        tool = req.get("tool", "")
        params = req.get("params", {})
        result = handle_mcp_call(tool, params)

        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        print(f"[FLD-MCP] {args[0]} {args[1]}")

def main():
    print(f"\U0001f4e1 FLD OS MCP Server running on :{PORT}")
    print(f"   Tools: {len(tool_list()['tools'])} available")
    print(f"   Health: http://localhost:{PORT}/health")
    print(f"   Stats:  http://localhost:{PORT}/stats")
    server = HTTPServer(("0.0.0.0", PORT), FLDMCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
