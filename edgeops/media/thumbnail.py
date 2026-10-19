"""Thumbnail planning without pretending to decode untrusted image bytes."""

from .metadata import ImageMetadata


def thumbnail_plan(metadata, max_width=320, max_height=240):
    if not isinstance(metadata, ImageMetadata):
        raise TypeError("metadata must be ImageMetadata")
    if max_width < 1 or max_height < 1:
        raise ValueError("thumbnail bounds must be positive")
    scale = min(max_width / metadata.width, max_height / metadata.height, 1)
    return {"width": max(1, round(metadata.width * scale)), "height": max(1, round(metadata.height * scale)), "required": scale < 1}
