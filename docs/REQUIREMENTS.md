# Requirements: retro-stamp

## Functional Requirements

### FR-1: Image Input
- Accept image via file path
- Supported formats: JPEG, PNG, HEIC, WEBP
- RAW formats (CR2, ARW, NEF) out of scope for MVP

### FR-2: Metadata Extraction
- Read date/time from EXIF metadata
- Priority order: `DateTimeOriginal` → `CreateDate` → `DateTimeDigitized` → file modification date
- If no date found: return original image unchanged (no error)

### FR-3: Timestamp Rendering
- Format: `DD.MM.YYYY`
- Style: Classic orange/red color (like 90s film cameras)
- Position: Bottom-right corner with ~2% margin from edges
- Size: Scale proportionally (~3% of image height)
- Shadow: Subtle dark shadow behind text for readability on bright backgrounds

### FR-4: Image Output
- Save to caller-specified destination path
- Output format: Same as input format
- Fallback: JPEG if original format cannot be written
- Preserve original EXIF metadata in output when possible

### FR-5: API Design
- Single function: `add_timestamp(input_path, output_path, options=None)`
- Return result object containing:
  - `output_path`: Path where image was saved
  - `width`: Output image width in pixels
  - `height`: Output image height in pixels
  - `date_used`: The date value applied (or `None`)
  - `date_source`: Which metadata field was used (or `None`)
  - `timestamp_added`: Boolean indicating if timestamp was added

## Non-Functional Requirements

### NFR-1: Quality
- No loss of image quality beyond format limitations
- Maintain original resolution

### NFR-2: Compatibility
- Python 3.8+
- Cross-platform: macOS, Linux, Windows

### NFR-3: Extensibility
- Options parameter allows future configuration without breaking changes
- Follow semantic versioning

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No date metadata found | Return original image unchanged, `timestamp_added=False` |
| Corrupted/unreadable image | Raise exception |
| Unsupported format | Raise exception |
| Invalid output path | Raise exception |

## Acceptance Criteria

- [ ] Can process JPEG image with EXIF date → outputs image with timestamp
- [ ] Can process PNG image → outputs image with timestamp (if date available)
- [ ] Can process HEIC image (iPhone) → outputs image with timestamp
- [ ] Can process WEBP image → outputs image with timestamp
- [ ] Timestamp is readable on both dark and light image backgrounds
- [ ] Original image quality is preserved
- [ ] Returns correct result object with all fields populated
- [ ] Gracefully handles image without date metadata
- [ ] Raises clear exception for unsupported formats
