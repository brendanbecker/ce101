# Context Engineering 101 for SREs

A practical guide to working effectively with AI coding assistants like Codex and Claude Code.

## What is Context Engineering?

Context Engineering is the practice of providing AI assistants with the right information, in the right format, so they can help you accomplish tasks effectively. It's not about writing clever prompts—it's about building systems that give the AI everything it needs to understand your work.

## Course Structure

This training consists of six modules designed for SRE teams:

1. **[Core Concepts](01-core-concepts.md)** - The four context strategies and foundational principles
2. **[Filesystem Organization](02-filesystem-organization.md)** - Using your directory structure as context architecture
3. **[MCP Servers](03-mcp-servers.md)** - When and why to use Model Context Protocol servers
4. **[Multi-Tab Orchestration](04-multi-tab-orchestration.md)** - Managing multiple specialized agents
5. **[Patterns and Anti-Patterns](05-patterns-and-antipatterns.md)** - Real-world workflows and critical mistakes to avoid
6. **[Skills Pattern](06-skills-pattern.md)** - Package team expertise as discoverable, composable capabilities

## Quick Start

If you're new to AI-assisted development:

1. Read **Core Concepts** to understand the fundamentals
2. Try the exercises in **Filesystem Organization**
3. Practice with a real task using **Patterns and Anti-Patterns**

If you're already using AI assistants:

1. Understand **MCP Servers** early to make informed tool decisions
2. Jump to **Multi-Tab Orchestration** to level up your workflow
3. Study **Patterns and Anti-Patterns** for real-world workflows and critical mistakes to avoid

## Key Takeaways

- **Stop writing prompts, start engineering context** - Give the AI what it needs to succeed
- **One agent, one job** - Use multiple tabs for complex tasks
- **Your filesystem is your context** - Organize logically and start sessions in the right place
- **Build searchable ground truth** - Create local inventories for repeated queries
- **Tokens are cheap, clarity is expensive** - Use isolation over compression

## Prerequisites

- Familiarity with command-line tools
- Experience with git, kubernetes, terraform, or similar infrastructure tools
- Access to Codex, Claude Code, or similar AI coding assistant

## Time Commitment

- **Core workshop**: 3 hours (modules 1-3)
- **Full course**: 6-7 hours (all modules)
- **Ongoing practice**: Apply to daily work

## Additional Resources

- [Quick Reference Card](quick-reference.md) - One-page cheat sheet
- [Workshop Exercises](workshop-exercises.md) - Hands-on practice activities
- [Example Prompts](example-prompts.md) - Copy-paste starting points

## Slide Generation Workflow

The course includes presentation slides that are generated from a master markdown file.

### Workflow

1. **Edit curriculum modules** (01-08.md) - These are the source of truth
2. **Update master presentation** with Claude Code's help:
   - Edit `CE101-Master-Presentation.md`
   - Follow [CE101 Slide Style Guide](docs/CE101-SLIDE-STYLE-GUIDE.md) for formatting
   - Extract key concepts from curriculum modules
   - Create slide-friendly versions of content
   - Generate in batches of 5-10 slides (see [workflow docs](docs/SLIDE_WORKFLOW.md))
3. **Generate slides automatically**:
   ```bash
   ./scripts/generate-slides.sh
   ```

This will:
- Generate styled PowerPoint: `CE101-Master-Presentation-Styled.pptx`
- Create PNG previews: `workspace/thumbnails/`
- Build HTML index for browsing slides

### Quick Commands

```bash
# Generate PowerPoint and PNG previews
./scripts/generate-slides.sh

# View slides in browser
./scripts/view-slides.sh

# Convert any PowerPoint to PNGs
./scripts/pptx-to-png.sh <file.pptx> [output-dir]
```

### Source Files (Edit These)

- `01-core-concepts.md` through `07-mcp-servers.md` - Curriculum modules
- `CE101-Master-Presentation.md` - Master slide deck markdown

### Generated Files (Don't Edit)

- `CE101-Master-Presentation-Styled.pptx` - PowerPoint output
- `workspace/thumbnails/` - PNG preview images
- `workspace/slides-html/` - Intermediate HTML files

Generated files are in `.gitignore` and should not be committed.

### Documentation

- **[CE101 Slide Style Guide](docs/CE101-SLIDE-STYLE-GUIDE.md)** - Markdown patterns, templates, and formatting rules
- **[Slide Workflow](docs/SLIDE_WORKFLOW.md)** - Complete generation workflow with troubleshooting
- **[Slide Creation Postmortem](docs/SLIDE_CREATION_POSTMORTEM.md)** - Lessons learned from initial creation

## Getting Help

Questions or feedback? Add them to the team wiki discussion page or bring them to office hours.

---

**Ready to get started?** Begin with [Core Concepts →](01-core-concepts.md)

## License

MIT License

Copyright (c) 2025 Brendan Becker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
