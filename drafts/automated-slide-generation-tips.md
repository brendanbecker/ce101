# CE101 Curriculum to Slides Workflow

## Your Workflow Architecture

```
Curriculum Modules (source of truth)
    ↓
Master Markdown File (generated)
    ↓
PowerPoint Slides (generated)
```

**Source**: 8 curriculum markdown files (01-08)
**Generated**: CE101-Master-Presentation.md
**Output**: CE101-Master-Presentation-Styled.pptx

## Philosophy

**Goal**: Edit curriculum modules → Generate beautiful slides automatically

**Key Principle**: Curriculum modules are the source of truth. Everything else is generated and disposable.

---

## Implementation Plan: Curriculum to Slides Pipeline

### Phase 1: Master Markdown Generator (NEEDED)

**Create**: `scripts/generate-master-markdown.js`

**Purpose**: Combine 8 curriculum modules into master presentation markdown

**Features needed:**
```javascript
// 1. Read all curriculum modules in order
const modules = [
  '01-core-concepts.md',
  '02-filesystem-organization.md',
  '03-multi-tab-orchestration.md',
  '04-local-data-stores.md',
  '05-integration-patterns.md',
  '06-practical-patterns.md',
  '07-common-pitfalls.md',
  '08-mcp-servers.md'
];

// 2. Extract slide-worthy content
// - Headers → slide titles
// - Key concepts → slide bullets
// - Examples → example slides

// 3. Add presentation-specific slides
// - Title slide
// - Module dividers
// - Takeaway slides

// 4. Generate CE101-Master-Presentation.md
```

**Extraction rules:**
- `# Module Title` → Module divider slide
- `## Section` → Content slide title
- `### Subsection` → Subtitle or nested concept
- Bullet lists → Slide bullets (max 6)
- Code blocks → Code example slides
- Tables → Comparison slides

**Example transformation:**
```markdown
# 01-core-concepts.md:
## Space Jam Theory
Your biggest barrier isn't the AI...
- Complex tasks are possible
- AI amplifies expertise

# Becomes in master:
---
# Space Jam Theory
## If You Can Dream It, You Can Do It

Your biggest barrier isn't the AI. It's your own self-imposed limit.

- Complex tasks are possible
- AI amplifies expertise
- Don't self-limit before trying
```

### Phase 2: Slide Generator (WORKING)

**Existing**: `workspace/generate-presentation.js`

**Status**: ✅ Generates all 56 slides successfully (with recent fixes)

**Input**: `CE101-Master-Presentation.md`
**Output**: `CE101-Master-Presentation-Styled.pptx`

**Theme**: Orange (Little Caesars) - already configured

### Phase 3: Automation Scripts (NEEDED)

**Create**: `scripts/` directory with helper scripts

#### 3.1. One-Command Generation
```bash
#!/bin/bash
# scripts/generate-all.sh

echo "📚 Generating master markdown from curriculum..."
node scripts/generate-master-markdown.js

echo "🎨 Generating styled slides..."
NODE_PATH=/home/becker/.nvm/versions/node/v20.19.3/lib/node_modules \
  node workspace/generate-presentation.js

echo "📸 Creating thumbnails..."
~/venvs/pptx-skill/bin/python ~/.claude/skills/pptx/scripts/thumbnail.py \
  CE101-Master-Presentation-Styled.pptx workspace/thumbnails --cols 5

echo "✅ Done! Check workspace/thumbnails for preview"
```

#### 3.2. Content Validator
```bash
# scripts/validate-curriculum.sh
# Check curriculum modules for slide-breaking issues
```

#### 3.3. Quick Preview
```bash
# scripts/preview-module.sh 01
# Generate slides from just module 01 for quick iteration
```

### Phase 4: Documentation (NEEDED)

**Update README.md** with new workflow:

```markdown
## Editing Curriculum

**Source files**: `01-*.md` through `08-*.md`

**To generate slides:**
```bash
npm run generate-slides
# or
./scripts/generate-all.sh
```

**To preview changes:**
```bash
# Edit a module
vim 06-practical-patterns.md

# Regenerate everything
npm run generate-slides

# View thumbnails
open workspace/thumbnails/thumbnails-1.jpg
```

### Current File Structure

```
ce101/
├── 01-core-concepts.md              ← SOURCE (edit these)
├── 02-filesystem-organization.md    ← SOURCE
├── 03-multi-tab-orchestration.md    ← SOURCE
├── 04-local-data-stores.md          ← SOURCE
├── 05-integration-patterns.md       ← SOURCE
├── 06-practical-patterns.md         ← SOURCE
├── 07-common-pitfalls.md            ← SOURCE
├── 08-mcp-servers.md                ← SOURCE (NEW - needs slides)
├── CE101-Master-Presentation.md     ← GENERATED (don't edit)
├── CE101-Master-Presentation-Styled.pptx  ← OUTPUT
├── scripts/
│   ├── generate-master-markdown.js  ← TO CREATE
│   ├── generate-all.sh              ← TO CREATE
│   └── validate-curriculum.sh       ← TO CREATE
└── workspace/
    ├── generate-presentation.js     ← WORKING ✅
    └── thumbnails/                  ← Generated previews
```

### Next Steps Checklist

- [ ] **Create master markdown generator** (`scripts/generate-master-markdown.js`)
  - Read 8 curriculum modules
  - Extract slide-worthy content
  - Add title/divider/takeaway slides
  - Output: `CE101-Master-Presentation.md`

- [ ] **Create automation script** (`scripts/generate-all.sh`)
  - Run master generator
  - Run slide generator
  - Create thumbnails
  - One command workflow

- [ ] **Add Module 8 content** to existing presentation
  - Currently only 7 modules in slides
  - `08-mcp-servers.md` exists but not in presentation
  - Need to include in master generation

- [ ] **Test full pipeline**
  - Edit a curriculum module
  - Run `generate-all.sh`
  - Verify slides updated correctly

- [ ] **Update README** with new workflow documentation

- [ ] **Optional: Add CI/CD**
  - Auto-regenerate on curriculum changes
  - Auto-commit generated files

---

## 1. Standardize Your Markdown Structure

### Slide-Friendly Markdown Patterns

Create consistent patterns that convert cleanly to slides:

```markdown
# Slide Title
## Optional Subtitle

Main content here:
- Bullet point 1
- Bullet point 2
- Bullet point 3

Additional paragraph text if needed.

---

# Next Slide
```

### Content Length Guidelines

**Establish limits that always fit:**
- **Titles**: Max 60 characters (fits in 38-40pt font)
- **Subtitles**: Max 80 characters (fits in 24pt font)
- **Bullets**: Max 5-6 bullets per slide, 80 chars each
- **Paragraphs**: Max 3 short paragraphs (2-3 lines each)

**Validation script idea:**
```bash
# Check markdown for slides that will overflow
./scripts/validate-slide-content.py CE101-Master-Presentation.md
```

### Slide Type Markers

Use consistent patterns to identify slide types:

```markdown
# Module 1: Core Concepts    # Detected as "Module" → orange divider slide
## The Foundation

---

# Space Jam Theory           # Regular content slide
## If You Can Dream It

---

# Course Overview            # "Overview" keyword → special layout?
```

---

## 2. Build a Slide Template Library

### Create Reusable HTML Templates

Instead of inline HTML generation, create template files:

```
templates/
├── title-slide.html          # Dark background, orange accent
├── module-divider.html       # Full orange background
├── content-slide.html        # White, orange left bar
├── two-column-slide.html     # Text + visual side-by-side
├── code-example-slide.html   # For code blocks
├── comparison-slide.html     # Before/after, good/bad
└── takeaway-slide.html       # Summary slides
```

**Benefits:**
- Edit template once, applies to all slides of that type
- Easier to test layouts in isolation
- Can maintain multiple themes (Little Caesars orange, corporate blue, etc.)

### Template Selection Logic

```javascript
function selectTemplate(slide) {
  if (slide.index === 0) return 'title-slide.html';
  if (slide.title.includes('Module')) return 'module-divider.html';
  if (slide.hasCodeBlock) return 'code-example-slide.html';
  if (slide.bullets.length > 6) return 'two-column-slide.html'; // Overflow prevention
  return 'content-slide.html';
}
```

---

## 3. Incremental Generation & Testing

### Generate One Slide at a Time

When debugging, don't regenerate all 56 slides:

```bash
# Generate only slide 10 for testing
node workspace/generate-presentation.js --slide=10

# Generate slides 10-15 for batch testing
node workspace/generate-presentation.js --range=10-15

# Quick preview without validation
node workspace/generate-presentation.js --slide=10 --no-validate
```

### Rapid Iteration Workflow

```bash
# 1. Edit markdown
vim CE101-Master-Presentation.md

# 2. Generate just the changed slide
node workspace/generate-presentation.js --slide=10

# 3. Preview immediately
open slide-10-preview.jpg  # Auto-generated thumbnail

# 4. Iterate until happy
# Repeat steps 1-3

# 5. Full generation when ready
node workspace/generate-presentation.js --all
```

---

## 4. Content Preprocessing

### Markdown Extensions for Slides

Add slide-specific metadata to your markdown:

```markdown
---
slide_type: two_column
max_bullets: 4
font_scale: 0.9  # Reduce fonts by 10% for dense content
---

# Dense Technical Content
...lots of bullets...
```

### Auto-Splitting Long Content

```javascript
// Detect slides that will overflow and auto-split
function preprocessSlide(slide) {
  if (slide.bullets.length > 6) {
    return splitIntoTwoSlides(slide);
  }
  if (slide.title.length > 60) {
    return shortenTitle(slide); // "Module 1: Core Concepts" → "Core Concepts"
  }
  return slide;
}
```

---

## 5. Visual Design System

### Create a Design Config File

Store all styling in one place:

```javascript
// config/design-themes.js
export const themes = {
  littleCaesars: {
    colors: {
      primary: 'F96D00',
      secondary: 'E85D04',
      text: '222831',
      accent: '4A90A4',
    },
    fonts: {
      title: { family: 'Arial', size: 38, weight: 'bold' },
      subtitle: { family: 'Arial', size: 24, weight: 'normal' },
      body: { family: 'Arial', size: 16, weight: 'normal' },
    },
    spacing: {
      padding: 35,
      margin: 22,
      bulletIndent: 25,
    },
    layouts: {
      titleSlide: { accentBarWidth: 10, accentBarColor: 'primary' },
      contentSlide: { accentBarWidth: 8, accentBarColor: 'primary' },
    }
  },

  corporate: {
    // Different theme for different audience
    colors: { primary: '4472C4', ... },
    ...
  }
};
```

**Usage:**
```bash
# Generate with Little Caesars theme
node workspace/generate-presentation.js --theme=littleCaesars

# Generate with corporate theme
node workspace/generate-presentation.js --theme=corporate
```

---

## 6. Automated Validation & Fixing

### Pre-Flight Checks

Before generating full deck:

```javascript
// Check all slides will render correctly
const issues = [];
for (const slide of slides) {
  if (slide.title.length > 60) issues.push(`Slide ${i}: Title too long`);
  if (slide.bullets.length > 6) issues.push(`Slide ${i}: Too many bullets`);
  if (estimatedHeight(slide) > 405) issues.push(`Slide ${i}: Content overflow`);
}

if (issues.length > 0) {
  console.log('⚠️ Issues found:');
  issues.forEach(i => console.log('  -', i));
  console.log('\nRun with --auto-fix to attempt automatic corrections');
}
```

### Auto-Fix Common Issues

```javascript
// Automatic fixes for common problems
function autoFix(slide) {
  // Shorten long titles
  if (slide.title.length > 60) {
    slide.title = shortenTitle(slide.title);
  }

  // Split long bullet lists
  if (slide.bullets.length > 6) {
    const [slide1, slide2] = splitSlide(slide);
    return [slide1, slide2];
  }

  // Reduce font size for dense content
  if (estimatedHeight(slide) > 380) {
    slide.fontScale = 0.9;
  }

  return [slide];
}
```

---

## 7. Smart Defaults & Overrides

### Default to Safe Layouts

```javascript
// Conservative defaults that always work
const SAFE_DEFAULTS = {
  titleFontSize: 36,      // Slightly smaller than ideal, but always fits
  maxBullets: 5,          // Conservative limit
  padding: 40,            // Extra breathing room
  lineHeight: 1.3,        // Tighter than ideal, but prevents overflow
};

// But allow per-slide overrides via markdown
function parseSlideMetadata(content) {
  const match = content.match(/<!--\s*SLIDE:\s*(\{.*?\})\s*-->/);
  if (match) {
    return JSON.parse(match[1]);
  }
  return {};
}
```

**In markdown:**
```markdown
<!-- SLIDE: {"fontSize": 40, "padding": 30} -->
# Custom Styled Slide
```

---

## 8. CI/CD for Slide Generation

### Automated Pipeline

```yaml
# .github/workflows/generate-slides.yml
name: Generate Presentation

on:
  push:
    paths:
      - '*.md'
      - 'slides/modules/*.md'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: npm install -g pptxgenjs playwright
      - name: Generate slides
        run: |
          node workspace/generate-presentation.js --all
          node workspace/generate-presentation.js --thumbnails
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: presentations
          path: |
            *.pptx
            thumbnails/*.jpg
```

**Result**: Every markdown commit automatically generates updated slides

---

## 9. Content Authoring Guidelines

### Write Markdown for Slides, Not Documents

**Document-style (BAD for slides):**
```markdown
The verification pattern is important because it enables you to maintain
safety while increasing productivity. When AI generates code, you should
review it thoroughly, test it in development, then staging, and finally
production. This ensures that errors are caught early.
```

**Slide-style (GOOD):**
```markdown
# The Verification Pattern

Why this works:
- Verification easier than generation
- AI generates comprehensive code
- You verify logic and context
- Safety maintained, speed increased

**Flow**: Generate → Review → Test → Execute
```

### Use Visual Markers

```markdown
✅ **Good practices**
❌ **Bad practices**
🚨 **Warning**
💡 **Pro tip**

These render as colorable elements in your templates
```

---

## 10. Your Maintenance Workflow

### Daily Editing Workflow

```bash
# 1. Edit curriculum source (this is your work)
vim 06-practical-patterns.md

# 2. Generate everything (one command)
./scripts/generate-all.sh
# Output:
# 📚 Generating master markdown from curriculum...
# 🎨 Generating styled slides...
# 📸 Creating thumbnails...
# ✅ Done!

# 3. Review changes
open workspace/thumbnails/thumbnails-1.jpg

# 4. Commit source files only
git add 06-practical-patterns.md
git commit -m "Update Module 6: Add dry-run pattern"
```

### What to Track in Git

**Track (source of truth):**
- ✅ `01-*.md` through `08-*.md` - Curriculum modules
- ✅ `scripts/` - Generation scripts
- ✅ `workspace/generate-presentation.js` - Slide generator

**Don't track (generated):**
- ❌ `CE101-Master-Presentation.md` - Generated from modules
- ❌ `CE101-Master-Presentation-Styled.pptx` - Generated from master
- ❌ `workspace/thumbnails/` - Preview images

Add to `.gitignore`:
```
CE101-Master-Presentation.md
CE101-Master-Presentation-Styled.pptx
workspace/thumbnails/
workspace/slides-html/
```

### Your Directory Structure

```
ce101/
├── 01-core-concepts.md              ← EDIT (source)
├── 02-filesystem-organization.md    ← EDIT (source)
├── 03-multi-tab-orchestration.md    ← EDIT (source)
├── 04-local-data-stores.md          ← EDIT (source)
├── 05-integration-patterns.md       ← EDIT (source)
├── 06-practical-patterns.md         ← EDIT (source)
├── 07-common-pitfalls.md            ← EDIT (source)
├── 08-mcp-servers.md                ← EDIT (source)
├── CE101-Master-Presentation.md     ← GENERATED (don't edit)
├── CE101-Master-Presentation-Styled.pptx  ← GENERATED (don't edit)
├── scripts/
│   ├── generate-master-markdown.js  ← To create
│   ├── generate-all.sh              ← To create
│   └── validate-curriculum.sh       ← To create
└── workspace/
    ├── generate-presentation.js     ← Working ✅
    └── thumbnails/                  ← Generated previews
```

---

## 11. Progressive Enhancement

### Start Simple, Add Complexity Gradually

**Phase 1: Basic Generation**
- Plain text slides
- Simple layouts
- Single template per slide type

**Phase 2: Add Polish**
- Color schemes
- Accent bars
- Font variations

**Phase 3: Advanced Features**
- Two-column layouts
- Code highlighting
- Automatic slide splitting

**Phase 4: Automation**
- CI/CD pipeline
- Auto-validation
- Multi-theme support

Don't try to do everything at once. Get basic generation working, then iterate.

---

## 12. Learning from Errors

### Error Pattern Database

Track common errors and their fixes:

```javascript
// errors-database.js
export const commonFixes = {
  'overflows body by X': {
    solutions: [
      'Reduce font size by 2pt',
      'Reduce padding by 5pt',
      'Split into two slides',
      'Use two-column layout',
    ]
  },
  'too close to bottom edge': {
    solutions: [
      'Reduce bottom padding',
      'Remove last bullet point',
      'Reduce line spacing',
    ]
  },
};
```

### Self-Healing Generation

```javascript
async function generateWithRetry(slide) {
  let attempts = 0;
  let errors = [];

  while (attempts < 3) {
    try {
      return await html2pptx(slide);
    } catch (error) {
      errors.push(error);
      slide = applyFix(slide, error);
      attempts++;
    }
  }

  throw new Error(`Could not generate slide after 3 attempts:\n${errors.join('\n')}`);
}
```

---

## Recommended Tools to Build

### 1. Content Validator
```bash
./scripts/validate-content.sh *.md
# Checks: title length, bullet counts, code block rendering
```

### 2. Quick Preview
```bash
./scripts/preview-slide.sh master-presentation.md 15
# Generates and opens slide 15 in <2 seconds
```

### 3. Batch Theme Switcher
```bash
./scripts/apply-theme.sh little-caesars *.md
# Regenerates all presentations with new theme
```

### 4. Diff Viewer
```bash
./scripts/slide-diff.sh old.pptx new.pptx
# Shows visual diff of what changed
```

---

## Summary: Your Minimal Effort Workflow

**What you do:**

1. **Edit curriculum modules** (01-08 markdown files)
2. **Run one command** (`./scripts/generate-all.sh`)
3. **Review thumbnail grid** (quick visual check)
4. **Commit source files** (git add curriculum modules)

**What you NEVER do:**
- Open PowerPoint to edit slides
- Worry about layout overflow
- Apply theme colors manually
- Regenerate master markdown by hand
- Adjust font sizes or alignment

**What the system handles automatically:**
- Master markdown generation (from 8 modules)
- Template selection (title/module/content)
- Layout optimization
- Theme application (orange/Little Caesars)
- Slide generation (all 56 slides)
- Thumbnail previews
- Validation & error reporting

---

## Immediate Next Steps (In Priority Order)

### 1. Create Master Markdown Generator ⚠️ CRITICAL

**File**: `scripts/generate-master-markdown.js`

**Purpose**: Transform curriculum modules (01-08) into presentation markdown

**This is the missing link** - Without this, you're manually maintaining CE101-Master-Presentation.md which defeats the purpose.

### 2. Create One-Command Script

**File**: `scripts/generate-all.sh`

**Purpose**: Run entire pipeline (master gen → slides → thumbnails)

**Impact**: Reduces workflow from 3 commands to 1

### 3. Test Full Pipeline

Edit a module → Run generate-all.sh → Verify slides updated

### 4. Add Module 8 to Current Presentation

The `08-mcp-servers.md` module exists but isn't in current slides. The master generator will add it automatically.

### 5. Update README Documentation

Document the workflow for future you (and others)

---

## Success Criteria

✅ **You can edit any curriculum module**
✅ **Run one command to regenerate everything**
✅ **Preview changes in <1 minute**
✅ **Commit only source files (8 markdown modules)**
✅ **Never open PowerPoint**

The upfront investment in the master markdown generator will pay off immediately - you'll be able to update any module and get beautiful, consistently styled slides in seconds!
