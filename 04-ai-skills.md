# Module 4: AI Skills

Package team expertise as discoverable, composable capabilities that AI assistants can load on-demand.

---

## The Problem

Your team has expertise, but it's scattered:

- **In people's heads** - Not accessible to everyone
- **In stale documentation** - Wiki pages from 2 years ago
- **In scripts that can't explain** - They execute but don't teach
- **Not enforced** - Just "tribal knowledge"

**What you need**: A way to package team standards that is discoverable, self-documenting, composable, executable, versioned, and loads progressively.

---

## What Are AI Skills?

### Defining a Skill

A **skill** is a filesystem-based package containing:
- **Metadata**: What the skill does (YAML frontmatter in SKILL.md)
- **Instructions**: How the AI should use it (SKILL.md content)
- **Standards**: Team conventions, schemas, checklists (YAML/JSON files)
- **Automation**: Optional executable scripts (Python, Bash, etc.)
- **Examples**: Reference implementations

**Structure**:
```
.ai-skills/skill-name/
├── SKILL.md                # Metadata + AI instructions
├── standards.yaml          # Team requirements/templates
├── check-script.py        # Optional automation
└── examples/              # Success/failure cases
```

### Progressive Disclosure

**The insight**: AI assistants have unlimited potential context but limited actual tokens.

**How skills solve this**:
```
1. AI reads metadata (50 tokens): "production-readiness-review - Validates services"
2. User asks about production readiness
3. AI loads full skill (5000 tokens): Complete checklist, automation, examples
4. AI applies skill to user's service
```

**Result**: Zero tokens most of the time, full context when relevant.

### The Value Triangle

```
         Scripts
      (Deterministic)
            /\
           /  \
          /    \
         /      \
        /________\
    AI           Team Standards
(Flexible)       (Versioned)
```

**Skills combine all three**:
- Scripts provide deterministic validation
- AI provides flexible reasoning and explanation
- Standards provide versioned team knowledge

---

## Example Skill Ideas

### Production Readiness Review

Validates services meet production launch requirements.

**Contains**:
- `prr-requirements.yaml`: Team's checklist organized by category (monitoring, security, reliability, docs, observability)
- `check-prr.py`: Automated validation of Kubernetes resources, required files, security contexts
- Instructions for AI on interpreting results in context (tier-based requirements, service-type exceptions)

**AI adds value**: Explains what failures mean, suggests remediation, identifies when exceptions are reasonable.

---

### SLO Builder

Generates Service Level Objectives based on service tier and type.

**Contains**:
- `slo-templates.yaml`: SLO templates for tiers (99.9%, 99.5%, 99%) and types (HTTP API, gRPC, batch job, data pipeline)
- `build-slos.py`: Generates SLO definitions in preferred format
- Composes with PRR skill - reads tier metadata from PRR output

**AI adds value**: Determines service type from architecture, adjusts templates, explains tradeoffs, validates measurability.

---

### Helm Values Validator

Validates Helm values files against team conventions.

**Checks**: Required fields, naming conventions, resource limits, environment overrides, no plaintext secrets.

**AI adds value**: Explains conventions, suggests fixes, handles edge cases.

---

### Dockerfile Security Scanner

Checks Dockerfiles for security issues.

**Checks**: No `latest` tag, non-root user, no secrets in ENV, multi-stage builds, health checks.

**AI adds value**: Explains security implications, suggests refactoring, provides secure pattern examples.

---

### Incident Postmortem Generator

Creates postmortem documents from incident notes.

**Creates**: Timeline, root cause analysis, impact assessment, action items, lessons learned.

**AI adds value**: Structures messy notes, identifies root causes, generates actionable remediation.

---

## When to Use Skills

### Skills vs. Scripts

| Scenario | Use |
|----------|-----|
| One-time automation | Script |
| Repeated process with edge cases | Skill |
| Pure deterministic check | Script |
| Needs context and explanation | Skill |

### Skills vs. MCP Servers

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| Context cost | Zero until loaded | Constant |
| Best for | Team processes | Live external data |
| Versioning | Git | External system |

**Rule**: If you explain the same team standards repeatedly, codify them as a skill.

---

## Building Your Own Skills

### Quick Guide

**1. Identify the need**
- You repeatedly explain team standards
- Script exists but needs context to interpret
- Process is partially automated, partially judgment

*Keep skills focused*: "production-readiness-review" not "infrastructure-automation". One job per skill.

**2. Create structure**
```bash
mkdir -p .ai-skills/skill-name/{examples,scripts}
```

**3. Write SKILL.md**
```markdown
---
name: skill-name
description: One-line description
version: 1.0.0
category: operations
tags: [relevant, keywords]
---

## Purpose
Why this exists

## When to Use
Specific scenarios

## AI Instructions
How AI should use this skill
```

**4. Add standards file**
```yaml
standards:
  - id: STD-001
    name: Standard name
    description: What it requires
    rationale: Why it matters  # Critical - enables AI to explain
    severity: blocker|required|recommended
```

*Always include rationale* so AI can explain the "why", not just check compliance.

**5. Test with AI**
```
Ask AI: "Use the <skill-name> skill to check this"
Verify AI loads, runs, interprets correctly
Iterate until it works
```

**6. Version and commit**
```bash
git add .ai-skills/skill-name/
git commit -m "Add skill-name skill v1.0.0"
git tag skill-skill-name-v1.0.0
```

*Version properly*: Use semantic versioning. Update version in SKILL.md metadata when you make changes.

---

## Integration with Earlier Modules

**Module 1 (Core Concepts)**: Skills use SELECT strategy through progressive disclosure.

**Module 2 (Filesystem)**: Skills leverage filesystem as context - `.ai-skills/` is the discoverable location.

**Module 3 (MCP Servers)**: Skills for team standards, MCP for live external data. Skills can wrap MCP.

**Module 5 (Multi-Tab)**: Skills work across tabs because they're filesystem-based, not in-memory.

**Module 6 (Patterns)**: Skills embody safety patterns - dry-run modes, progressive verification, read vs execute.

---

## Summary

### What Skills Solve

1. Token budget constraints through progressive disclosure
2. Inconsistent standards through version-controlled knowledge
3. Scripts that can't explain through AI reasoning
4. Generic LLM knowledge through team-specific practices
5. Forgotten expertise through codified packages

### When to Create a Skill

**Create when**:
- ✅ Explaining same standards repeatedly
- ✅ Script needs context to interpret
- ✅ Process is partially automated, partially judgment
- ✅ Team does things inconsistently

**Don't create when**:
- ❌ Pure deterministic task
- ❌ One-time automation
- ❌ Generic knowledge

### Key Takeaways

1. **Progressive disclosure** - Load context only when needed
2. **Value triangle** - Scripts + AI + Standards
3. **Composability** - Skills work together naturally
4. **Platform agnostic** - Works with any AI that reads files
5. **Document rationale** - Enable AI to teach, not just check

---

**[← Back to MCP Servers](03-mcp-servers.md)** | **[Multi-Tab Orchestration →](05-multi-tab-orchestration.md)**
