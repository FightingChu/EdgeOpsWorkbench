"""Client summary view model with immutable display rows."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DesktopRow:
    title: str
    value: str
    severity: str = "info"


def summary_rows(summary):
    if not isinstance(summary, dict):
        raise ValueError("summary must be an object")
    return [DesktopRow("Registered devices", str(summary.get("devices", 0))), DesktopRow("Telemetry readings", str(summary.get("telemetry", 0))), DesktopRow("Open incidents", str(summary.get("open_incidents", 0))), DesktopRow("Critical incidents", str(summary.get("critical_incidents", 0)), "critical")]
