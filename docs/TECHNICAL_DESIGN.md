# Technical Design: retro-stamp

## Technology Stack

- **Language**: Python 3.8+
- **Image Processing**: Pillow
- **HEIC Support**: pillow-heif
- **EXIF Reading**: piexif (for JPEG), Pillow's built-in (for others)
- **Testing**: pytest
- **Package Management**: setuptools, published to PyPI

## Project Structure

```
retro-stamp/
├── src/
│   └── retro_stamp/
│       ├── __init__.py        # Public API exports
│       ├── core.py            # Main add_timestamp function
│       ├── metadata.py        # EXIF extraction logic
│       ├── renderer.py        # Timestamp drawing logic
│       └── exceptions.py      # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest fixtures, sample images
│   ├── test_core.py           # Integration tests
│   ├── test_metadata.py       # Metadata extraction tests
│   └── test_renderer.py       # Rendering tests
│   └── fixtures/              # Sample test images
│       ├── sample.jpg
│       ├── sample.png
│       ├── sample.heic
│       └── sample_no_exif.jpg
├── docs/
│   ├── PROJECT_BRIEF.md
│   ├── REQUIREMENTS.md
│   └── TECHNICAL_DESIGN.md
├── pyproject.toml             # Package config, dependencies
├── README.md
└── LICENSE
```

## Dependencies

```toml
[project]
dependencies = [
    "Pillow>=10.0.0",
    "pillow-heif>=0.13.0",
    "piexif>=1.1.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

## API Design

### Public Function

```python
def add_timestamp(
    input_path: str | Path,
    output_path: str | Path,
    options: dict | None = None
) -> TimestampResult:
    """
    Add retro-style timestamp to an image.
    
    Args:
        input_path: Path to source image
        output_path: Path for output image
        options: Reserved for future configuration
        
    Returns:
        TimestampResult with operation details
        
    Raises:
        UnsupportedFormatError: If image format not supported
        ImageReadError: If image cannot be read
    """
```

### Result Object

```python
@dataclass
class TimestampResult:
    output_path: Path
    width: int
    height: int
    date_used: datetime | None
    date_source: str | None  # e.g., "DateTimeOriginal", "CreateDate"
    timestamp_added: bool
```

### Exceptions

```python
class RetroStampError(Exception):
    """Base exception for retro-stamp"""

class UnsupportedFormatError(RetroStampError):
    """Raised when image format is not supported"""

class ImageReadError(RetroStampError):
    """Raised when image cannot be read or is corrupted"""
```

## Module Responsibilities

### `core.py`
- Orchestrates the workflow
- Validates input/output paths
- Delegates to metadata and renderer modules
- Handles format detection and output

### `metadata.py`
- Extracts EXIF data from images
- Implements fallback chain: DateTimeOriginal → CreateDate → DateTimeDigitized → file mtime
- Parses date strings into datetime objects

### `renderer.py`
- Draws timestamp on image
- Handles font sizing (3% of image height)
- Positions text (bottom-right, 2% margin)
- Applies shadow effect for readability
- Uses system default font

## Format Handling

| Input Format | Output Format | Notes |
|--------------|---------------|-------|
| JPEG | JPEG | Preserve quality |
| PNG | PNG | Preserve transparency if present |
| HEIC | HEIC | Via pillow-heif |
| WEBP | WEBP | Native Pillow support |

If output format fails, fallback to JPEG with quality=95.

## Timestamp Rendering Details

- **Color**: RGB(255, 140, 0) - orange
- **Shadow**: RGB(0, 0, 0) with 50% opacity, offset 2px
- **Font**: System default (PIL default)
- **Size**: 3% of image height
- **Position**: Bottom-right, 2% margin from edges
- **Format**: DD.MM.YYYY

## Testing Strategy

- **Unit tests**: Each module tested in isolation
- **Integration tests**: Full workflow with real images
- **Fixtures**: Sample images in each supported format
- **Coverage target**: 80%+
