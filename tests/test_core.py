"""Tests for core module."""

import tempfile
from pathlib import Path

import pytest

from retro_stamp import TimestampResult, UnsupportedFormatError, add_timestamp

FIXTURES = Path(__file__).parent / "fixtures"


def test_add_timestamp_to_jpeg_with_exif():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.jpg"

        result = add_timestamp(FIXTURES / "sample.jpg", output)

        assert isinstance(result, TimestampResult)
        assert result.output_path == output
        assert result.timestamp_added is True
        assert result.date_used is not None
        assert result.date_source == "DateTimeOriginal"
        assert output.exists()


def test_add_timestamp_to_jpeg_without_exif():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.jpg"

        result = add_timestamp(FIXTURES / "sample_no_exif.jpg", output)

        assert result.timestamp_added is True
        assert result.date_source == "FileModifyDate"


def test_add_timestamp_to_png():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.png"

        result = add_timestamp(FIXTURES / "sample.png", output)

        assert result.timestamp_added is True
        assert output.exists()


def test_add_timestamp_to_webp():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.webp"

        result = add_timestamp(FIXTURES / "sample.webp", output)

        assert result.timestamp_added is True
        assert output.exists()


def test_add_timestamp_to_heic():
    heic_path = FIXTURES / "sample.heic"
    if not heic_path.exists():
        pytest.skip("HEIC fixture not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.heic"

        result = add_timestamp(heic_path, output)

        assert result.timestamp_added is True


def test_add_timestamp_returns_dimensions():
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.jpg"

        result = add_timestamp(FIXTURES / "sample.jpg", output)

        assert result.width == 800
        assert result.height == 600


def test_add_timestamp_raises_for_unsupported_format():
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_input = Path(tmpdir) / "test.bmp"
        fake_input.touch()
        output = Path(tmpdir) / "output.bmp"

        with pytest.raises(UnsupportedFormatError):
            add_timestamp(fake_input, output)


def test_add_timestamp_auto_format_converts_heic_to_jpeg():
    heic_path = FIXTURES / "sample.heic"
    if not heic_path.exists():
        pytest.skip("HEIC fixture not available")

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "output.heic"

        result = add_timestamp(heic_path, output, {"output_format": "auto"})

        assert result.output_path.suffix == ".jpg"
