# Implementation Plan: retro-stamp

## Approach

- Code-first, then add tests for each module
- Flat task list, sequential execution
- All formats (JPEG, PNG, HEIC, WEBP) supported before release
- Tests use real sample images for reliability

## Task List

### Setup

- [ ] **1. Project scaffolding**
  - Create folder structure (`src/retro_stamp/`, `tests/`, etc.)
  - Create `pyproject.toml` with dependencies
  - Create empty module files

- [ ] **2. Acquire test images**
  - Find/create sample JPEG with EXIF DateTimeOriginal
  - Find/create sample HEIC with EXIF (iPhone photo)
  - Find/create sample PNG (convert from JPEG, may lose EXIF)
  - Find/create sample WEBP with EXIF
  - Create sample JPEG without EXIF metadata
  - Place in `tests/fixtures/`

### Core Implementation

- [ ] **3. Implement exceptions module**
  - `RetroStampError`, `UnsupportedFormatError`, `ImageReadError`

- [ ] **4. Implement metadata module**
  - Function to extract date from EXIF
  - Fallback chain: DateTimeOriginal → CreateDate → DateTimeDigitized → file mtime
  - Handle JPEG, HEIC, PNG, WEBP
  - Return `(datetime, source_field)` or `(None, None)`

- [ ] **5. Test metadata module**
  - Test extraction from each format
  - Test fallback chain
  - Test image with no EXIF

- [ ] **6. Implement renderer module**
  - Function to draw timestamp on image
  - Calculate font size (3% of height)
  - Calculate position (bottom-right, 2% margin)
  - Draw shadow + text
  - Return modified image

- [ ] **7. Test renderer module**
  - Test timestamp appears on image
  - Test scaling on different image sizes
  - Test shadow visibility

- [ ] **8. Implement core module**
  - `add_timestamp()` function
  - Format detection
  - Load image (with pillow-heif for HEIC)
  - Call metadata extraction
  - Call renderer (if date found)
  - Save in original format (fallback to JPEG)
  - Preserve EXIF in output
  - Return `TimestampResult`

- [ ] **9. Test core module**
  - Integration test: JPEG → JPEG with timestamp
  - Integration test: HEIC → HEIC with timestamp
  - Integration test: PNG → PNG with timestamp
  - Integration test: WEBP → WEBP with timestamp
  - Test: image without EXIF returns unchanged
  - Test: unsupported format raises exception
  - Test: corrupted image raises exception

### Packaging

- [ ] **10. Public API exports**
  - Export `add_timestamp`, `TimestampResult`, exceptions from `__init__.py`

- [ ] **11. Update README**
  - Installation instructions
  - Usage example
  - Supported formats

- [ ] **12. Add LICENSE**
  - Choose license (MIT recommended)

- [ ] **13. Final verification**
  - Run full test suite
  - Manual spot-check on real photos (if available)
  - Verify package installs correctly with `pip install -e .`

## Definition of Done

- All tests pass
- All four formats (JPEG, PNG, HEIC, WEBP) work correctly
- Package installable via pip
- README has clear usage instructions
