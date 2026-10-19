"""Workflow version 1 grammar, prior-step references, and bounded resolution."""

import re

from .models import _text
from .validation import bounded_json


ACTIONS = {"emit", "assert.equal", "summary", "events.query", "plugin.invoke"}


def _walk(value, references, depth=0):
    if depth > 32:
        raise ValueError("workflow parameter nesting exceeds 32")
    if isinstance(value, dict):
        if "$ref" in value:
            if set(value) != {"$ref"} or not isinstance(value["$ref"], str):
                raise ValueError("reference must be a single $ref string")
            references.append(value["$ref"])
        else:
            for item in value.values():
                _walk(item, references, depth + 1)
    elif isinstance(value, list):
        for item in value:
            _walk(item, references, depth + 1)


def validate_workflow(value):
    bounded_json(value)
    if not isinstance(value, dict) or set(value) != {"version", "name", "steps"}:
        raise ValueError("workflow fields must be version, name, and steps")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("unsupported workflow version")
    _text(value["name"], "workflow name", 128)
    steps = value["steps"]
    if not isinstance(steps, list) or not 1 <= len(steps) <= 50:
        raise ValueError("workflow must contain 1-50 steps")
    seen = set()
    for step in steps:
        if not isinstance(step, dict) or set(step) != {"id", "action", "params"}:
            raise ValueError("step fields must be id, action, and params")
        name = step["id"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", name) or name in seen:
            raise ValueError("step id must be unique and use lowercase identifier characters")
        if not isinstance(step["action"], str) or step["action"] not in ACTIONS:
            raise ValueError("unsupported workflow action")
        if not isinstance(step["params"], dict):
            raise ValueError("step params must be an object")
        references = []
        _walk(step["params"], references)
        for reference in references:
            parts = reference.split(".")
            if not all(parts) or (parts[0] != "input" and not (len(parts) >= 2 and parts[0] == "steps" and parts[1] in seen)):
                raise ValueError("reference must address input or an earlier step")
        seen.add(name)
    return value


def resolve(value, context):
    if isinstance(value, dict):
        if "$ref" in value:
            current = context
            try:
                for part in value["$ref"].split("."):
                    if not isinstance(current, dict):
                        raise KeyError(part)
                    current = current[part]
                return current
            except KeyError:
                raise ValueError("unresolved workflow reference: " + value["$ref"]) from None
        return {key: resolve(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, context) for item in value]
    return value
