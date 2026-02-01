#!/usr/bin/env python3
"""Quick script to test retro-stamp on any image."""

import sys
from pathlib import Path

from retro_stamp import add_timestamp


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 try_it.py <image_path> [output_path] [--auto]")
        print()
        print("Options:")
        print("  --auto  Use best format for quality (HEIC → JPEG)")
        print()
        print("Examples:")
        print("  python3 try_it.py photo.jpg")
        print("  python3 try_it.py IMG_1234.HEIC --auto")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    
    use_auto = "--auto" in sys.argv
    args = [a for a in sys.argv[2:] if a != "--auto"]
    
    if args:
        output_path = Path(args[0])
    else:
        output_path = input_path.parent / f"{input_path.stem}_stamped{input_path.suffix}"

    options = {"output_format": "auto"} if use_auto else None
    result = add_timestamp(input_path, output_path, options)

    print(f"Input:  {input_path}")
    print(f"Output: {result.output_path}")
    print(f"Size:   {result.width}x{result.height}")
    print(f"Date:   {result.date_used}")
    print(f"Source: {result.date_source}")
    print(f"Added:  {result.timestamp_added}")


if __name__ == "__main__":
    main()
