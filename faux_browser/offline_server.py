#!/usr/bin/env python3
"""Offline HTTP server that serves cached pages and placeholder messages."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
from hashlib import sha256


class OfflineHandler(SimpleHTTPRequestHandler):
    """Serve files from repo and inject a placeholder when missing."""

    placeholder = (
        "<html><body><h1>Content unavailable</h1>"
        "<p>No cached copy for {path}</p></body></html>"
    )
    log_path: Path
    allowed_domains: set[str]
    soft_allow_domains: set[str]
    blocked_domains: set[str]
    manifest: dict[str, dict]
    session_limit: int | None
    session_start: datetime

    def _verify_hash(self, file_path: Path) -> bool:
        rel = str(file_path.relative_to(Path.cwd()))
        entry = self.manifest.get(rel)
        if not entry:
            return True
        h = sha256()
        with file_path.open('rb') as fh:
            for chunk in iter(lambda: fh.read(8192), b''):
                h.update(chunk)
        return h.hexdigest() == entry.get('sha256')

    def _log_access(self) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        with self.log_path.open("a", encoding="utf-8") as log:
            log.write(f"{timestamp} {self.path}\n")

    def do_GET(self):
        if self.session_limit is not None:
            now = datetime.now(timezone.utc)
            elapsed = (now - self.session_start).total_seconds() / 60
            if elapsed > self.session_limit:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Time limit exceeded")
                self._log_access()
                return
        path = self.translate_path(self.path)
        domain = (
            Path(self.path).parts[1]
            if self.path.startswith('/pages/') and len(Path(self.path).parts) > 1
            else ''
        )
        if domain in self.blocked_domains:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Blocked domain")
        elif domain and domain not in self.allowed_domains:
            self.send_response(403)
            self.end_headers()
            if domain in self.soft_allow_domains:
                self.wfile.write(b"Approval required")
            else:
                self.wfile.write(b"Access denied")
        elif Path(path).exists():
            file_ok = self._verify_hash(Path(path))
            if not file_ok:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Checksum mismatch")
            else:
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
    parser.add_argument("--profile", default="profiles/default.json", help="User profile JSON")
    parser.add_argument("--verify", action="store_true", help="Verify file hashes from manifest")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    if not repo_path.exists():
        raise SystemExit(f"Repository path {repo_path} does not exist")

    log_dir = repo_path / "metadata"
    log_dir.mkdir(parents=True, exist_ok=True)
    OfflineHandler.log_path = log_dir / "server_access.log"

    manifest_path = repo_path / "manifest.json"
    if args.verify and manifest_path.exists():
        OfflineHandler.manifest = json.loads(manifest_path.read_text())
    else:
        OfflineHandler.manifest = {}

    profile_path = Path(args.profile)
    if profile_path.exists():
        profile = json.loads(profile_path.read_text())
        OfflineHandler.allowed_domains = set(profile.get("allowed_domains", []))
        OfflineHandler.soft_allow_domains = set(profile.get("soft_allow_domains", []))
        OfflineHandler.blocked_domains = set(profile.get("blocked_domains", []))
        OfflineHandler.session_limit = profile.get("time_limit_minutes")
    else:
        OfflineHandler.allowed_domains = set()
        OfflineHandler.soft_allow_domains = set()
        OfflineHandler.blocked_domains = set()
        OfflineHandler.session_limit = None
    OfflineHandler.session_start = datetime.now(timezone.utc)

    os.chdir(repo_path)
    httpd = HTTPServer(("localhost", args.port), OfflineHandler)
    print(f"Serving {repo_path} on http://localhost:{args.port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    main()
