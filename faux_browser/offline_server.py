#!/usr/bin/env python3
"""Offline HTTP server that serves cached pages and placeholder messages."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
import argparse
import os


class OfflineHandler(SimpleHTTPRequestHandler):
    """Serve files from repo and inject a placeholder when missing."""

    placeholder = (
        "<html><body><h1>Content unavailable</h1>"
        "<p>No cached copy for {path}</p></body></html>"
    )
    log_path: Path

    def _log_access(self) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with self.log_path.open("a", encoding="utf-8") as log:
            log.write(f"{timestamp} {self.path}\n")

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
        self._log_access()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve cached pages from repository")
    parser.add_argument("--repo", default="repository", help="Path to local repository")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        raise SystemExit(f"Repository path {repo_path} does not exist")

    log_dir = repo_path / "metadata"
    log_dir.mkdir(parents=True, exist_ok=True)
    OfflineHandler.log_path = log_dir / "server_access.log"

    os.chdir(repo_path)
    httpd = HTTPServer(("localhost", args.port), OfflineHandler)
    print(f"Serving {repo_path} on http://localhost:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    main()
