#!/usr/bin/env python3
"""Minimal offline HTTP server for the faux browser."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve cached pages from repository")
    parser.add_argument("--repo", default="repository", help="Path to local repository")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        raise SystemExit(f"Repository path {repo_path} does not exist")

    os.chdir(repo_path)
    httpd = HTTPServer(("localhost", args.port), SimpleHTTPRequestHandler)
    print(f"Serving {repo_path} on http://localhost:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    main()
