# Module 2: Filesystem Organization

Your workspace structure is your context architecture. The way you organize files directly impacts how effectively AI assistants can help you.

---

## The Core Principle

**Start where relevant context lives.**

Where you launch an AI session determines what context it naturally has. For SRE work, this usually means starting at the team level (`/company/SRE/`) rather than drilling down to specific subdirectories.

You control what the AI sees through:
1. **Starting location** - where you `cd` before starting the session
2. **AGENTS.md files** - documentation that tells AI how things are organized
3. **Explicit paths in prompts** - directing AI to specific locations

---

## AGENTS.md: Your AI's Field Guide

Before diving into directory organization, understand this: **AGENTS.md is the single most important file for context engineering.**

### What is AGENTS.md?

A markdown file that tells AI coding assistants how to work with your codebase:
- Where things are located
- Common commands to run
- Project-specific conventions
- Workflows and patterns

**Key insight**: AGENTS.md saves you from repeating context every session. The AI reads it automatically when you start in that directory.

(Note: If you use Claude exclusively, you can name it `CLAUDE.md` instead.)

### Where to Place Them

Use AGENTS.md at multiple levels:

```
/company/
├── AGENTS.md                 # Portfolio: "We have SRE, Dev, QA teams"
├── SRE/
│   ├── AGENTS.md             # Team: "We use terraform, helm, ansible"
│   ├── terraform/
│   │   └── AGENTS.md         # Category: "These are our terraform repos"
│   └── helm/
│       └── service-a/
│           └── AGENTS.md     # Project: "This service's specific rules"
```

**Rule of thumb**:
- Portfolio level: What teams/projects exist
- Team level: What tools and workflows we use
- Category level: Which repos are in this category
- Project level: Specific rules for this codebase

### What Goes In AGENTS.md

Keep it simple. Answer these questions:

1. **What is this?** (1-2 sentence overview)
2. **What's the structure?** (directory tree with comments)
3. **Common commands?** (3-5 most-used commands)
4. **Key conventions?** (naming, workflows, deployment)

**Example /company/SRE/AGENTS.md**:
```markdown
# SRE Team Workspace

Infrastructure and operations for production systems.

## Structure
terraform/   # Infrastructure as Code (separate repos per project)
helm/        # Kubernetes charts (separate repos per service)
ansible/     # Configuration management
notes/       # Runbooks, incidents, decisions
scripts/     # Automation utilities

## Common Commands
- terraform plan - Preview infrastructure changes
- helmfile -e production sync - Deploy to production
- flux reconcile kustomization production - Sync GitOps

## Conventions
- All terraform changes require plan review
- Scripts must have dry-run mode
- Document decisions in notes/decisions/
```

### Why This Works

**Without AGENTS.md**:
```
You: "Update user-api helm chart memory to 1Gi"
AI: *searches everywhere*
AI: "Where are helm charts?"
You: "helm/charts/"
AI: *searches again*
```

**With AGENTS.md**:
```
You: "Update user-api helm chart memory to 1Gi"
AI: *reads AGENTS.md, knows helm/charts/ structure*
AI: "Done. Also adjusted requests proportionally. Review?"
```

---

## Directory Structure for SRE Teams

Organize by team, then by tool, with AGENTS.md at each level:

```
company/
├── AGENTS.md
├── SRE/
│   ├── AGENTS.md
│   ├── terraform/          # Separate repos for each project
│   │   ├── AGENTS.md
│   │   ├── azure-infra/    (.git)
│   │   └── k8s-clusters/   (.git)
│   ├── helm/               # Separate repos for each service
│   │   ├── AGENTS.md
│   │   ├── service-a/      (.git)
│   │   └── service-b/      (.git)
│   ├── ansible/
│   │   └── AGENTS.md
│   ├── notes/              # Shared documentation repo
│   │   ├── runbooks/
│   │   ├── incidents/
│   │   ├── inventory/
│   │   └── decisions/
│   ├── scripts/
│   │   ├── automation/
│   │   ├── utilities/
│   │   └── monitoring/
│   └── tmp/                # Temporary files (gitignored)
├── Dev/
│   └── AGENTS.md
└── QA/
    └── AGENTS.md
```

Team-based top level gives clear ownership. Tool-based second level prevents conflicts. Category-level AGENTS.md maps which repos exist.

### The Notes Directory

This is your context gold mine. Four subdirectories:

- **runbooks/** - Operational procedures (database-failover.md, pod-crashloop.md, etc.)
- **incidents/** - Post-mortems organized by date (2024-11.md) or severity (major-incidents/)
- **inventory/** - Local caches of frequently-needed data (JSON format preferred)
- **decisions/** - Architecture Decision Records numbered sequentially (001-kubernetes-cluster-sizing.md)

Keep formats consistent and searchable. The AI can parse structured markdown easily.

---

## Starting Sessions at the Right Level

**Bad: Too narrow**
```bash
cd /company/SRE/helm/charts/user-api/
# Now you can only see this one chart
```

**Good: Start at team level**
```bash
cd /company/SRE/
# Now you can reference helm, terraform, notes, etc.
"Look in helm/charts/user-api/ and update memory to 1Gi"
```

**Why team-level is better**:
- Access to runbooks, other charts, terraform configs
- Can investigate across multiple systems
- AGENTS.md provides the map
- You use explicit paths in prompts to direct AI

**When to go deeper**: Only when you want to limit what the AI can access (large repos, prevent accidental changes to other services).

### Example: Cross-System Investigation

```
Understand our database failover process:
1. Search notes/runbooks/ for failover procedures
2. Check helm/charts/*/values.yaml for DB connection configs
3. Look in terraform/ for DB infrastructure setup
```

Starting at team level lets you investigate across multiple systems in a single prompt.

---

## Cross-Team Investigations

Sometimes SRE problems need dev repo investigation. Use **handoff prompts** to spawn focused subagents.

**Example**: From `/company/SRE/`, ask AI to draft a handoff prompt:
```
We have 500 errors from user-api. Checked helm config (correct),
DB is healthy, errors started after latest deploy.

Draft a handoff prompt for investigating /company/Dev/user-api/
```

AI generates:
```markdown
## Problem: Database connection timeouts in user-api

## Ruled Out (SRE investigation)
- Helm config correct (pool size: 50)
- Database healthy, started after deploy at 14:23 UTC

## Investigate in Dev Repo
- Database connection handling code
- Recent changes to connection pooling
- Hardcoded timeouts overriding config

## Context: commit abc123def, 15% error rate
```

Open new tab at `/company/Dev/user-api/`, paste handoff, investigate. Each agent gets the right AGENTS.md and focused scope.

(Module 5 covers multi-tab orchestration in depth.)

---

## Git Organization

Use separate repos, organized by category. Category-level AGENTS.md files map which repos exist:

```
/company/SRE/terraform/
├── AGENTS.md           # "We have azure-infra, k8s-clusters, networking repos"
├── azure-infra/        (.git)
├── k8s-clusters/       (.git)
└── networking/         (.git)
```

This gives each repo independent versioning while letting you work across multiple repos from the category level.

---

## Practical Exercise

### Step 1: Create Your First AGENTS.md

Start at team level:

```bash
cd /company/SRE/
vi AGENTS.md
```

Include:
- What this directory contains (1-2 sentences)
- Directory structure (top-level, with comments)
- 3-5 common commands
- Key conventions

### Step 2: Create Notes Structure

```bash
mkdir -p notes/{runbooks,incidents,inventory,decisions}
mkdir -p scripts/{automation,utilities,monitoring}
mkdir -p tmp
```

### Step 3: Test with AI

```bash
cd /company/SRE/
# Start AI session
"Based on AGENTS.md, show me where helm charts are and list available services"
```

If AI finds them easily, your structure works.

### Step 4: Iterate

Notice what questions AI asks repeatedly? Add those answers to AGENTS.md.

---

## Action Items

1. **Create team-level AGENTS.md** - Single biggest impact. Takes 10 minutes, saves hundreds of tokens per session.

2. **Create notes/ structure** - Even empty, it signals where docs should go: `notes/{runbooks,incidents,inventory,decisions}`

3. **Use consistent naming** - Pick a convention, stick to it across all directories.

4. **Start sessions at team level** - Stop navigating deep. Start at `/company/SRE/` and use explicit paths in prompts.

5. **Add category AGENTS.md** - In terraform/, helm/, etc. to map which repos exist.

6. **Test and iterate** - Ask AI to find something. Notice what it asks for repeatedly? Add to AGENTS.md.

---

**[← Back to Core Concepts](01-core-concepts.md)** | **[MCP Servers →](03-mcp-servers.md)**
