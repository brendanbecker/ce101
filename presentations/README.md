# CE101 Presentation Materials

This directory contains all materials related to the Context Engineering 101 presentation slidedecks, separate from the core curriculum markdown files.

## Directory Structure

```
presentations/
├── README.md                          # This file - presentation workflow overview
├── pptx/                              # PowerPoint presentation files
│   ├── CE101-Master-Presentation.pptx
│   ├── CE101-Master-Presentation-Improved.pptx
│   └── CE101-Master-Presentation-Styled.pptx
├── sources/                           # Markdown sources for slides
│   └── CE101-Master-Presentation.md
├── scripts/                           # Generation and conversion tools
│   ├── generate-presentation.js       # Node.js presentation generator
│   ├── generate-slides.sh            # Shell wrapper for slide generation
│   ├── pptx-to-png.sh                # Convert PowerPoint to PNG images
│   ├── view-slides.sh                # View slides in terminal
│   ├── analyze_pptx_unicode.py       # Analyze Unicode usage in presentations
│   ├── extract_pptx_text.py          # Extract text content from slides
│   ├── read_pptx.py                  # Basic PowerPoint reading utility
│   └── combine_presentations.py      # Combine multiple presentations
└── docs/                              # Workflow documentation
    ├── SLIDE_WORKFLOW.md              # Step-by-step slide creation process
    ├── MARP_SLIDE_STANDARD.md         # Marp markdown standards
    ├── SLIDE_CREATION_POSTMORTEM.md   # Lessons learned from slide creation
    ├── CE101-SLIDE-STYLE-GUIDE.md     # Style guide for presentations
    ├── EMOJI_ANALYSIS_REPORT.md       # Unicode/emoji usage analysis
    └── HANDOFF_COMPLETE.md            # Project handoff documentation
```

## Quick Start

### Viewing Slides

```bash
# View slides in terminal
cd presentations/scripts
./view-slides.sh ../pptx/CE101-Master-Presentation-Styled.pptx
```

### Converting to PNG

```bash
# Convert PowerPoint to PNG images
cd presentations/scripts
./pptx-to-png.sh ../pptx/CE101-Master-Presentation-Styled.pptx
```

### Generating Slides from Markdown

```bash
# Generate slides from markdown source
cd presentations/scripts
./generate-slides.sh
```

## Python Tools

The Python scripts require the `python-pptx` package. Virtual environment located at: `~/venvs/pptx-tools`

### Usage Examples

```bash
# Activate virtual environment
source ~/venvs/pptx-tools/bin/activate

# Read PowerPoint structure
python3 scripts/read_pptx.py pptx/CE101-Master-Presentation.pptx

# Extract text content
python3 scripts/extract_pptx_text.py pptx/CE101-Master-Presentation.pptx

# Analyze Unicode usage
python3 scripts/analyze_pptx_unicode.py pptx/CE101-Master-Presentation.pptx

# Combine multiple presentations
python3 scripts/combine_presentations.py pptx/file1.pptx pptx/file2.pptx -o pptx/combined.pptx
```

## Documentation

For detailed information about the slide creation workflow, styling standards, and best practices, see:

- **[SLIDE_WORKFLOW.md](docs/SLIDE_WORKFLOW.md)** - Complete workflow from markdown to final presentation
- **[CE101-SLIDE-STYLE-GUIDE.md](docs/CE101-SLIDE-STYLE-GUIDE.md)** - Visual and content styling standards
- **[MARP_SLIDE_STANDARD.md](docs/MARP_SLIDE_STANDARD.md)** - Marp markdown format specifications
- **[SLIDE_CREATION_POSTMORTEM.md](docs/SLIDE_CREATION_POSTMORTEM.md)** - Lessons learned and best practices

## Relationship to Curriculum

The core Context Engineering 101 **curriculum** lives in the repository root:

- `01-core-concepts.md` through `06-patterns-and-antipatterns.md`
- `README.md`, `quick-reference.md`, `workshop-exercises.md`, `example-prompts.md`

This `presentations/` directory contains the **delivery materials** (slidedecks) that accompany the written curriculum.

## File Versions

Multiple versions of the master presentation exist:

- **CE101-Master-Presentation.pptx** - Original version
- **CE101-Master-Presentation-Improved.pptx** - Enhanced version with improvements
- **CE101-Master-Presentation-Styled.pptx** - Final styled version for delivery

Refer to `docs/SLIDE_CREATION_POSTMORTEM.md` for version history and evolution.
