"""Transport-neutral adapter that preserves every parsed frame for the caller."""

from .framing import FrameParser


class ProtocolTransport:
    def __init__(self, on_frame):
        if not callable(on_frame):
            raise TypeError("on_frame must be callable")
        self.parser = FrameParser()
        self.on_frame = on_frame

    def receive(self, data):
        frames = self.parser.feed(data)
        for frame in frames:
            self.on_frame(frame)
        return len(frames)

    def close(self):
        self.parser.finish()
