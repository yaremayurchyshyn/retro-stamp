# retro-stamp

Add retro-style timestamps to photos using original metadata, like vintage film cameras.

## Installation

```bash
pip install retro-stamp
```

## Usage

```python
from retro_stamp import add_timestamp

result = add_timestamp("photo.jpg", "photo_stamped.jpg")

print(result.timestamp_added)  # True
print(result.date_used)        # datetime(2024, 6, 15, 14, 30)
print(result.date_source)      # "DateTimeOriginal"
```

## Options

```python
# Default: preserve original format
result = add_timestamp("photo.heic", "output.heic")
# Output: output.heic (same format, may have larger file size)

# Auto: choose best format for quality
result = add_timestamp("photo.heic", "output.heic", {"output_format": "auto"})
# Output: output.jpg (converted for better quality preservation)
```

| Option | Value | Description |
|--------|-------|-------------|
| `output_format` | `"preserve"` (default) | Keep same format as input |
| `output_format` | `"auto"` | Convert to best format for quality (HEIC → JPEG) |

## Supported Formats

- JPEG
- PNG
- HEIC (iPhone photos)
- WEBP

## Result Object

The `add_timestamp` function returns a `TimestampResult` with:

- `output_path` - Path where image was saved
- `width` - Image width in pixels
- `height` - Image height in pixels
- `date_used` - The datetime applied (or `None`)
- `date_source` - Which metadata field was used
- `timestamp_added` - Whether a timestamp was added

## Try It Locally

```bash
# Install dependencies
pip install -e .

# Run on any image
python3 try_it.py photo.jpg

# Custom output path
python3 try_it.py photo.jpg output/stamped.jpg

# iPhone HEIC
python3 try_it.py IMG_1234.HEIC

# Use auto format (HEIC → JPEG for better quality)
python3 try_it.py IMG_1234.HEIC --auto
```

## License

MIT
