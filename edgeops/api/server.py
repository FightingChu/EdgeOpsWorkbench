"""Read-only local HTTP API and static dashboard."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .. import __version__
from ..application import OperationsService
from ..domain.event_query import EventQuery


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def make_server(settings):
    service = OperationsService(settings.database_path)
    service.initialize()

    class Handler(BaseHTTPRequestHandler):
        server_version = "EdgeOps/" + __version__
        sys_version = ""

        def log_message(self, format, *args):
            return

        def respond(self, status, body, content_type="application/json; charset=utf-8"):
            if not isinstance(body, bytes):
                body = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; "
                "img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            )
            self.end_headers()
            self.wfile.write(body)

        def trusted_host(self):
            port = self.server.server_address[1]
            return self.headers.get("Host", "").lower() in {f"127.0.0.1:{port}", f"localhost:{port}"}

        def do_GET(self):
            if not self.trusted_host():
                self.respond(403, {"error": "local requests only"})
                return
            parsed = urlsplit(self.path)
            try:
                if len(self.path) > 8192:
                    raise ValueError("request target exceeds 8192 characters")
                if parsed.path == "/api/health":
                    self.respond(200, {"status": "ok", "version": __version__})
                elif parsed.path == "/api/summary":
                    self.respond(200, service.summary())
                elif parsed.path == "/api/devices":
                    self.respond(200, {"devices": service.list_devices()})
                elif parsed.path == "/api/incidents":
                    self.respond(200, {"incidents": service.list_incidents()})
                elif parsed.path.startswith("/api/incidents/"):
                    raw_id = parsed.path.removeprefix("/api/incidents/")
                    if not raw_id.isascii() or not raw_id.isdecimal() or len(raw_id) > 19:
                        raise ValueError("incident id must be a positive integer")
                    detail = service.incident_detail(int(raw_id))
                    self.respond(200 if detail else 404, detail or {"error": "incident not found"})
                elif parsed.path == "/api/events/filters":
                    if parsed.query:
                        raise ValueError("event filters endpoint does not accept parameters")
                    self.respond(200, service.event_filters())
                elif parsed.path == "/api/events":
                    params = parse_qs(parsed.query, keep_blank_values=True, max_num_fields=16,
                                      encoding="utf-8", errors="strict")
                    allowed = {"limit", "cursor", "q", "severity", "service", "device_id", "since", "until"}
                    if set(params) - allowed or any(len(values) != 1 for values in params.values()):
                        raise ValueError("unknown or repeated event query parameter")
                    values = {key: items[0] for key, items in params.items()}
                    if "limit" in values:
                        value = values["limit"]
                        if not value.isascii() or not value.isdecimal() or len(value) > 3:
                            raise ValueError("limit must be an integer between 1 and 200")
                        values["limit"] = int(value)
                    self.respond(200, service.list_events(EventQuery(**values)))
                elif parsed.path == "/api/telemetry":
                    query = parse_qs(parsed.query)
                    raw_limit = query.get("limit", ["50"])
                    if len(raw_limit) != 1 or not raw_limit[0].isascii() or not raw_limit[0].isdecimal():
                        raise ValueError("limit must be a positive integer")
                    self.respond(200, {"telemetry": service.recent_telemetry(int(raw_limit[0]))})
                elif parsed.path in {"/", "/index.html", "/style.css", "/app.js", "/manifest.webmanifest", "/sw.js", "/sw-register.js"}:
                    name = "index.html" if parsed.path == "/" else parsed.path[1:]
                    mime = {"index.html": "text/html; charset=utf-8", "style.css": "text/css; charset=utf-8",
                            "app.js": "text/javascript; charset=utf-8", "manifest.webmanifest": "application/manifest+json; charset=utf-8",
                            "sw.js": "text/javascript; charset=utf-8", "sw-register.js": "text/javascript; charset=utf-8"}[name]
                    self.respond(200, (STATIC_DIR / name).read_bytes(), mime)
                else:
                    self.respond(404, {"error": "not found"})
            except (ValueError, OSError) as exc:
                self.respond(400, {"error": str(exc)})

    return ThreadingHTTPServer((settings.host, settings.port), Handler)
