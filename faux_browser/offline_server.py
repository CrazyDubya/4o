#!/usr/bin/env python3
"""Offline HTTP server that serves cached pages and placeholder messages."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse
import os


class OfflineHandler(SimpleHTTPRequestHandler):
    """Serve files from repo and inject a placeholder when missing."""

    placeholder = (
        "<html><body><h1>Content unavailable</h1>"
        "<p>No cached copy for {path}</p></body></html>"
    )

    def do_GET(self):
        path = self.translate_path(self.path)
        if Path(path).exists():
            super().do_GET()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            msg = self.placeholder.format(path=self.path)
            self.wfile.write(msg.encode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve cached pages from repository")
    parser.add_argument("--repo", default="repository", help="Path to local repository")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        raise SystemExit(f"Repository path {repo_path} does not exist")

    os.chdir(repo_path)
    httpd = HTTPServer(("localhost", args.port), OfflineHandler)
    print(f"Serving {repo_path} on http://localhost:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    main()
