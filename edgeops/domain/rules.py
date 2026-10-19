"""Threshold rules for the bootstrap incident engine."""

from dataclasses import dataclass

from .models import TelemetryReading


@dataclass(frozen=True)
class IncidentDecision:
    fingerprint: str
    title: str
    severity: str


def evaluate_reading(reading: TelemetryReading):
    thresholds = {
        "temperature": ((85.0, "critical"), (75.0, "warning")),
        "vibration": ((8.0, "critical"), (5.0, "warning")),
    }
    if reading.metric == "battery":
        severity = "critical" if reading.value <= 10 else "warning" if reading.value <= 20 else None
    else:
        severity = None
        for threshold, candidate in thresholds.get(reading.metric, ()):
            if reading.value >= threshold:
                severity = candidate
                break
    if severity is None:
        return None
    return IncidentDecision(
        fingerprint=f"threshold:{reading.metric}:{severity}",
        title=f"{reading.metric} threshold exceeded",
        severity=severity,
    )

