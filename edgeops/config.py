"""Configuration loading with explicit keys and local-only defaults."""

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    host: str = "127.0.0.1"
    port: int = 8877
    data_dir: Path = Path("data")
    database_name: str = "edgeops.sqlite3"

    @property
    def database_path(self):
        return self.data_dir / self.database_name


def load_settings(config_path=None, *, host=None, port=None, data_dir=None):
    path = Path(config_path) if config_path else Path("config.local.json")
    values = {}
    if path.exists():
        parsed = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError("configuration must be a JSON object")
        unknown = set(parsed) - {"host", "port", "data_dir", "database_name"}
        if unknown:
            raise ValueError("unknown configuration keys: " + ", ".join(sorted(unknown)))
        values.update(parsed)
    if host is not None:
        values["host"] = host
    if port is not None:
        values["port"] = port
    if data_dir is not None:
        values["data_dir"] = data_dir
    settings = Settings(
        host=str(values.get("host", "127.0.0.1")),
        port=int(values.get("port", 8877)),
        data_dir=Path(values.get("data_dir", "data")),
        database_name=str(values.get("database_name", "edgeops.sqlite3")),
    )
    if settings.host not in {"127.0.0.1", "localhost"}:
        raise ValueError("the bootstrap server only accepts a local host")
    if not 1 <= settings.port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    if Path(settings.database_name).name != settings.database_name:
        raise ValueError("database_name must be a filename")
    return settings

