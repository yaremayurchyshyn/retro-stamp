"""retro-stamp: Add retro-style timestamps to photos."""

from retro_stamp.core import TimestampResult, add_timestamp
from retro_stamp.exceptions import (
    ImageReadError,
    RetroStampError,
    UnsupportedFormatError,
)

__all__ = [
    "add_timestamp",
    "TimestampResult",
    "RetroStampError",
    "UnsupportedFormatError",
    "ImageReadError",
]

__version__ = "0.1.0"
