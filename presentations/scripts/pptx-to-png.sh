#!/bin/bash
# Convert PowerPoint presentation to PNG images (one per slide)
#
# Usage: ./scripts/pptx-to-png.sh <input.pptx> [output-dir]
#
# Dependencies: libreoffice, pdftoppm (poppler-utils)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.pptx> [output-dir]"
    echo ""
    echo "Example: $0 CE101-Master-Presentation-Styled.pptx workspace/thumbnails"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_DIR="${2:-workspace/thumbnails}"

# Validate input file
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}Error: Input file not found: $INPUT_FILE${NC}"
    exit 1
fi

# Check for required tools
if ! command -v soffice &> /dev/null; then
    echo -e "${RED}Error: LibreOffice (soffice) not found${NC}"
    echo "Install with: sudo apt-get install libreoffice"
    exit 1
fi

if ! command -v pdftoppm &> /dev/null; then
    echo -e "${YELLOW}Warning: pdftoppm not found, trying ImageMagick...${NC}"
    if ! command -v convert &> /dev/null; then
        echo -e "${RED}Error: Neither pdftoppm nor ImageMagick found${NC}"
        echo "Install with: sudo apt-get install poppler-utils"
        exit 1
    fi
    USE_IMAGEMAGICK=1
else
    USE_IMAGEMAGICK=0
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}Output directory: $OUTPUT_DIR${NC}"

# Create temporary directory for PDF
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

PDF_FILE="$TEMP_DIR/presentation.pdf"

echo -e "${YELLOW}Step 1/2: Converting PPTX to PDF...${NC}"
soffice --headless --convert-to pdf --outdir "$TEMP_DIR" "$INPUT_FILE" > /dev/null 2>&1

if [ ! -f "$PDF_FILE" ]; then
    # LibreOffice might use the original filename
    PDF_FILE="$TEMP_DIR/$(basename "${INPUT_FILE%.pptx}.pdf")"
    if [ ! -f "$PDF_FILE" ]; then
        echo -e "${RED}Error: PDF conversion failed${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ PDF created successfully${NC}"

echo -e "${YELLOW}Step 2/2: Converting PDF to PNG images...${NC}"

if [ $USE_IMAGEMAGICK -eq 1 ]; then
    # Use ImageMagick (slower but more widely available)
    convert -density 150 "$PDF_FILE" "$OUTPUT_DIR/slide-%03d.png"
else
    # Use pdftoppm (faster and better quality)
    pdftoppm -png -r 150 "$PDF_FILE" "$OUTPUT_DIR/slide"

    # Rename files to have consistent numbering (slide-001.png, slide-002.png, etc.)
    cd "$OUTPUT_DIR"
    counter=1
    for file in slide-*.png; do
        if [ -f "$file" ]; then
            new_name=$(printf "slide-%03d.png" $counter)
            if [ "$file" != "$new_name" ]; then
                mv "$file" "$new_name"
            fi
            ((counter++))
        fi
    done
    cd - > /dev/null
fi

# Count generated images
NUM_SLIDES=$(find "$OUTPUT_DIR" -name "slide-*.png" | wc -l)

echo -e "${GREEN}✓ Generated $NUM_SLIDES PNG images${NC}"
echo ""
echo -e "${GREEN}Preview images created in: $OUTPUT_DIR${NC}"
echo "View with: ls -lh $OUTPUT_DIR/slide-*.png"

# Create an index HTML file for easy viewing
cat > "$OUTPUT_DIR/index.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>CE101 Slide Preview</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #F96D00;
        }
        .slide-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .slide {
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .slide img {
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .slide-number {
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
            color: #222831;
        }
    </style>
</head>
<body>
    <h1>CE101 Presentation - Slide Preview</h1>
    <p>Total slides: $NUM_SLIDES</p>
    <div class="slide-container">
EOF

# Add each slide to the HTML index
for i in $(seq 1 $NUM_SLIDES); do
    slide_num=$(printf "%03d" $i)
    cat >> "$OUTPUT_DIR/index.html" <<EOF
        <div class="slide">
            <img src="slide-$slide_num.png" alt="Slide $i">
            <div class="slide-number">Slide $i</div>
        </div>
EOF
done

# Close HTML
cat >> "$OUTPUT_DIR/index.html" <<EOF
    </div>
</body>
</html>
EOF

echo -e "${GREEN}✓ Created HTML index: $OUTPUT_DIR/index.html${NC}"
echo ""
echo -e "${YELLOW}To view slides in browser:${NC}"
echo "  file://$(realpath "$OUTPUT_DIR/index.html")"
