"""Subprocess plugin calls exchange bounded JSON and hold no database transaction."""

from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys

from ..domain.plugins import PluginManifest
from ..domain.validation import bounded_json, integer


class PluginHost:
    def __init__(self):
        self.entries = {}

    def load(self, directory):
        root = Path(directory).resolve()
        path = root / "plugin.json"
        if path.stat().st_size > 16384:
            raise ValueError("plugin manifest exceeds 16384 bytes")
        manifest = PluginManifest.parse(json.loads(path.read_text(encoding="utf-8")))
        filename, function = manifest.entrypoint.split(":")
        module = (root / filename).resolve()
        if module.parent != root or not module.is_file():
            raise ValueError("plugin module must exist within the plugin directory")
        if manifest.name in self.entries:
            raise ValueError("duplicate plugin name: " + manifest.name)
        self.entries[manifest.name] = (manifest, module, function)
        return asdict(manifest)

    def manifests(self):
        return [asdict(self.entries[name][0]) for name in sorted(self.entries)]

    def invoke(self, name, request, timeout=5):
        integer(timeout, "timeout", 1, 30)
        if name not in self.entries:
            raise ValueError("plugin is not loaded: " + str(name))
        payload = bounded_json(request).encode("utf-8")
        manifest, module, function = self.entries[name]
        try:
            result = subprocess.run(
                [sys.executable, "-m", "edgeops.plugins.runner", str(module), function],
                input=payload, capture_output=True, timeout=timeout,
                cwd=Path(__file__).resolve().parents[2],
            )
        except subprocess.TimeoutExpired:
            raise ValueError("plugin execution timed out") from None
        if result.returncode:
            raise ValueError("plugin failed: " + result.stderr[:2048].decode("utf-8", errors="replace"))
        if len(result.stdout) > 65536:
            raise ValueError("plugin output exceeds 65536 bytes")
        try:
            value = json.loads(result.stdout.decode("utf-8"))
            bounded_json(value)
        except (ValueError, UnicodeError):
            raise ValueError("plugin returned invalid JSON") from None
        return value
