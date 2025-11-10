#!/bin/bash
# Generate PowerPoint slides and PNG previews from master markdown
#
# Usage: ./scripts/generate-slides.sh

set -euo pipefail

MASTER_MD="CE101-Master-Presentation.md"
OUTPUT_PPTX="CE101-Master-Presentation-Styled.pptx"
THUMBNAIL_DIR="workspace/thumbnails"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}📊 CE101 Slide Generator${NC}\n"

# Check master markdown exists
if [ ! -f "$MASTER_MD" ]; then
    echo "❌ Error: Master markdown not found: $MASTER_MD"
    echo ""
    echo "Create it first by editing curriculum and working with Claude Code."
    exit 1
fi

# Step 1: Generate PowerPoint from markdown
echo -e "${YELLOW}Step 1/2: Generating PowerPoint from markdown...${NC}"
NODE_PATH=/home/becker/.nvm/versions/node/v20.19.3/lib/node_modules \
  node scripts/generate-presentation.js

if [ ! -f "$OUTPUT_PPTX" ]; then
    echo "❌ Error: PowerPoint generation failed"
    exit 1
fi

echo -e "${GREEN}✓ PowerPoint created: $OUTPUT_PPTX${NC}\n"

# Step 2: Generate PNG previews
echo -e "${YELLOW}Step 2/2: Generating PNG previews...${NC}"
./scripts/pptx-to-png.sh "$OUTPUT_PPTX" "$THUMBNAIL_DIR" | grep -E "✓|Generated"

echo ""
echo -e "${GREEN}✅ Done!${NC}"
echo ""
echo "📂 Output files:"
echo "   PowerPoint: $OUTPUT_PPTX"
echo "   Thumbnails: $THUMBNAIL_DIR/"
echo "   Preview:    file://$(realpath $THUMBNAIL_DIR/index.html)"
echo ""
echo "💡 To view slides: ./scripts/view-slides.sh"
