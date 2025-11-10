# CE101 Slide Style Guide

**Purpose**: Create well-formatted, visually balanced slides from markdown that maximize space utilization without overcrowding.

**Philosophy**: Good markdown structure produces good slides. This guide documents patterns that work and patterns to avoid.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Slide Structure Templates](#slide-structure-templates)
3. [Content Density Guidelines](#content-density-guidelines)
4. [Common Issues and Solutions](#common-issues-and-solutions)
5. [Formatting Rules](#formatting-rules)
6. [Testing Workflow](#testing-workflow)

---

## Core Principles

### 1. Optimize for Slide Real Estate

**DO**: Fill available space without overcrowding
- 4-6 bullets with sub-bullets for depth
- Brief explanatory text where helpful
- Examples that illustrate key points

**DON'T**: Create sparse or overcrowded slides
- 2-3 bullets with no context (too sparse)
- 8+ bullets with no hierarchy (overcrowded)
- Walls of text with no visual breaks

### 2. Prevent Orphaned Text

**DO**: Keep related content together
- Integrate lead-in text with what follows
- Use bold formatting to highlight key phrases inline

**DON'T**: Create orphaned lines
- "Include:" on one line, bullets below
- "Example:" separated from the example
- Section headers with no content before bullets

### 3. Use Hierarchy Effectively

**DO**: Use sub-bullets for supporting details
- Main bullet: Key concept
  - Sub-bullet: Supporting detail
  - Sub-bullet: Example or explanation

**DON'T**: Flatten everything into top-level bullets
- Creates visual monotony
- Reduces information density
- Harder to scan

### 4. Format Code and Paths Consistently

**DO**: Use proper markdown formatting
- Code blocks (```) for multi-line examples
- Backticks (`) for inline paths and commands
- Clear syntax for command examples

**DON'T**: Mix formatting styles
- Some paths in backticks, others not
- Code examples without proper blocks
- Inconsistent formatting within same slide

---

## Slide Structure Templates

### Template 1: Simple Content Slide

```markdown
# Slide Title

**Brief subtitle or key insight**

- Main point with brief explanation
  - Supporting detail that adds context
  - Example or use case
- Second main point with context
  - Supporting detail
  - Another relevant detail
- Third main point
  - Context that helps understanding
  - Practical application

**Closing insight or takeaway**
```

**Why this works:**
- Clear hierarchy with main and sub-bullets
- 3-4 main bullets with 2 sub-bullets each = good density
- Opening and closing statements frame the content
- Visual balance without overcrowding

### Template 2: Before/After Comparison

```markdown
# Slide Title

**Setup or context statement**

❌ **Anti-pattern description:**
- Problem 1
- Problem 2
- Problem 3
- Why this fails

✅ **Best practice description:**
- Solution 1
- Solution 2
- Solution 3
- Why this works

**Key insight about the difference**
```

**Why this works:**
- Clear visual distinction (❌ vs ✅)
- Parallel structure for easy comparison
- Balanced content on both sides
- Closing statement reinforces learning

### Template 3: Code Example Slide

```markdown
# Slide Title

**Context about what this code demonstrates**

**Scenario/Use case:**

\```bash
# Main command or script
command --flag argument

# Another command showing usage
command2 --flag value
\```

**Benefits or key points:**
- Benefit 1
- Benefit 2
- Benefit 3

**Additional context or warning if needed**
```

**Why this works:**
- Context before code (explains the "why")
- Clean code block formatting
- Benefits/explanation after code
- Complete thought on single slide

### Template 4: List with Inline Context

```markdown
# Slide Title

**Overview statement that sets up the list**

Be descriptive and actionable. **Essential elements:**

- **Element name**: Brief description of what it means
  - Why it matters
  - When to use it
- **Second element**: Its description
  - Context about importance
  - Practical application
- **Third element**: What it represents
  - Supporting detail
  - Example or use case

**Closing statement that reinforces the pattern**
```

**Why this works:**
- Avoids orphaned "Include:" or similar lead-ins
- Bold element names create visual anchors
- Inline descriptions with sub-bullets add depth
- Integrated flow from intro to content to conclusion

### Template 5: Module Divider

```markdown
# Module N: Module Title

Brief description of what this module covers

---
```

**Why this works:**
- Clean and simple
- Provides visual break between sections
- Sets expectations for upcoming content

---

## Content Density Guidelines

### Optimal Bullet Count

**For content slides:**
- **Minimum**: 3 main bullets with sub-bullets (sparse below this)
- **Optimal**: 4-6 main bullets with 1-3 sub-bullets each
- **Maximum**: 7 main bullets (overcrowded beyond this)

**For comparison slides (❌ vs ✅):**
- 3-4 bullets per section
- Parallel structure between sections

### When to Add Sub-Bullets

**DO add sub-bullets when:**
- Main bullet needs clarification
- Concrete examples illustrate the point
- Supporting details add value
- Breaking down complex concepts

**DON'T add sub-bullets when:**
- Main bullet is self-explanatory
- Adding redundant information
- Creating excessive nesting (3+ levels)
- Sub-bullet is longer than main bullet

### Text Length Guidelines

**Main bullets:**
- 5-15 words ideal
- Can be full sentence or phrase
- Should be scannable at a glance

**Sub-bullets:**
- 3-10 words ideal
- Supporting details, not full explanations
- Keep concise and focused

**Opening/closing statements:**
- 1-2 sentences maximum
- Bold key phrases for emphasis
- Frame the content, don't repeat it

---

## Common Issues and Solutions

### Issue 1: Orphaned Lead-In Text

❌ **DON'T do this:**
```markdown
# Natural Language Communication

**Include:**

- What you're trying to accomplish
- What you're unsure about
- Where relevant files are
```

**Problem**: "Include:" is orphaned from the list, creating awkward visual break.

✅ **DO this instead:**
```markdown
# Natural Language Communication

**Talk naturally and be comprehensive. Include these elements:**

- What you're trying to accomplish
- What you're unsure about
- Where relevant files are
```

**Solution**: Integrate lead-in with its list in same sentence.

---

### Issue 2: Sparse Slides with Too Much Whitespace

❌ **DON'T do this:**
```markdown
# MCP Servers

**What they are:**

- Connect to external systems
- Extend AI capabilities
- Have context cost
```

**Problem**: Only 3 bullets, no depth, wasted space.

✅ **DO this instead:**
```markdown
# What Are MCP Servers?

**Connections to external systems and APIs**

- GitHub integration
  - Repository access, PR management
  - Issue tracking and discussions
- Cloud provider APIs
  - Azure resources, AWS infrastructure
- Issue tracking systems
  - Jira tickets, Azure DevOps work items

**They extend AI capabilities beyond local files**

**Key consideration**: Every MCP server has a context cost
```

**Solution**: Add sub-bullets, opening and closing context.

---

### Issue 3: Code Not Formatted as Code Blocks

❌ **DON'T do this:**
```markdown
# Tab Layout Example

Tab 1 (Blue): Application code
Tab 2 (Blue): Kubernetes manifests
Tab 3 (Green): Fix implementation
```

**Problem**: Looks like regular bullets, not code structure.

✅ **DO this instead:**
```markdown
# Tab Layout Example

**Scenario: Database connection errors**

\```
Tab 1 (Blue): Application code repository
  → Check connection string configuration

Tab 2 (Blue): Kubernetes manifests
  → Verify database secrets

Tab 3 (Green): Fix implementation
  → Apply configuration changes
\```
```

**Solution**: Use code blocks for structured layouts.

---

### Issue 4: Inconsistent Path Formatting

❌ **DON'T do this:**
```markdown
# File Paths

- Check /company/SRE/main.tf
- Update the helm/charts/values.yaml file
- Look at `/var/log/app.log`
```

**Problem**: Inconsistent formatting makes it hard to scan.

✅ **DO this instead:**
```markdown
# File Paths

**Always use absolute paths in backticks:**

- Check `/company/SRE/terraform/main.tf`
- Update `/company/SRE/helm/charts/api/values.yaml`
- Look at `/var/log/api-service/app.log`
```

**Solution**: Consistent backticks for all paths.

---

### Issue 5: No Visual Hierarchy

❌ **DON'T do this:**
```markdown
# The Audit Pattern

For each MCP server ask these questions
When did I last use this?
What specific task required it?
How many tools do I actually use?
Be ruthless about removal
```

**Problem**: No structure, hard to parse, no hierarchy.

✅ **DO this instead:**
```markdown
# The Audit Pattern

**Monthly review of installed MCP servers**

**For each server, ask yourself:**

1. **When did I last use this?**
   - If more than 2 weeks ago, consider removal

2. **What specific task required it?**
   - Can that task be done another way?

3. **How many tools do I actually use vs. total provided?**
   - High overhead for low utilization?

**Be ruthless about removal** - You can always reinstall later
```

**Solution**: Use numbered lists, bold questions, sub-bullets for context.

---

## Formatting Rules

### Bold Text

**Use bold for:**
- Key concepts and principles
- Section headers within slides
- Questions in Q&A format
- Emphasis on critical points
- Slide subtitles

**Don't overuse:**
- More than 2-3 bold phrases per slide gets busy
- Entire bullets should rarely be bold
- Bold loses impact when overused

### Code Formatting

**Use code blocks (```) for:**
- Multi-line commands
- Script examples
- Bash/shell commands
- File structure diagrams
- Tab layout examples
- Any structured technical content

**Use inline backticks (`) for:**
- File paths: `/company/SRE/helm/values.yaml`
- Commands: `kubectl get pods`
- Flags: `--dry-run`
- Variables: `NAMESPACE=production`
- Technical terms: `values.yaml`

### Emojis

**Use strategically:**
- Color coding tabs: 🟢 🔵 🟡 🔴
- Checkmarks/X marks: ✅ ❌
- Keep consistent throughout deck
- Don't overuse (1-2 per slide max)

**Standard patterns:**
- ✅ for correct/recommended approaches
- ❌ for incorrect/anti-patterns
- 🟢🔵🟡🔴 for tab color coding

### Lists

**Bullet lists:**
- Use `-` for bullets (not `*` or `+`)
- Indent sub-bullets with 2 spaces
- Maximum 2 levels of nesting
- Keep parallel structure

**Numbered lists:**
- Use for sequences or priority
- Use for step-by-step instructions
- Format: `1. **Question/Step**: Details`

---

## Testing Workflow

### Generate and Review Incrementally

**DON'T**: Write 53 slides then generate once
- Can't see formatting issues until the end
- Massive rework if pattern is wrong
- Hard to track which slides need fixes

**DO**: Generate in batches of 5-10 slides
1. Write 5-10 slides
2. Run `./scripts/generate-slides.sh`
3. Review generated slides in browser
4. Fix formatting issues immediately
5. Repeat for next batch

**Benefits:**
- Catch issues early
- Refine patterns as you go
- Build muscle memory for good patterns
- Less rework at the end

### Pre-Flight Checklist

Before generating final deck, check:

- [ ] All slides have 4-6 bullets (or good reason for deviation)
- [ ] No orphaned "Include:", "Example:", etc.
- [ ] All code examples in proper code blocks
- [ ] All file paths in backticks or code blocks
- [ ] Consistent use of ✅ and ❌ for comparisons
- [ ] Sub-bullets add value, not redundancy
- [ ] Opening/closing statements frame content
- [ ] No walls of text without visual breaks
- [ ] Tab examples formatted as code blocks
- [ ] Consistent formatting within each slide type

### Quick Visual Check

Open `workspace/thumbnails/index.html` and scan thumbnails:

**Red flags to look for:**
- Lots of whitespace = too sparse
- Dense text block = overcrowded
- Uneven slides = inconsistent formatting
- Orphaned single lines at top of slides
- Missing code block formatting (looks like bullets)

**Good signs:**
- Balanced text distribution
- Clear visual hierarchy
- Consistent slide density
- Clean code block formatting
- Visual variety with sub-bullets

---

## Common Slide Types Reference

### Content Slide (Standard)
```markdown
# Title
**Subtitle**
- Bullet with sub-bullets
**Closing**
```

### Comparison Slide
```markdown
# Title
**Context**
❌ **Anti-pattern:**
- Problems
✅ **Best practice:**
- Solutions
**Insight**
```

### Code Example
```markdown
# Title
**Context**
\```bash
code here
\```
**Benefits:**
- List
```

### Process/Steps
```markdown
# Title
**Overview**
**Phase 1: Name**
- Steps
**Phase 2: Name**
- Steps
```

### List with Context
```markdown
# Title
**Overview. Essential elements:**
- **Item**: Description
  - Details
**Closing**
```

---

## Quick Do's and Don'ts

### DO:
✅ Use sub-bullets for depth and context
✅ Add opening/closing statements to frame content
✅ Format all code/paths consistently
✅ Test in small batches (5-10 slides at a time)
✅ Integrate lead-in text with its content
✅ Use 4-6 main bullets for optimal density
✅ Bold key concepts for emphasis
✅ Keep parallel structure in comparisons

### DON'T:
❌ Create orphaned "Include:" or "Example:" lines
❌ Leave sparse slides with just 2-3 bullets
❌ Mix formatted and unformatted paths
❌ Flatten everything into top-level bullets
❌ Write 53 slides then test once
❌ Overcrowd with 8+ bullets per slide
❌ Use different emoji patterns inconsistently
❌ Skip opening/closing context statements

---

## When to Break the Rules

These guidelines are patterns, not laws. Break them when:

- **Module dividers**: Intentionally simple (title + subtitle only)
- **Title slide**: Special formatting for visual impact
- **Closing slide**: Can be minimal for effect
- **Dense technical content**: May need more bullets if essential
- **Visual variety**: Occasionally vary pattern for interest

**Key principle**: Break rules intentionally, not accidentally.

If you break a guideline, know why and ensure it improves the slide.

---

## Measuring Success

A well-formatted slide should:
- Be scannable in 3-5 seconds
- Have clear visual hierarchy
- Fill space without feeling crowded
- Use formatting that aids comprehension
- Match patterns from rest of deck

**The ultimate test**: Can someone understand the key point without reading every word?

If yes → good slide
If no → needs more visual structure
