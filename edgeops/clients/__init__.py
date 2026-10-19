"""Client-side contracts shared by PWA and desktop shells."""

from .profiles import ClientProfile, profiles
from .state import ClientState, apply_event_page

__all__ = ["ClientProfile", "profiles", "ClientState", "apply_event_page"]
