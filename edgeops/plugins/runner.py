"""One plugin invocation per disposable process; stdout is a JSON protocol."""

import importlib.util
import json
import sys

from ..domain.validation import bounded_json


def main():
    try:
        module_path, function = sys.argv[1:]
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise ValueError("plugin input exceeds 65536 bytes")
        request = json.loads(raw.decode("utf-8"))
        spec = importlib.util.spec_from_file_location("edgeops_operator_plugin", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = getattr(module, function)(request)
        sys.stdout.buffer.write(bounded_json(result).encode("utf-8"))
        return 0
    except Exception as exc:
        sys.stderr.buffer.write(f"{type(exc).__name__}: {exc}".encode("utf-8", errors="replace"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
