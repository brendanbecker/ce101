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

## Iterative Workflow (RECOMMENDED)

**Don't write all slides then generate once. Generate in batches.**

### Recommended Process

1. **Write 5-10 slides** following the [style guide](CE101-SLIDE-STYLE-GUIDE.md)
2. **Generate slides**: `./scripts/generate-slides.sh`
3. **Review in browser**: `open workspace/thumbnails/index.html`
4. **Fix issues immediately** before writing more slides
5. **Repeat** for next batch of slides

### Why This Works

- Catch formatting issues early
- Refine patterns as you go
- Build muscle memory for good markdown
- Less rework at the end
- Visual feedback helps you improve

### Visual Quality Check

When reviewing thumbnails, look for:
- **Too sparse**: Lots of whitespace, only 2-3 bullets
- **Too dense**: Wall of text, 8+ bullets
- **Orphaned text**: Single lines separated from content
- **Missing code blocks**: Technical examples that look like bullets

## Pre-Flight Checklist

Before generating the final deck, verify:

- [ ] **Content density**: Most slides have 4-6 bullets with sub-bullets
- [ ] **No orphaned text**: "Include:", "Example:", etc. integrated with content
- [ ] **Code formatting**: All code examples use proper code blocks (```)
- [ ] **Path consistency**: All file paths in backticks or code blocks
- [ ] **Comparison slides**: Consistent ✅/❌ formatting
- [ ] **Sub-bullets**: Add context, not redundancy
- [ ] **Opening/closing statements**: Frame the content on each slide
- [ ] **Visual hierarchy**: Clear structure with bold and formatting
- [ ] **Tab examples**: Formatted as code blocks, not plain bullets
- [ ] **Slide count**: Target 50-60 slides for 90-minute workshop

**Pro tip**: Run through this checklist every 10-15 slides, not just at the end.

## Common Issues and Solutions

### Issue: Orphaned Lead-In Text

**Problem**: Lines like "Include:" or "Example:" separated from their content

❌ **Don't do this:**
```markdown
Include:
- Item 1
- Item 2
```

✅ **Do this instead:**
```markdown
**Include these elements:**
- Item 1
- Item 2
```

**Solution**: Integrate lead-in text into the same line, use bold for emphasis.

---

### Issue: Sparse Slides

**Problem**: Only 2-3 bullets with lots of whitespace

**Solution**:
- Add sub-bullets for context and examples
- Include opening and closing statements
- Expand bullets with brief explanations
- Combine related sparse slides

---

### Issue: Code Examples Not Formatted

**Problem**: Tab layouts or commands shown as regular bullets

**Solution**:
- Use code blocks (```) for multi-line technical content
- Use backticks (`) for inline paths and commands
- See [style guide examples](CE101-SLIDE-STYLE-GUIDE.md#formatting-rules)

---

### Issue: Inconsistent Path Formatting

**Problem**: Some paths in backticks, others not

**Solution**:
- Always use backticks: `/company/SRE/file.yaml`
- Or use code blocks for multiple paths
- Be consistent across entire deck

---

### Issue: Too Many Bullets

**Problem**: 8+ bullets per slide, overcrowded

**Solution**:
- Split into multiple slides
- Use sub-bullets to create hierarchy
- Target 4-6 main bullets maximum
- Consider if all points are essential

---

## Troubleshooting

### Slides look cut off or overflow
- Reduce bullets per slide (max 6-7)
- Shorten text content
- Split into multiple slides
- Check for excessively long bullets

### Generated PowerPoint has errors
- Check `CE101-Master-Presentation.md` formatting
- Ensure slide separators are `---` on their own line
- Verify no malformed markdown
- Check for unclosed code blocks

### PNGs not updating
- Clear thumbnails: `rm -rf workspace/thumbnails`
- Regenerate: `./scripts/generate-slides.sh`
- Check LibreOffice is installed (required for PNG conversion)

### Slides too sparse or too dense
- Review [style guide](CE101-SLIDE-STYLE-GUIDE.md) for optimal density
- Aim for 4-6 main bullets with sub-bullets
- Use opening/closing statements to add context
- Add visual hierarchy with bold and formatting

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
