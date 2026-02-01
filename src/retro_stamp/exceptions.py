"""Exception classes for retro-stamp."""


class RetroStampError(Exception):
    """Base exception for retro-stamp."""


class UnsupportedFormatError(RetroStampError):
    """Raised when image format is not supported."""


class ImageReadError(RetroStampError):
    """Raised when image cannot be read or is corrupted."""
