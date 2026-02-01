# Known Issues & Backlog

## Active Issues

### ISSUE-001: HEIC output file size significantly larger than original

**Status**: Resolved  
**Severity**: Medium  
**Discovered**: 2026-02-01  
**Resolved**: 2026-02-01

**Description**:  
When processing iPhone HEIC photos, the output file is ~4-5x larger than the original (e.g., 1.8MB → 8.5MB).

**Root Cause**:  
This is a known limitation, not a bug in our code. Apple's HEIC encoder (used on iPhone) is highly optimized and uses proprietary compression settings. The pillow-heif library uses libheif which doesn't achieve the same compression efficiency.

**References**:
- https://developer.apple.com/forums/thread/793946

**Options Considered**:
1. Output HEIC as JPEG instead (smaller files, widely compatible)
2. Add option for user to choose output format
3. Accept the limitation and document it
4. Investigate libheif encoding parameters for better compression

**Decision**:  
Implemented Option 2 - Added `output_format` option with two modes:
- `"preserve"` (default): Keep same format as input, even if size/quality differs
- `"auto"`: Library chooses best format for quality (HEIC → JPEG)

**Rationale**:  
Gives users control. Those who need HEIC format can accept larger size. Those who prioritize size/quality can use auto mode.

---

### ISSUE-002: Brightness difference in processed HEIC images

**Status**: Documented (Limitation)  
**Severity**: Medium  
**Discovered**: 2026-02-01

**Description**:  
Processed HEIC images appear darker compared to the original when viewed on macOS/iOS.

**Root Cause**:  
iPhone photos contain an **HDR gain map** (`urn:com:apple:photo:2020:aux:hdrgainmap`) - auxiliary data that tells compatible displays how to boost brightness for HDR rendering. When viewing the original HEIC on macOS/iOS, the system automatically applies this gain map, making the image appear brighter.

Our processed images lose this gain map because:
1. pillow-heif can read auxiliary images but cannot write them back
2. Apple's gain map format uses proprietary metadata (not standard XMP)
3. Applying the gain map permanently ("baking in") would require knowing the exact parameters

**Technical Investigation**:
```python
# We CAN extract the gain map:
heif = pillow_heif.open_heif("photo.HEIC")
aux_info = heif[0].info.get('aux', {})
# Returns: {'urn:com:apple:photo:2020:aux:hdrgainmap': [63]}

gain_map = heif[0].get_aux_image(63)  # Works!
# Returns: HeifAuxImage, size=(2142, 2856), mode=L

# But we CANNOT write it back - no API exists in pillow-heif
```

**Key Finding**:  
The actual pixel values are identical between original and processed images. The perceived brightness difference is because macOS/iOS applies the HDR gain map when displaying the original HEIC, but our output doesn't have this gain map.

**Options Considered**:
1. **Accept limitation** - Document that HDR gain maps aren't preserved
2. **Bake in the gain map** - Apply gain map permanently to pixel values
3. **Use Apple native APIs** - Use ImageIO via PyObjC (macOS only)
4. **Wait for library support** - Monitor pillow-heif for aux image write support
5. **Use libultrahdr** - Google's library for HDR gain map handling

**Decision**:  
Option 1 - Accept and document the limitation. No viable workaround exists for brightness.

**Rationale**:
- Option 2 (bake in): Would require reverse-engineering Apple's proprietary parameters; results would vary
- Option 3 (native APIs): Would make library macOS-only, breaking cross-platform goal
- Option 4 (wait): No timeline for pillow-heif support
- Option 5 (libultrahdr): Adds significant complexity; designed for Android format, not Apple's

**Important**: There is currently NO workaround for the brightness difference. The `auto` format option only helps with file size (ISSUE-001), not brightness. Users must accept that processed images will appear as SDR rendition.

**Workarounds for Users**:
1. Accept that processed images match SDR rendition (what non-HDR displays show)
2. View processed images on non-HDR displays where difference is minimal
3. Use `output_format: "auto"` for smaller file size (but brightness is same as preserve mode)

**Note**: The `auto` format option does NOT fix the brightness issue - it only addresses the file size issue (ISSUE-001). Both HEIC and JPEG outputs have the same pixel values and will appear darker than the original when viewed on HDR displays.

**Additional Investigation (2026-02-01)**:

*Option 2 - Baking in gain map:*
- Successfully extracted gain map from HEIC using `pillow_heif.get_aux_image()`
- Gain map stats: min=87, max=253, avg=152.7 (not centered at 128 as expected)
- Created test images with different headroom values (0.5, 1.0, 1.5)
- Problem: Without knowing Apple's exact parameters (headroom, offsets, gamma), results are inconsistent
- Apple doesn't use standard XMP metadata format, parameters are proprietary

*Alternative libraries explored:*
| Library | Read Aux | Write Aux | Notes |
|---------|----------|-----------|-------|
| pillow-heif | ✅ | ❌ | Best Python option, but no aux write |
| pyheif | ❌ | ❌ | Read-only, deprecated |
| libheif CLI | ✅ | ⚠️ | May work via `heif-enc`, requires separate install |
| ImageMagick | ✅ | ❌ | Uses libheif, same limitations |
| AppleJPEGGainMap | ✅ | ✅ | Swift only, macOS only |

*Reference implementation found:*
- [AppleJPEGGainMap](https://github.com/grapeot/AppleJPEGGainMap) - Swift implementation that works
- Uses Apple's native ImageIO APIs
- Requires a "reference" iPhone photo to extract metadata structure
- macOS only, not portable to Python without PyObjC

**Conclusion**: No Python library currently supports writing HEIC with auxiliary images. The only working solution requires Apple's native Swift APIs, which would break cross-platform support. 

**Final Decision**: Accept the limitation. The HDR brightness difference is a trade-off we accept to maintain:
- Cross-platform compatibility
- Simple, maintainable code
- Consistent behavior across all image formats

Tested workarounds (uniform brightness boost of 10-20%) produced acceptable but imperfect results, and would add complexity for marginal benefit.

---

## Resolved Issues

(None yet - issues above are first encountered)

---

## Backlog (Future Improvements)

### BACKLOG-001: Configurable timestamp styling
- Font, color, position, format
- Priority: Medium
- Status: Planned for post-MVP

### BACKLOG-002: CLI interface
- Command-line tool for batch processing
- Priority: Low
- Status: Planned for post-MVP

### BACKLOG-003: Batch processing API
- Process multiple images in one call
- Priority: Low
- Status: Planned for post-MVP

### BACKLOG-004: Custom font support
- Bundle retro-style fonts
- Priority: Low
- Status: Planned for post-MVP

### BACKLOG-005: HDR gain map preservation
- Preserve Apple HDR gain maps in output
- Priority: Low
- Status: Blocked (waiting for pillow-heif support)
- Related: ISSUE-002

---

## Decision Log

| Date | Issue | Decision | Rationale |
|------|-------|----------|-----------|
| 2026-02-01 | ISSUE-001 | Add `output_format` option | Gives users control over size vs format trade-off |
| 2026-02-01 | ISSUE-002 | Document as limitation | Cross-platform support more important than HDR; workaround exists |
| 2026-02-01 | ISSUE-002 | Investigated baking in gain map | Results inconsistent without Apple's proprietary parameters |
| 2026-02-01 | ISSUE-002 | Rejected alternative libraries | No Python library supports writing HEIC aux images |
| 2026-02-01 | ISSUE-002 | Wait for pillow-heif support | Added BACKLOG-005 to track; revisit when library adds aux write |
| 2026-02-01 | ISSUE-002 | Tested brightness workaround | 10% boost acceptable but imperfect; complexity not worth marginal benefit |
| 2026-02-01 | ISSUE-002 | Final: Accept limitation | Prioritize cross-platform support and code simplicity over HDR |
