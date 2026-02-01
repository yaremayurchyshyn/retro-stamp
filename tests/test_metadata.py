"""Tests for metadata module."""

from pathlib import Path

import pytest

from retro_stamp.metadata import extract_date

FIXTURES = Path(__file__).parent / "fixtures"


def test_extract_date_from_jpeg_with_exif():
    date, source = extract_date(FIXTURES / "sample.jpg")

    assert date is not None
    assert date.year == 2024
    assert date.month == 6
    assert date.day == 15
    assert source == "DateTimeOriginal"


def test_extract_date_from_jpeg_without_exif_falls_back_to_mtime():
    date, source = extract_date(FIXTURES / "sample_no_exif.jpg")

    assert date is not None
    assert source == "FileModifyDate"


def test_extract_date_from_webp_with_exif():
    date, source = extract_date(FIXTURES / "sample.webp")

    assert date is not None
    assert date.year == 2023
    assert date.month == 12
    assert source == "DateTimeOriginal"


def test_extract_date_from_png_falls_back_to_mtime():
    date, source = extract_date(FIXTURES / "sample.png")

    assert date is not None
    assert source == "FileModifyDate"


def test_extract_date_from_heic():
    heic_path = FIXTURES / "sample.heic"
    if not heic_path.exists():
        pytest.skip("HEIC fixture not available")

    date, source = extract_date(heic_path)

    assert date is not None
