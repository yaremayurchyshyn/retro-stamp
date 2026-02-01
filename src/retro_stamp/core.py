"""Core functionality for adding timestamps to images."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

from retro_stamp.exceptions import ImageReadError, UnsupportedFormatError
from retro_stamp.metadata import extract_date
from retro_stamp.renderer import render_timestamp

register_heif_opener()

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
FORMATS_WITH_QUALITY_LOSS = {".heic"}


@dataclass
class TimestampResult:
    """Result of timestamp operation."""

    output_path: Path
    width: int
    height: int
    date_used: datetime | None
    date_source: str | None
    timestamp_added: bool


def add_timestamp(
    input_path: str | Path,
    output_path: str | Path,
    options: dict | None = None,
) -> TimestampResult:
    """Add retro-style timestamp to an image.

    Options:
        output_format: "preserve" (default) or "auto"
            - preserve: Keep same format as input
            - auto: Choose best format for quality (HEIC → JPEG)
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    options = options or {}

    _validate_format(input_path)
    image, image_info = _load_image(input_path)
    date, source = extract_date(input_path)

    if date:
        image = render_timestamp(image, date)

    output_path = _save_image(image, image_info, input_path, output_path, options)

    return TimestampResult(
        output_path=output_path,
        width=image.width,
        height=image.height,
        date_used=date,
        date_source=source,
        timestamp_added=date is not None,
    )


def _validate_format(path: Path) -> None:
    """Validate image format is supported."""
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(f"Format '{suffix}' is not supported")


def _load_image(path: Path) -> tuple[Image.Image, dict]:
    """Load image from path, preserving metadata."""
    try:
        image = Image.open(path)
        image.load()
        info = dict(image.info)
        return image, info
    except (OSError, ValueError) as error:
        raise ImageReadError(f"Cannot read image: {error}") from error


def _determine_output_format(input_path: Path, options: dict) -> str:
    """Determine best output format based on options."""
    suffix = input_path.suffix.lower()
    output_format = options.get("output_format", "preserve")

    if output_format == "auto" and suffix in FORMATS_WITH_QUALITY_LOSS:
        return ".jpg"

    return suffix


def _save_image(
    image: Image.Image,
    original_info: dict,
    input_path: Path,
    output_path: Path,
    options: dict,
) -> Path:
    """Save image preserving format and quality when possible."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    target_format = _determine_output_format(input_path, options)

    if target_format != input_path.suffix.lower():
        output_path = output_path.with_suffix(target_format)

    save_kwargs = _build_save_kwargs(original_info)

    try:
        _save_with_format(image, output_path, target_format, save_kwargs)
    except (OSError, ValueError):
        output_path = output_path.with_suffix(".jpg")
        image.convert("RGB").save(output_path, "JPEG", quality=95)

    return output_path


def _build_save_kwargs(original_info: dict) -> dict:
    """Build save kwargs preserving ICC profile and EXIF."""
    save_kwargs = {}
    if original_info.get("icc_profile"):
        save_kwargs["icc_profile"] = original_info["icc_profile"]
    if original_info.get("exif"):
        save_kwargs["exif"] = original_info["exif"]
    return save_kwargs


def _save_with_format(
    image: Image.Image,
    output_path: Path,
    target_format: str,
    save_kwargs: dict,
) -> None:
    """Save image in specified format."""
    if target_format in {".jpg", ".jpeg"}:
        image.convert("RGB").save(output_path, "JPEG", quality=95, **save_kwargs)
    elif target_format == ".png":
        image.save(output_path, "PNG", **save_kwargs)
    elif target_format == ".webp":
        image.convert("RGB").save(output_path, "WEBP", quality=95, **save_kwargs)
    elif target_format == ".heic":
        image.convert("RGB").save(output_path, "HEIF", quality=90, **save_kwargs)
    else:
        image.convert("RGB").save(output_path, "JPEG", quality=95, **save_kwargs)
