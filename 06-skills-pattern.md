# Module 6: The Skills Pattern

Package team expertise as discoverable, composable capabilities that AI assistants can load on-demand.

---

## The Problem: Expertise Scattered Everywhere

### Scenario: The New Team Member

A new SRE joins your team. They ask: "How do I know if a service is ready for production?"

You could answer in three ways:

**Option 1: Verbal explanation** (15 minutes)
- Inconsistent across team members
- Not documented anywhere
- Forgotten details
- No traceability

**Option 2: Point to documentation** (if it exists)
- "Check the wiki for the PRR checklist"
- Wiki is 8 months out of date
- Doesn't explain *why* each requirement matters
- No automation to help

**Option 3: Share a script** (if it exists)
- Script checks some things automatically
- But can't explain context or handle edge cases
- "Why is this failing?" requires reading code
- Doesn't help you understand the *process*

### The Real Problem

Your team has expertise, but it's not **accessible, consistent, or composable**:

- **Expertise lives in people's heads** - Not in systems
- **Documentation gets stale** - No one maintains it
- **Scripts can't explain** - They execute but don't teach
- **Standards aren't enforced** - Just "tribal knowledge"
- **LLMs have generic knowledge** - Not *your team's* standards

### What We Need

A way to package team expertise that is:
1. **Discoverable** - AI can find it when relevant
2. **Self-documenting** - Explains what it does and why
3. **Composable** - Skills work together naturally
4. **Executable** - Can automate checks when possible
5. **Versioned** - Team standards evolve, skills evolve with them
6. **Progressive** - Load only what's needed, when it's needed

---

## The Skills Pattern

### What is a Skill?

A **skill** is a filesystem-based package containing:
- **Metadata**: What the skill does (YAML frontmatter in SKILL.md)
- **Instructions**: How the AI should use it (SKILL.md content)
- **Standards**: Team conventions, schemas, checklists (YAML/JSON files)
- **Automation**: Optional executable scripts (Python, Bash, etc.)
- **Examples**: Reference implementations showing success/failure cases

### Basic Structure

```
.ai-skills/skill-name/
├── SKILL.md                    # Metadata + instructions for AI
├── standards.yaml              # Team's requirements/templates
├── check-script.py            # Optional automation
└── examples/
    ├── passing-example/
    └── failing-example/
```

### The Key Insight: Progressive Disclosure

AI assistants face a fundamental challenge: **unlimited potential context, limited actual tokens**.

Skills solve this through **progressive disclosure**:

```
1. AI reads metadata (50 tokens): "production-readiness-review - Validates services for production launch"
2. User asks about production readiness
3. AI loads full skill (5000 tokens): Complete checklist, automation, examples
4. AI applies skill to user's service
```

**Without skills**: You'd paste the entire checklist into every conversation about production readiness.

**With skills**: AI loads it only when needed. Zero tokens most of the time, full context when relevant.

### The Value Triangle: Deterministic + Flexible + Versioned

Skills combine three things that individually are insufficient:

```
         Scripts
         (Deterministic)
            /\
           /  \
          /    \
         /      \
    AI           Team Standards
(Flexible)       (Versioned)
```

**Scripts alone**: Execute checks but can't reason about edge cases
**AI alone**: Generic knowledge, not your team's specific standards
**Standards alone**: Static documents that get out of date

**Skills = All three together**:
- Deterministic validation where automation is possible
- Flexible reasoning for context-specific decisions
- Versioned team standards that evolve with your practice

---

## Example Skill Ideas

Here are concrete examples of skills you might build for your team:

### 1. Production Readiness Review

**Purpose**: Validate that a service meets production launch requirements

**What it contains**:
- `prr-requirements.yaml`: Team's production checklist with requirements organized by category (monitoring, security, reliability, documentation, etc.)
- Each requirement has: description, rationale, severity (blocker/required/recommended), check type (automated/manual)
- `check-prr.py`: Automated script that validates Kubernetes resources, checks for required files, validates security contexts
- Instructions for AI on how to interpret results with context (e.g., "Tier-3 services have relaxed requirements", "Batch jobs don't need availability metrics")

**How AI adds value**:
- Runs automated checks and explains what they mean
- Interprets failures in context of service type and tier
- Suggests specific remediation steps
- Explains *why* each requirement matters for this specific service
- Identifies when exceptions are reasonable

**Example usage**:
```
User: "Check if my service is ready for production"
AI: [Loads production-readiness-review skill]
AI: [Runs check-prr.py script]
AI: "I found 3 blockers. The most critical is missing health checks -
     for a tier-1 service, this means pods won't be automatically
     restarted when they hang. Let me show you how to add them..."
```

---

### 2. SLO Builder

**Purpose**: Generate Service Level Objectives based on service tier and type

**What it contains**:
- `slo-templates.yaml`: SLO templates for different tiers (tier-1: 99.9%, tier-2: 99.5%, tier-3: 99%) and service types (HTTP API, gRPC, batch job, data pipeline)
- `build-slos.py`: Script that generates SLO definitions in your preferred format (Sloth, Prometheus, etc.)
- Composes with PRR skill - can read tier metadata from PRR output

**How AI adds value**:
- Determines appropriate service type from architecture
- Adjusts templates for service-specific needs
- Explains tradeoffs between SLO targets and cost
- Validates SLOs are measurable given current monitoring setup
- Suggests adjustments if templates don't fit

**Example composition**:
```
Step 1: User runs PRR → identifies "tier-1 HTTP API"
Step 2: User asks "Create SLOs for this service"
Step 3: AI loads SLO builder, reads tier from PRR metadata
Step 4: AI generates appropriate SLOs without asking for tier again
```

---

### 3. Helm Values Validator

**Purpose**: Validate Helm values files against team conventions

**What it checks**:
- Required fields present (image.repository, image.tag, resources)
- Naming conventions (services, deployments, configmaps)
- Resource limits within acceptable ranges (not too low, not wastefully high)
- Environment-specific overrides complete (prod has all required fields)
- Values don't contain secrets or sensitive data (should use secretRefs)

**How AI adds value**:
- Explains why conventions exist
- Suggests fixes for violations
- Handles edge cases (dev vs prod differences are expected)

---

### 4. Dockerfile Security Scanner

**Purpose**: Check Dockerfiles for security issues and best practices

**What it checks**:
- Base image not using `latest` tag (unpinned versions)
- Running as non-root user
- No secrets in build args or ENV
- Multi-stage builds for smaller images
- Minimal layers and proper caching
- Health check defined

**How AI adds value**:
- Explains security implications of each issue
- Suggests refactoring to fix issues
- Recommends base image alternatives
- Provides examples of secure patterns

---

### 5. Terraform Module Generator

**Purpose**: Scaffold Terraform modules following team conventions

**What it generates**:
- Standard directory structure
- variables.tf with required variables and descriptions
- outputs.tf with standard outputs
- README.md template with required sections
- examples/ directory with usage examples
- Appropriate provider configuration

**How AI adds value**:
- Customizes template based on module type (VPC, compute, database, etc.)
- Fills in sensible defaults based on team patterns
- Explains conventions and best practices as it generates

---

### 6. Incident Postmortem Generator

**Purpose**: Create incident postmortem document from notes

**What it creates**:
- Timeline of events from raw notes
- Root cause analysis section
- Impact assessment (customers affected, downtime duration)
- Action items with owners and deadlines
- Lessons learned
- Follow-up tasks

**How AI adds value**:
- Structures messy incident notes into clear narrative
- Identifies root causes from descriptions
- Generates actionable remediation items
- Suggests preventive measures based on root cause

---

### 7. Cost Optimization Analyzer

**Purpose**: Analyze infrastructure for cost optimization opportunities

**What it checks**:
- Resource requests vs actual usage patterns
- Over-provisioned workloads
- Idle resources (0 replicas, unused PVCs)
- Expensive storage classes where cheaper would work
- Opportunities for reserved instances or committed use discounts

**How AI adds value**:
- Explains cost implications in dollars
- Suggests right-sizing based on metrics
- Prioritizes optimization opportunities by potential savings
- Identifies risks in suggested changes

---

### 8. Changelog Formatter

**Purpose**: Transform git commits into team changelog format

**What it does**:
- Groups commits by type (feat, fix, chore, docs, breaking)
- Formats in team's changelog style
- Generates summary for release notes
- Links to issues/PRs
- Highlights breaking changes

**How AI adds value**:
- Interprets commit messages (even messy ones)
- Writes human-friendly descriptions
- Suggests version bump (major/minor/patch) based on changes
- Ensures important changes aren't buried

---

## Skills vs. Other Approaches

### When to Use Skills vs. Scripts

| Use Case | Scripts | Skills | Why |
|----------|---------|--------|-----|
| One-time automation | ✅ | ❌ | Script is simpler |
| Repeated process with edge cases | ❌ | ✅ | AI handles context |
| Team standard enforcement | ❌ | ✅ | Standards evolve, skills version them |
| Pure deterministic check | ✅ | ❌ | No AI needed |
| Needs explanation | ❌ | ✅ | AI explains why, not just what |

### When to Use Skills vs. MCP Servers

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| **Context cost** | Zero until loaded | Constant (tool schemas) |
| **Discovery** | Metadata in filesystem | Registered in config |
| **Versioning** | Git | External system |
| **Team-specific** | Perfect fit | Overkill |
| **Live queries** | Not designed for this | Perfect fit |
| **Best for** | Team processes, standards | External APIs, live data |

**Example scenarios**:

**Use MCP**: "What's the current CPU usage of this pod?" (live query, changes constantly)

**Use Skill**: "Does this service meet production standards?" (team-specific process, standards change slowly)

### When to Use Skills vs. Just Asking the LLM

| Scenario | Just Ask LLM | Use Skill | Why |
|----------|--------------|-----------|-----|
| "How do I write a Dockerfile?" | ✅ | ❌ | Generic knowledge |
| "What's our team's Dockerfile standard?" | ❌ | ✅ | Team-specific |
| "Explain Kubernetes readiness probes" | ✅ | ❌ | Well-known concept |
| "What does our PRR checklist require?" | ❌ | ✅ | Your standards |
| First time doing something | ✅ | ❌ | Learning mode |
| 10th time doing the same thing | ❌ | ✅ | Codify the pattern |

**The pattern**: If you find yourself explaining the same team standards repeatedly, codify them as a skill.

---

## Building Your Own Skills

### Step-by-Step Guide

**Step 1: Identify the Need**

Look for patterns where:
- You repeatedly explain team standards
- A script exists but needs context to interpret
- Process is partially automated, partially judgment
- Different team members do things differently

**Step 2: Define the Skill Structure**

```bash
mkdir -p .ai-skills/your-skill-name/{examples,schemas,scripts}
```

**Step 3: Write SKILL.md with Metadata**

```markdown
---
name: your-skill-name
description: One-line description of what it does
version: 1.0.0
category: [operations|security|development|compliance]
tags: [relevant, keywords]
requires_tools: [tools needed to run scripts]
composes_with: [other skills that work with this one]
---

# Your Skill Name

## Purpose
[Why this skill exists]

## When to Use
[Specific scenarios]

## How It Works
[Overview of automated + manual parts]

## AI Instructions
[How the AI should use this skill]

## Examples
[Point to examples directory]

## Related Skills
[Skills that compose with this one]
```

**Step 4: Create Team Standards File (YAML/JSON)**

```yaml
# your-standards.yaml
standards:
  - id: STD-001
    name: Clear standard name
    description: What this standard requires
    rationale: Why it matters
    severity: [blocker|required|recommended]
    check: [automated|manual]
```

**Step 5: Write Automation Script (Optional)**

Only if parts can be automated. Keep it simple - the AI provides the intelligence.

**Step 6: Create Examples**

Show both success and failure cases so AI learns what good/bad looks like.

**Step 7: Test with AI**

```
1. Navigate to directory with test case
2. Ask AI: "Use the <your-skill-name> skill to check this"
3. Verify AI loads metadata, runs script, interprets results
4. Iterate on instructions in SKILL.md until AI uses it correctly
```

**Step 8: Version and Document**

```bash
git add .ai-skills/your-skill-name/
git commit -m "Add <your-skill-name> skill v1.0.0"
git tag skill-your-skill-name-v1.0.0
```

### Skill Structure Conventions

**File naming**:
- `SKILL.md` - Always uppercase, contains metadata
- `*-requirements.yaml` or `*-standards.yaml` - Lowercase, descriptive
- `check-*.py` or `build-*.py` - Lowercase, verb-based
- `examples/` - Always plural

**Metadata fields** (YAML frontmatter in SKILL.md):
- `name`: Lowercase with hyphens (matches directory name)
- `description`: One clear sentence
- `version`: Semantic versioning (1.0.0)
- `category`: Single category for organization
- `tags`: Array of relevant keywords
- `requires_tools`: Tools needed to run
- `composes_with`: Skills this works well with

---

## Practical Exercises

### Exercise 1: Identify a Skill Opportunity

**Objective**: Find a repeated team process that would benefit from codification

**Tasks**:
1. List 3-5 things you explain to new team members repeatedly
2. Identify which involve both automation and judgment
3. Choose one that has the most repetition
4. Sketch out what a skill would contain

**Deliverable**: One-paragraph skill proposal

---

### Exercise 2: Create a Simple Skill

**Objective**: Build a minimal viable skill

**Choose one of these scenarios** (or create your own):

**Option A: README Quality Checker**
- Validates README files have required sections
- Checks for common missing information
- AI explains what each section should contain

**Option B: Git Commit Message Validator**
- Checks commits follow team convention
- Validates format, scope, and description
- AI suggests improvements for unclear messages

**Option C: Environment Variable Checker**
- Ensures required env vars are documented
- Checks for secrets that should use secret management
- AI explains security implications

**Tasks**:
1. Create skill directory structure
2. Write SKILL.md with metadata and instructions
3. Create standards YAML file
4. Add 1-2 examples
5. Test with AI on real data

**Deliverable**: Working skill ready for team use

---

### Exercise 3: Compose Two Skills

**Objective**: Demonstrate skills working together

**Scenario**: Create two skills that share data

**Example**:
- Skill A: Analyzes service and creates metadata file
- Skill B: Reads metadata from Skill A and generates config

**Tasks**:
1. Design the metadata format they'll share
2. Create both skills
3. Test the workflow end-to-end
4. Document the composition in both SKILL.md files

**Deliverable**: Two skills that compose naturally

---

## Common Pitfalls

### Pitfall 1: Skills Too Broad

**What it looks like**:
```
Skill name: "infrastructure-automation"
Description: "Automates all infrastructure tasks"
```

**Why it fails**:
- Too vague to load at the right time
- Tries to do everything, does nothing well
- Huge context cost when loaded

**The fix**:

Make skills **specific and focused**:
```
✅ Good:
  - production-readiness-review
  - dockerfile-security-scanner
  - helm-values-validator

❌ Too broad:
  - kubernetes-helper
  - deployment-automation
  - monitoring-setup
```

---

### Pitfall 2: Over-Engineering

**What it looks like**:

Simple deterministic task → Skill with extensive metadata, standards, examples, 500 lines of Python

**Why it fails**:
- Deterministic tasks don't need AI reasoning
- Just script is simpler and faster
- Maintenance overhead for no benefit

**The fix**:

**Use skills when**:
- AI adds value through reasoning
- Edge cases require context
- Team standards need explanation

**Use scripts when**:
- Pure deterministic transformation
- No context needed
- Same result every time

---

### Pitfall 3: Missing Rationale in Standards

**What it looks like**:

```yaml
requirements:
  - id: SEC-001
    name: Security context configured
    check: automated
    severity: blocker
```

No explanation of *why* it matters.

**The fix**:

**Always include rationale**:

```yaml
requirements:
  - id: SEC-001
    name: Security context configured
    description: Pod security context with runAsNonRoot
    check: automated
    severity: blocker
    rationale: |
      Defense in depth - limit container privileges to reduce
      blast radius if container is compromised. RunAsNonRoot
      prevents root exploits.
```

Now AI can explain the "why" to users.

---

### Pitfall 4: Skills Not Versioned

**What it looks like**:

Skills edited in place with no version tracking.

**Why it fails**:
- Can't reproduce past results
- Breaking changes surprise users
- Can't rollback problematic updates

**The fix**:

**Version skills properly**:

```yaml
---
name: production-readiness-review
version: 2.1.0  # Semantic versioning
---
```

**Update version when**:
- Major (3.0.0): Breaking changes
- Minor (2.1.0): New checks added
- Patch (2.0.1): Bug fixes

**Git tagging**:
```bash
git tag skill-production-readiness-review-v2.1.0
git push --tags
```

---

## Integration with Earlier Modules

### Module 1: Core Concepts - SELECT Strategy

Skills use the **SELECT** strategy through progressive disclosure.

**Traditional**: Paste 4000 token checklist into every conversation
**Skills**: 50 tokens for metadata, 5000 tokens only when needed

---

### Module 2: Filesystem Organization

Skills leverage **filesystem as context**:

```
.ai-skills/                          ← Discoverable location
├── production-readiness-review/     ← Skill name = directory name
│   ├── SKILL.md                     ← Metadata for discovery
│   └── requirements.yaml            ← Standards data
└── slo-builder/
    └── ...
```

Standard location makes skills discoverable.

---

### Module 3: MCP Servers

**Skills and MCP serve different purposes**:

| Use Case | MCP Server | Skill |
|----------|-----------|-------|
| Live external data | ✅ | ❌ |
| Team-specific standards | ❌ | ✅ |
| Real-time queries | ✅ | ❌ |
| Versioned team knowledge | ❌ | ✅ |
| Context cost | Constant | Zero until loaded |

**Skills can wrap MCP** for team-specific processes using live data.

---

### Module 4: Multi-Tab Orchestration

Skills work across tabs because they're **filesystem-based**, not in-memory.

```
Tab 1: "Use production-readiness-review to audit this service"
Tab 2: "Fix the issues found in Tab 1" [loads same skill]
Tab 3: "Re-run production-readiness-review" [verifies fixes]
```

---

### Module 5: Patterns and Anti-Patterns

Skills embody safety patterns:

- **Dry-Run**: Skills can include dry-run modes
- **Progressive Verification**: Test skills in dev → review → prod
- **Read vs Execute**: Skills READ and GENERATE, you EXECUTE
- **Accountability**: You verify skill recommendations before executing

---

## Summary

### The Skills Pattern Solves

1. **Token budget constraints**: Progressive disclosure loads only when needed
2. **Inconsistent standards**: Version-controlled team knowledge
3. **Scripts can't explain**: AI adds reasoning and context
4. **Generic LLM knowledge**: Skills encode your team's specific practices
5. **Forgotten expertise**: Codified in discoverable, self-documenting packages

### The Value Triangle

```
     Scripts (Deterministic)
            /\
           /  \
          /    \
         /      \
    AI           Team Standards
(Flexible)       (Versioned)
```

Skills combine all three: automated validation + flexible reasoning + versioned standards.

### When to Create a Skill

Create a skill when:
- ✅ You're explaining the same standards repeatedly
- ✅ A script exists but needs context to interpret
- ✅ Process is partially automated, partially judgment
- ✅ Team members do things differently and should be consistent

Don't create a skill when:
- ❌ Task is purely deterministic (just use a script)
- ❌ One-time automation (not repeated)
- ❌ Generic knowledge (LLM already knows this)

### Key Takeaways

1. **Progressive disclosure**: Load context only when needed
2. **Composability**: Skills work together naturally
3. **Platform agnostic**: Works with any AI that can read files
4. **Version everything**: Skills are code, treat them as such
5. **Document the why**: Rationale enables AI to teach, not just check

---

**[← Back to Patterns and Anti-Patterns](05-patterns-and-antipatterns.md)** | **[Quick Reference →](quick-reference.md)**
