# Device protocol

EOW1 frames use a fixed header, little-endian length, bounded payload, and CRC32. The parser accepts fragmented input and rejects bad magic, versions, lengths, checksums, and truncated frames.
