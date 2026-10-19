"""Incremental parser for EOW1 frames: magic, version, type, length, payload, CRC."""

from dataclasses import dataclass
import struct

from .checksum import crc32

MAGIC = b"EOW1"
VERSION = 1
HEADER = struct.Struct("<4sBBH")
TRAILER = struct.Struct("<I")
MAX_PAYLOAD = 4096


@dataclass(frozen=True)
class Frame:
    message_type: int
    payload: bytes
    version: int = VERSION

    def __post_init__(self):
        if type(self.message_type) is not int or not 0 <= self.message_type <= 255:
            raise ValueError("message_type must be a byte")
        if self.version != VERSION:
            raise ValueError("unsupported protocol version")
        if not isinstance(self.payload, bytes) or len(self.payload) > MAX_PAYLOAD:
            raise ValueError(f"payload must be at most {MAX_PAYLOAD} bytes")


def encode_frame(frame):
    if not isinstance(frame, Frame):
        raise TypeError("frame must be a Frame")
    header = HEADER.pack(MAGIC, frame.version, frame.message_type, len(frame.payload))
    return header + frame.payload + TRAILER.pack(crc32(header + frame.payload))


class FrameParser:
    def __init__(self):
        self._buffer = bytearray()

    def feed(self, data):
        if not isinstance(data, bytes):
            raise TypeError("parser input must be bytes")
        self._buffer.extend(data)
        result = []
        while True:
            if len(self._buffer) >= 4 and bytes(self._buffer[:4]) != MAGIC:
                raise ValueError("frame magic mismatch")
            if len(self._buffer) < HEADER.size:
                break
            _, version, message_type, length = HEADER.unpack(self._buffer[:HEADER.size])
            if version != VERSION:
                raise ValueError("unsupported protocol version")
            if length > MAX_PAYLOAD:
                raise ValueError("frame payload exceeds limit")
            total = HEADER.size + length + TRAILER.size
            if len(self._buffer) < total:
                break
            raw = bytes(self._buffer[:total])
            received = TRAILER.unpack(raw[-TRAILER.size:])[0]
            if crc32(raw[:-TRAILER.size]) != received:
                raise ValueError("frame checksum mismatch")
            result.append(Frame(message_type, raw[HEADER.size:HEADER.size + length], version))
            del self._buffer[:total]
        return result

    def finish(self):
        if self._buffer:
            raise ValueError("truncated frame")
