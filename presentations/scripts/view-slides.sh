#!/bin/bash
# Quick viewer for generated slide PNGs
#
# Usage: ./scripts/view-slides.sh [thumbnail-dir]

THUMBNAIL_DIR="${1:-workspace/thumbnails}"

if [ ! -d "$THUMBNAIL_DIR" ]; then
    echo "Error: Thumbnail directory not found: $THUMBNAIL_DIR"
    echo ""
    echo "Generate thumbnails first:"
    echo "  ./scripts/pptx-to-png.sh CE101-Master-Presentation-Styled.pptx"
    exit 1
fi

if [ ! -f "$THUMBNAIL_DIR/index.html" ]; then
    echo "Error: No index.html found in $THUMBNAIL_DIR"
    exit 1
fi

INDEX_FILE="$(realpath "$THUMBNAIL_DIR/index.html")"
NUM_SLIDES=$(find "$THUMBNAIL_DIR" -name "slide-*.png" | wc -l)

echo "Found $NUM_SLIDES slides in $THUMBNAIL_DIR"
echo ""
echo "Opening in browser: file://$INDEX_FILE"
echo ""

# Try to open in WSL browser (wslview) or default Linux browser
if command -v wslview &> /dev/null; then
    wslview "$INDEX_FILE"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$INDEX_FILE"
elif command -v sensible-browser &> /dev/null; then
    sensible-browser "$INDEX_FILE"
else
    echo "No browser launcher found. Please open manually:"
    echo "  file://$INDEX_FILE"
fi
