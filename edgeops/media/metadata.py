"""Small media metadata schema independent from image decoding libraries."""

from dataclasses import dataclass

from ..domain.models import _text
from ..domain.validation import integer


@dataclass(frozen=True)
class ImageMetadata:
    width: int
    height: int
    orientation: int = 1
    thumbnail_bytes: int = 0

    def __post_init__(self):
        integer(self.width, "width", 1, 20000)
        integer(self.height, "height", 1, 20000)
        integer(self.orientation, "orientation", 1, 8)
        integer(self.thumbnail_bytes, "thumbnail_bytes", 0, 2 * 1024 * 1024)
