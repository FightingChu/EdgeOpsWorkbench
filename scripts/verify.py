"""Independent project verification using an isolated data directory."""

from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from edgeops.application import OperationsService
from edgeops.application.jobs import JobService
from edgeops.application.workflows import WorkflowService
from edgeops.application.analytics import AnalyticsService
from edgeops.application.alerting import AlertingService
from edgeops.application.configuration import ConfigurationService
from edgeops.application.interchange import InterchangeService
from edgeops.application.exports import ExportService
from edgeops.application.deployments import DeploymentService
from edgeops.codecs.ndjson import decode as decode_events
from edgeops.benchmark import list_cases
from edgeops.devices import load_demo
from edgeops.devices.protocol import FrameParser, decode_message, encode_frame
from edgeops.devices.protocol.messages import ReadingMessage, encode_message
from edgeops.domain import TelemetryReading
from edgeops.domain.event_query import EventQuery
from edgeops.domain.jobs import JobRequest


def main():
    with tempfile.TemporaryDirectory(prefix="edgeops-verify-") as directory:
        service = OperationsService(Path(directory) / "verify.sqlite3")
        summary = load_demo(service, datetime(2026, 10, 19, tzinfo=timezone.utc))
        expected = {"devices": 3, "telemetry": 5, "open_incidents": 4, "critical_incidents": 1}
        if summary != expected:
            raise SystemExit(f"summary mismatch: expected {expected}, received {summary}")
        if len(service.list_devices()) != 3 or len(service.list_incidents()) != 4:
            raise SystemExit("detail counts do not match the summary")
        fixture = ROOT / "fixtures" / "demo_events.jsonl"
        imported = service.import_events(fixture)
        if imported["inserted_count"] != 3 or service.list_events(EventQuery(limit=10))["events"][0]["message"] != "inspection frame delayed":
            raise SystemExit("event ingestion verification failed")
        clock = [1000.0]
        jobs = JobService(service, clock=lambda: clock[0])
        job_id = jobs.enqueue(JobRequest("health.snapshot"))
        result = jobs.work_once()
        if result is None or result["id"] != job_id or result["status"] != "succeeded":
            raise SystemExit("job verification failed")
        workflows = WorkflowService(service, clock=lambda: clock[0])
        definition = {"version": 1, "name": "verify", "steps": [{"id": "summary", "action": "summary", "params": {}}]}
        run = workflows.resume(workflows.start(definition))
        if run["status"] != "succeeded":
            raise SystemExit("workflow verification failed")
        reading = TelemetryReading("press-01", "temperature", 70, "C", "2026-10-19T00:00:00+00:00")
        parser = FrameParser()
        frames = parser.feed(encode_frame(encode_message(ReadingMessage(reading, 1))))
        if len(frames) != 1 or decode_message(frames[0]).reading != reading:
            raise SystemExit("protocol verification failed")
        if len(list_cases(ROOT)) != 18:
            raise SystemExit("case catalog verification failed")
        report = AnalyticsService(service).report("temperature", "press-01")
        if report["count"] != 2 or report["series"][0]["statistics"]["mean"] != 73:
            raise SystemExit("telemetry analytics verification failed")
        rules = [{"version": 1, "id": "event-errors", "severity": "critical",
                  "condition": {"field": "severity", "op": "severity", "value": "error"},
                  "group_by": ["device_id"]}]
        if len(AlertingService(service).evaluate(rules)["matches"]) != 1:
            raise SystemExit("alert evaluation verification failed")
        exported = Path(directory) / "events.ndjson"
        if ExportService(service).export(exported)["records"] != 3:
            raise SystemExit("event export verification failed")
        csv_file = Path(directory) / "events.csv"
        InterchangeService().convert(exported, csv_file, "ndjson", "csv")
        if len(InterchangeService().read(csv_file, "csv")) != 3:
            raise SystemExit("event format roundtrip verification failed")
        if ConfigurationService().inspect(overrides={"port": 9000})["port"] != 9000:
            raise SystemExit("layered configuration verification failed")
        firmware = Path(directory) / "firmware.bin"
        firmware.write_bytes(b"edgeops-verification-firmware")
        deployments = DeploymentService(service)
        artifact = deployments.register(firmware, "1.0.0")
        deployment = deployments.create("press-01", artifact["id"])
        result = deployments.run_simulation(deployment["id"], firmware)
        if result["state"] != "succeeded" or len(result["history"]) != 4:
            raise SystemExit("durable deployment verification failed")
    print("Project verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
