"""Authorized local configuration checks return stable, machine-readable findings."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str
    passed: bool
    detail: str


def audit_settings(settings):
    return [Finding("local-bind", "critical", settings.host in {"127.0.0.1", "localhost"}, "service host is local-only"),
            Finding("port-range", "warning", 1 <= settings.port <= 65535, "port is in the TCP range"),
            Finding("database-name", "warning", "/" not in settings.database_name and "\\" not in settings.database_name, "database name has no path separators")]


def audit_headers(headers):
    if not isinstance(headers, dict):
        raise ValueError("headers must be a mapping")
    required = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer"}
    return [Finding("header:" + key, "warning", headers.get(key) == value, f"expected {value}") for key, value in required.items()]
