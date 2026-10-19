"""Deterministic bootstrap data for local demonstrations and tests."""

from datetime import datetime, timedelta, timezone

from ..domain import Device, TelemetryReading


DEMO_DEVICES = (
    Device("press-01", "Assembly Press 01", "press"),
    Device("gateway-01", "North Gateway", "gateway"),
    Device("camera-01", "Inspection Camera 01", "camera"),
)

DEMO_READINGS = (
    ("press-01", "temperature", 68.0, "C"),
    ("press-01", "vibration", 5.7, "mm/s"),
    ("gateway-01", "battery", 18.0, "%"),
    ("camera-01", "temperature", 87.0, "C"),
    ("press-01", "temperature", 78.0, "C"),
)


def load_demo(service, start=None):
    start = start or datetime.now(timezone.utc).replace(microsecond=0)
    for device in DEMO_DEVICES:
        service.register_device(device)
    for offset, (device_id, metric, value, unit) in enumerate(DEMO_READINGS):
        service.ingest(TelemetryReading(
            device_id=device_id,
            metric=metric,
            value=value,
            unit=unit,
            recorded_at=(start + timedelta(seconds=offset)).isoformat(),
        ))
    return service.summary()

