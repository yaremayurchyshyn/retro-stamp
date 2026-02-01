"""Tests for renderer module."""

from datetime import datetime

from PIL import Image

from retro_stamp.renderer import render_timestamp


def test_render_timestamp_returns_image():
    image = Image.new("RGB", (800, 600), color="white")
    date = datetime(2024, 6, 15)

    result = render_timestamp(image, date)

    assert isinstance(result, Image.Image)
    assert result.size == image.size


def test_render_timestamp_modifies_image():
    image = Image.new("RGB", (800, 600), color="white")
    date = datetime(2024, 6, 15)

    result = render_timestamp(image, date)

    assert result.tobytes() != image.tobytes()


def test_render_timestamp_preserves_mode():
    image = Image.new("RGB", (800, 600), color="white")
    date = datetime(2024, 6, 15)

    result = render_timestamp(image, date)

    assert result.mode == image.mode


def test_render_timestamp_scales_with_image_size():
    small_image = Image.new("RGB", (400, 300), color="white")
    large_image = Image.new("RGB", (1600, 1200), color="white")
    date = datetime(2024, 6, 15)

    small_result = render_timestamp(small_image, date)
    large_result = render_timestamp(large_image, date)

    assert small_result.size == small_image.size
    assert large_result.size == large_image.size
