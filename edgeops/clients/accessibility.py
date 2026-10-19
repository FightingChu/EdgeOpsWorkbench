"""Accessibility checks for the static dashboard contract."""

import re


def inspect_html(html):
    if not isinstance(html, str):
        raise ValueError("html must be text")
    checks = {"lang": bool(re.search(r"<html[^>]+lang=", html, re.I)), "viewport": "name=\"viewport\"" in html, "script-src": "script-src 'self'" in html}
    return {"passed": all(checks.values()), "checks": checks}
