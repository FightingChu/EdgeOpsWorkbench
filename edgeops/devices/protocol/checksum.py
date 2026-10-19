"""Checksums used by the device wire format."""

import zlib


def crc32(data):
    if not isinstance(data, bytes):
        raise TypeError("checksum input must be bytes")
    return zlib.crc32(data) & 0xffffffff
