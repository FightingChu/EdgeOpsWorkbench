# EOW1 protocol

Frames use a four-byte `EOW1` marker, version, message type, little-endian payload length, UTF-8 JSON payload, and CRC32 over the header plus payload. The parser is incremental and rejects unknown versions, oversize payloads, checksum mismatches, and trailing partial frames. Device adapters own transport and delivery retries; this package only validates bytes and converts readings.
