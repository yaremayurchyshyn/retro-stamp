"""Timestamp rendering on images."""

from __future__ import annotations

from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

TIMESTAMP_COLOR = (255, 140, 0)  # Orange
SHADOW_COLOR = (0, 0, 0, 128)  # Black with 50% opacity
SHADOW_OFFSET = 2
FONT_SIZE_RATIO = 0.03  # 3% of image height
MARGIN_RATIO = 0.02  # 2% from edges
DATE_FORMAT = "%d.%m.%Y"


def render_timestamp(image: Image.Image, date: datetime) -> Image.Image:
    """
    Render timestamp on image.

    Returns:
        New image with timestamp rendered.
    """
    original_mode = image.mode
    result = image.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    text = date.strftime(DATE_FORMAT)
    font = _get_font(result.height)
    position = _calculate_position(result.size, text, font)

    _draw_shadow(draw, position, text, font)
    _draw_text(draw, position, text, font)

    result = Image.alpha_composite(result, overlay)

    if original_mode in ("RGB", "L"):
        result = result.convert(original_mode)

    return result


def _get_font(image_height: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Get font scaled to image size."""
    font_size = max(int(image_height * FONT_SIZE_RATIO), 12)
    try:
        return ImageFont.truetype("Arial", font_size)
    except OSError:
        return ImageFont.load_default()


def _calculate_position(
    image_size: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> tuple[int, int]:
    """Calculate bottom-right position with margin."""
    width, height = image_size
    margin_x = int(width * MARGIN_RATIO)
    margin_y = int(height * MARGIN_RATIO)

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = width - text_width - margin_x
    y = height - text_height - margin_y

    return x, y


def _draw_shadow(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    """Draw shadow behind text."""
    shadow_position = (position[0] + SHADOW_OFFSET, position[1] + SHADOW_OFFSET)
    draw.text(shadow_position, text, font=font, fill=SHADOW_COLOR)


def _draw_text(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    """Draw timestamp text."""
    draw.text(position, text, font=font, fill=TIMESTAMP_COLOR)
