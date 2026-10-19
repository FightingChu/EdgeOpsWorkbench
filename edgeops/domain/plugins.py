"""Versioned plugin manifest validation with explicit declared capabilities."""

from dataclasses import dataclass
import re


CAPABILITIES = {"importer": {"events.decode"}, "exporter": {"events.encode"},
                "rule": {"events.evaluate"}, "diagnostic": {"data.summarize"}}


@dataclass(frozen=True)
class PluginManifest:
    name: str
    kind: str
    entrypoint: str
    capabilities: tuple
    description: str
    version: int = 1

    @classmethod
    def parse(cls, value):
        required = {"name", "kind", "entrypoint", "capabilities", "description", "version"}
        if not isinstance(value, dict) or set(value) != required:
            raise ValueError("plugin manifest fields do not match version 1")
        if type(value["version"]) is not int or value["version"] != 1:
            raise ValueError("unsupported plugin version")
        if not isinstance(value["name"], str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value["name"]):
            raise ValueError("invalid plugin name")
        if not isinstance(value["kind"], str) or value["kind"] not in CAPABILITIES:
            raise ValueError("unsupported plugin kind")
        if not isinstance(value["entrypoint"], str) or not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*\.py:[a-zA-Z_][a-zA-Z0-9_]*", value["entrypoint"]):
            raise ValueError("entrypoint must be a local module.py:function")
        caps = value["capabilities"]
        if not isinstance(caps, list) or not all(isinstance(cap, str) for cap in caps) or set(caps) != CAPABILITIES[value["kind"]] or len(caps) != len(set(caps)):
            raise ValueError("plugin capabilities do not match kind")
        description = value["description"]
        if not isinstance(description, str) or not 1 <= len(description) <= 512:
            raise ValueError("plugin description must contain 1-512 characters")
        return cls(value["name"], value["kind"], value["entrypoint"], tuple(caps), description)
