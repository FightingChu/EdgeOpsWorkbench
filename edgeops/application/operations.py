"""Use cases for device registration, telemetry ingestion, and queries."""

from ..domain import Device, TelemetryReading, evaluate_reading
from ..persistence import Database
from ..persistence.repositories import OperationsRepository
from ..persistence.events import EventRepository
from ..domain.event_query import EventQuery
from .event_import import parse_event_file
from ..persistence.audit import record


class OperationsService:
    def __init__(self, database_path):
        self.database = Database(database_path)

    def initialize(self):
        self.database.initialize()

    def register_device(self, device):
        if not isinstance(device, Device):
            raise TypeError("device must be a Device")
        self.initialize()
        with self.database.connect() as connection:
            OperationsRepository.register_device(connection, device)
            record(connection, "device.register", device.id, {"name": device.name, "kind": device.kind})

    def ingest(self, reading):
        if not isinstance(reading, TelemetryReading):
            raise TypeError("reading must be a TelemetryReading")
        self.initialize()
        with self.database.connect() as connection:
            reading_id = OperationsRepository.ingest(connection, reading, evaluate_reading(reading))
            record(connection, "telemetry.ingest", reading_id, {"device_id": reading.device_id, "metric": reading.metric})
            return reading_id

    def summary(self):
        self.initialize()
        with self.database.connect() as connection:
            return OperationsRepository.summary(connection)

    def list_devices(self):
        self.initialize()
        with self.database.connect() as connection:
            return OperationsRepository.devices(connection)

    def list_incidents(self):
        self.initialize()
        with self.database.connect() as connection:
            return OperationsRepository.incidents(connection)

    def recent_telemetry(self, limit=50):
        self.initialize()
        with self.database.connect() as connection:
            return OperationsRepository.telemetry(connection, limit)

    def import_events(self, path, *, format="jsonl", encoding="utf-8"):
        parsed = parse_event_file(path, format=format, encoding=encoding)
        self.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            result = EventRepository.import_file(connection, parsed)
            record(connection, "events.import", result["id"], {
                "sha256": result["sha256"], "records": result["record_count"],
                "inserted": result["inserted_count"], "duplicates": result["duplicate_count"],
            })
            return result

    def list_events(self, query=None):
        query = query if query is not None else EventQuery()
        if not isinstance(query, EventQuery):
            raise TypeError("query must be an EventQuery")
        self.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN")
            return EventRepository.page(connection, query)

    def event_filters(self):
        self.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN")
            return EventRepository.filters(connection)

    def incident_detail(self, incident_id):
        if type(incident_id) is not int or not 1 <= incident_id <= 9223372036854775807:
            raise ValueError("incident id must be a positive integer")
        self.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN")
            incident = OperationsRepository.incident(connection, incident_id)
            if incident is None:
                return None
            return {
                "incident": incident,
                "telemetry": OperationsRepository.incident_telemetry(connection, incident, 20),
                "events": EventRepository.page(
                    connection, EventQuery(device_id=incident["device_id"], limit=20)
                )["events"],
            }
