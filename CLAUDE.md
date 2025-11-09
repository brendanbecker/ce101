# CLAUDE.md

This file provides guidance to Claude Code when working with the Context Engineering 101 training repository.

## Project Overview

This is an educational training course teaching SREs (Site Reliability Engineers) and developers how to work effectively with AI coding assistants through **Context Engineering** - the practice of providing AI assistants with the right information in the right format.

**Key Philosophy**: Stop writing prompts, start engineering context. This course teaches practitioners to build systems that give AI everything it needs to understand their work.

## Repository Structure

```
ce101/
├── README.md                           # Course overview and navigation
├── 01-core-concepts.md                 # Module 1: Four context strategies
├── 02-filesystem-organization.md       # Module 2: Directory structure as context
├── 03-multi-tab-orchestration.md       # Module 3: Multiple specialized agents
├── 04-integration-patterns.md          # Module 4: Live queries vs local data
├── 05-practical-patterns.md            # Module 5: Real-world workflows
├── 06-common-pitfalls.md               # Module 6: What to avoid
├── 07-mcp-servers.md                   # Module 7: MCP server evaluation
├── quick-reference.md                  # One-page cheat sheet
├── workshop-exercises.md               # Hands-on practice activities
├── example-prompts.md                  # Copy-paste starting points
├── docs/                               # Workflow documentation and handoff notes
│   ├── SLIDE_WORKFLOW.md
│   ├── MARP_SLIDE_STANDARD.md
│   ├── HANDOFF_COMPLETE.md
│   └── EMOJI_ANALYSIS_REPORT.md
├── scripts/                            # Presentation generation scripts
│   ├── generate-slides.sh
│   ├── pptx-to-png.sh
│   └── view-slides.sh
├── archive/                            # Archived modules
│   └── 04-local-data-stores.md         # Archived: Module 4 (searchable inventories)
└── drafts/                             # Work-in-progress concepts for future integration
    ├── concepts-overview.md            # How new concepts relate to each other
    ├── integration-plan.md             # Strategy for curriculum updates
    ├── learning-while-working.md       # AI as teacher, dry-run patterns
    ├── mcp-servers-module.md           # Module 8: MCP server evaluation (draft)
    ├── natural-language-communication.md  # Effective AI interaction patterns
    ├── space-jam-theory.md             # Empowerment and exploration
    └── verification-accountability-patterns.md  # Safety and responsibility
```

## Core Concepts to Understand

### The Four Context Strategies

1. **Inline Context**: Information in the conversation (prompts, files, code)
2. **Filesystem Context**: Directory structure and file organization
3. **Environment Context**: Where the agent starts and what it can access
4. **External Context**: APIs, live queries, and runtime information

### Key Principles

- **One agent, one job**: Use multiple tabs for complex tasks
- **Filesystem is context**: Organize logically, start sessions in the right place
- **Build searchable ground truth**: Create local inventories for repeated queries
- **Tokens are cheap, clarity is expensive**: Use isolation over compression
- **The right tool for the right job**: Match context strategy to task needs

### Emerging Concepts (See drafts/)

New principles being developed for future curriculum integration:

- **"If you can dream it, you can do it"**: Empowerment to attempt complex tasks (Space Jam Theory)
- **Talk naturally with AI**: Expressing uncertainty triggers better explanations
- **AI as teacher**: Learn new tools and patterns while accomplishing tasks
- **Dry-run everything**: Safe testing mode is mandatory for operational scripts
- **Progressive verification**: Dev → Review → Prod workflow for new automation
- **You are accountable**: AI generates, you verify and execute
- **Selective MCP use**: Only install servers you'll use intentionally and frequently

## Working with This Repository

### Content Guidelines

**Tone and Style**:
- Practical, direct, SRE-focused
- Use real-world examples from infrastructure/ops work
- Balance theory with actionable advice
- Include code examples and file snippets where helpful

**Module Structure**:
Each module follows this pattern:
1. Overview and learning objectives
2. Core concepts with examples
3. Practical exercises or patterns
4. Common mistakes to avoid
5. Key takeaways

**Example Format**:
Use clear before/after examples showing ineffective vs effective approaches:
```markdown
### Example: [Scenario]

**Ineffective approach:**
[What not to do and why]

**Effective approach:**
[What to do instead and why it works]
```

### Common Tasks

**Adding New Content**:
- Maintain consistent module numbering (01-07)
- Follow existing markdown formatting conventions
- Include practical SRE/DevOps examples
- Add cross-references to related modules
- Update README.md table of contents if needed

**Updating Examples**:
- Use realistic infrastructure scenarios (Kubernetes, Terraform, CI/CD)
- Show actual file paths and directory structures
- Include both ineffective and effective approaches
- Explain the "why" behind recommendations

**Maintaining Slides**:
- Slides are stored in `slides/` directory
- Complete presentation deck: Sessions 1-7 correspond to modules 1-7
- Source PowerPoint files for presentations
- Keep slide content synchronized with markdown modules
- Session files use consistent naming: CE101_SessionN_Topic_Name.pptx

### File Organization Principles

This repository practices what it preaches:

1. **Logical grouping**: Related content in numbered sequence
2. **Clear naming**: Descriptive filenames with consistent patterns
3. **Flat structure**: Core modules at root level for easy discovery
4. **Support materials separated**: Slides, exercises, references in appropriate locations
5. **README as entry point**: Clear navigation and quick start paths

**Working with Drafts**:
- `drafts/` contains work-in-progress concepts being developed for future curriculum updates
- These represent new ideas and patterns not yet integrated into core modules
- Key concepts being explored:
  - **Space Jam Theory**: Empowerment to attempt complex tasks without self-limiting
  - **Natural Language Communication**: How to interact with AI more effectively
  - **Learning While Working**: AI as teacher, dry-run patterns, progressive verification
  - **Verification & Accountability**: Safety patterns for production work
  - **MCP Servers**: When to use/avoid, context cost evaluation
- `integration-plan.md` outlines strategies for weaving these into existing modules
- `concepts-overview.md` shows how all concepts relate to each other
- Review these drafts before making major curriculum changes

### Python Scripts

Supporting Python scripts for PowerPoint analysis:
- `analyze_pptx_unicode.py`: Analyzes Unicode usage in presentations
- `extract_pptx_text.py`: Extracts text content from slides
- `read_pptx.py`: Basic PowerPoint reading utility

These are utility scripts for content management, not core curriculum.

**Virtual Environment**:
- Python scripts require `python-pptx` package
- Virtual environment located at: `~/venvs/pptx-tools`
- Usage: `source ~/venvs/pptx-tools/bin/activate && python3 read_pptx.py <file>`

## Target Audience

**Primary**: SREs, DevOps engineers, platform engineers
**Secondary**: Software developers working with infrastructure

**Assumed Knowledge**:
- Command-line proficiency
- Git, Kubernetes, Terraform, or similar tools
- Basic programming/scripting experience
- Familiarity with AI coding assistants helpful but not required

## Course Delivery

**Workshop Format**:
- Core workshop: 3 hours (modules 1-3)
- Full course: 5-6 hours (all modules)
- Hands-on exercises throughout
- Apply learnings to real work

**Learning Paths**:

*New to AI assistants*:
1. Core Concepts
2. Filesystem Organization
3. Practical Patterns

*Experienced with AI assistants*:
1. Multi-Tab Orchestration
2. Local Data Stores
3. Common Pitfalls

## Editing Guidelines

When working with course content:

1. **Maintain consistency**: Match tone, style, and format of existing modules
2. **Preserve examples**: Keep realistic infrastructure scenarios throughout
3. **Update cross-references**: If renaming or restructuring, check all links
4. **Test exercises**: Ensure workshop exercises are practical and completable
5. **Keep README current**: Update navigation and quick reference as needed

## Terminology

- **Context Engineering**: Providing AI with right information in right format
- **Agent**: An AI assistant instance (e.g., Claude Code tab)
- **Tab orchestration**: Using multiple specialized AI sessions
- **Ground truth**: Local reference data for consistent answers
- **Inline context**: Information provided directly in conversation
- **Filesystem context**: Information conveyed through directory structure

## License

MIT License - See README.md for full text

---

**Remember**: This course is about teaching others how to work with AI effectively. When editing, ask: "Does this help an SRE become more productive with AI tools?"
