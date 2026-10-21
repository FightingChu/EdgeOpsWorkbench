"""Standard-library HTTP client for the local JSON API."""

import json
from urllib.request import Request, urlopen


def get_json(base_url, path, timeout=5):
    if not base_url.startswith("http://127.0.0.1:"):
        raise ValueError("client only permits loopback HTTP")
    with urlopen(Request(base_url.rstrip("/") + path, headers={"Accept": "application/json"}), timeout=timeout) as response:
        body = json.loads(response.read())
        if response.status != 200:
            raise ValueError(body.get("error", "HTTP request failed"))
        return body
