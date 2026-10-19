"""Security reports omit secrets while preserving check identity and result."""

from dataclasses import asdict

from ..media.redaction import redact_metadata


def redact_report(findings, context=None):
    return {"findings": [asdict(finding) for finding in findings], "context": redact_metadata(context or {})}
