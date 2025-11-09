# CE101 Slide Generation Workflow

## Overview

**Goal**: Edit curriculum → Generate beautiful slides automatically

**Philosophy**: Curriculum modules (01-08.md) are the source of truth. Master presentation markdown is curated with Claude's help. Everything else is generated.

## Three-Step Workflow

### 1. Edit Curriculum (You)
Edit the curriculum modules:
- `01-core-concepts.md`
- `02-filesystem-organization.md`
- `03-multi-tab-orchestration.md`
- `04-local-data-stores.md`
- `05-integration-patterns.md`
- `06-practical-patterns.md`
- `07-common-pitfalls.md`
- `08-mcp-servers.md`

### 2. Update Master Presentation (You + Claude)
Work with Claude Code to update `CE101-Master-Presentation.md`:
- Extract slide-worthy concepts from curriculum updates
- Format for slides (max 6-7 bullets per slide)
- Add module dividers and transitions
- Keep it concise (50-60 slides recommended)

### 3. Generate Slides (Automated)
Run the generation script:
```bash
./scripts/generate-slides.sh
```

This automatically:
1. Generates `CE101-Master-Presentation-Styled.pptx` from markdown
2. Creates PNG previews in `workspace/thumbnails/`
3. Builds HTML index for easy browsing

## Quick Commands

```bash
# One-command generation: markdown → PowerPoint → PNGs
./scripts/generate-slides.sh

# View slides in browser
./scripts/view-slides.sh

# Or directly open:
open workspace/thumbnails/index.html
```

## File Organization

```
ce101/
├── 01-core-concepts.md              ← SOURCE (edit this)
├── 02-filesystem-organization.md    ← SOURCE
├── ...
├── 08-mcp-servers.md                ← SOURCE
│
├── CE101-Master-Presentation.md     ← CURATED (edit with Claude)
│
├── CE101-Master-Presentation-Styled.pptx   ← GENERATED (don't edit)
├── workspace/
│   ├── thumbnails/                   ← GENERATED PNGs
│   │   ├── slide-001.png
│   │   ├── ...
│   │   └── index.html               ← Browse all slides
│   └── slides-html/                 ← GENERATED (intermediate)
│
└── scripts/
    ├── generate-slides.sh           ← Main automation
    ├── pptx-to-png.sh              ← PowerPoint → PNG converter
    └── view-slides.sh              ← Browser launcher
```

## Slide Format Guidelines

### Slide Types

**Title Slide** (first slide only):
```markdown
# Context Engineering 101
## Stop Writing Prompts, Start Engineering Context

A practical guide for SREs and DevOps engineers
```

**Module Divider** (contains "Module" in title):
```markdown
# Module 1: Core Concepts
```

**Content Slide** (everything else):
```markdown
# Slide Title
## Optional Subtitle

Intro text here

- Bullet point 1
- Bullet point 2
- Maximum 6-7 bullets for readability
```

### Formatting Constraints

- Slide dimensions: 720pt × 405pt (16:9)
- Minimum margins: 0.5" (36pt) from edges
- Max bullets: 6-7 per slide
- Font sizes: Auto-adjusted based on content density
- Title limit: ~60 characters for readability

### Color Theme

Professional orange scheme (Little Caesars branding):
- Primary Orange: #F96D00
- Deep Orange: #E85D04
- Charcoal: #222831
- Cool Gray: #546E7A

## Troubleshooting

### Slides look cut off or overflow
- Reduce bullets per slide (max 6-7)
- Shorten text content
- Split into multiple slides

### Generated PowerPoint has errors
- Check `CE101-Master-Presentation.md` formatting
- Ensure slide separators are `---` on their own line
- Verify no malformed markdown

### PNGs not updating
- Clear thumbnails: `rm -rf workspace/thumbnails`
- Regenerate: `./scripts/generate-slides.sh`

## What NOT to Edit

These files are auto-generated and will be overwritten:
- `CE101-Master-Presentation-Styled.pptx`
- `workspace/thumbnails/*`
- `workspace/slides-html/*`

These are in `.gitignore` and should not be committed.

## Development Notes

### Slide Generator
Location: `workspace/generate-presentation.js`
- Parses markdown using marp-style separators (`---`)
- Generates HTML for each slide
- Converts HTML → PowerPoint using `html2pptx`
- Auto-adjusts font sizes for content density

### PNG Converter
Location: `scripts/pptx-to-png.sh`
- Uses LibreOffice to convert PowerPoint → PDF
- Uses `pdftoppm` to convert PDF → PNG images
- Generates HTML index for browsing
- Runs in ~10-15 seconds

### Styling
Orange theme configured in `workspace/generate-presentation.js:8-17`
Layout types: title slide, module divider, content slide
