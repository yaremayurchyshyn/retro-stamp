# Project Brief: retro-stamp

## Overview

A library/package that adds retro-style timestamps to photos using their original metadata, replicating the date stamps from vintage film cameras.

## Problem Statement

When printing or sharing digital photos, there's no easy way to add the classic date stamp that old cameras used to burn into film. Manually adding timestamps is tedious and requires looking up when each photo was taken. This library automates the process.

## Goals

- Provide a simple API to add timestamps to photos programmatically
- Support modern image formats (JPEG, PNG, HEIC from iPhones)
- Preserve image quality (output in same format as input when possible)
- Design for future extensibility (styling, positioning, format options)

## Target Users

- Developers integrating timestamp functionality into their applications
- Future: End users via a hosted web service with UI

## Scope

### MVP (In Scope)
- Single image processing
- Read EXIF DateTimeOriginal metadata (fallback to other date fields)
- Classic orange/red timestamp in bottom-right corner
- Date format: `DD.MM.YYYY`
- Output to caller-specified destination path
- Support formats: JPEG, PNG, HEIC
- Skip images without date metadata (no error)

### Future (Out of Scope for MVP)
- Batch processing
- CLI interface
- Configurable styling (font, color, position)
- Configurable date formats
- Web service / UI

## Technical Direction

- Language: Python (better ecosystem for image processing and HEIC support)
- Key dependencies: Pillow, pillow-heif, piexif or similar for EXIF
- Publishable as a pip package

## Success Criteria

A developer can install the package and with minimal code:
1. Pass an image path
2. Get a new image with a retro timestamp based on when the photo was taken
