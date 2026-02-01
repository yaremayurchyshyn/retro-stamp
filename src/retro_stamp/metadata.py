"""Metadata extraction from images."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import piexif
from PIL import Image
from PIL.ExifTags import TAGS

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

DATE_FIELDS_PRIORITY = [
    "DateTimeOriginal",
    "DateTimeDigitized",
    "DateTime",
]


def extract_date(image_path: str | Path) -> tuple[datetime | None, str | None]:
    """
    Extract date from image EXIF metadata.

    Returns:
        Tuple of (datetime, source_field) or (None, None) if no date found.
    """
    path = Path(image_path)

    date_result = _extract_from_pillow(path)
    if date_result[0]:
        return date_result

    date_result = _extract_from_piexif(path)
    if date_result[0]:
        return date_result

    return _extract_from_file_mtime(path)


def _extract_from_pillow(path: Path) -> tuple[datetime | None, str | None]:
    """Extract date using Pillow's EXIF reader."""
    try:
        with Image.open(path) as image:
            exif_data = image.getexif()
            if not exif_data:
                return None, None

            tag_names = {v: k for k, v in TAGS.items()}

            for field_name in DATE_FIELDS_PRIORITY:
                tag_id = tag_names.get(field_name)
                if tag_id and tag_id in exif_data:
                    date = _parse_date(exif_data[tag_id])
                    if date:
                        return date, field_name

            exif_ifd = exif_data.get_ifd(piexif.ExifIFD.DateTimeOriginal)
            if exif_ifd:
                for field_name in DATE_FIELDS_PRIORITY:
                    tag_id = tag_names.get(field_name)
                    if tag_id and tag_id in exif_ifd:
                        date = _parse_date(exif_ifd[tag_id])
                        if date:
                            return date, field_name
    except (OSError, ValueError, KeyError):
        pass

    return None, None


def _extract_from_piexif(path: Path) -> tuple[datetime | None, str | None]:
    """Extract date using piexif for JPEG files."""
    try:
        exif_dict = piexif.load(str(path))
        exif_ifd = exif_dict.get("Exif", {})

        field_mapping = {
            piexif.ExifIFD.DateTimeOriginal: "DateTimeOriginal",
            piexif.ExifIFD.DateTimeDigitized: "DateTimeDigitized",
        }

        for tag_id, field_name in field_mapping.items():
            if tag_id in exif_ifd:
                value = exif_ifd[tag_id]
                if isinstance(value, bytes):
                    value = value.decode("utf-8", errors="ignore")
                date = _parse_date(value)
                if date:
                    return date, field_name
    except (OSError, ValueError, KeyError, piexif.InvalidImageDataError):
        pass

    return None, None


def _extract_from_file_mtime(path: Path) -> tuple[datetime | None, str | None]:
    """Fallback to file modification time."""
    try:
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime), "FileModifyDate"
    except OSError:
        return None, None


def _parse_date(value: str | bytes | None) -> datetime | None:
    """Parse EXIF date string to datetime."""
    if not value:
        return None

    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="ignore")

    value = value.strip().rstrip("\x00")

    try:
        return datetime.strptime(value, EXIF_DATE_FORMAT)
    except ValueError:
        return None
