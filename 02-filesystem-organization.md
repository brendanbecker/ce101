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

**Example /company/SRE/terraform/AGENTS.md** (category level):
```markdown
# Terraform Repositories

## Repos in this directory
- `azure-infrastructure/` - Cloud resources (Platform team)
- `kubernetes-clusters/` - AKS setup (SRE team)
- `networking/` - VNets, DNS, load balancers (Network team)

Each repo uses terraform workspaces for dev/staging/prod.
State stored in Azure Storage. Always review plan before apply.
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

**Why this works**:
- **Team-based top level**: Clear ownership, natural context boundaries
- **Tool-based second level**: Each tool has its namespace, prevents conflicts
- **Category-level AGENTS.md**: Maps which repos exist in each category
- **Separate repos**: Independent lifecycles, clear ownership

### The Notes Directory

This is your context gold mine. Four subdirectories:

**runbooks/** - Operational procedures
```
runbooks/
├── database-failover.md
├── disk-space-alerts.md
└── pod-crashloop.md
```

**incidents/** - Post-mortems and historical learning
```
incidents/
├── 2024-11.md
├── 2024-10.md
└── major-incidents/
    └── 2024-09-15-database-outage.md
```

**inventory/** - Local caches of frequently-needed data
```
inventory/
├── azure-resources.json
├── work-items.json
└── helm-charts-index.json
```

**decisions/** - Architecture Decision Records (ADRs)
```
decisions/
├── 001-kubernetes-cluster-sizing.md
├── 002-monitoring-strategy.md
└── template.md
```

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

### Example Prompts from SRE Level

**Focused task**:
```
Look in helm/charts/user-api/ and update resource limits to 1Gi memory.
We're seeing OOMKilled pods at peak traffic. Check current limits first.
```

**Cross-system investigation**:
```
Understand our database failover process:
1. Search notes/runbooks/ for failover procedures
2. Check helm/charts/*/values.yaml for DB connection configs
3. Look in terraform/ for DB infrastructure setup
```

**Exploratory search**:
```
Find all helm charts using nginx-ingress. We're upgrading to v1.5.
Check Chart.yaml dependencies, ingress templates, and annotations.
```

---

## Cross-Team Investigations

Sometimes SRE problems need dev repo investigation. Use **handoff prompts** to spawn focused subagents.

### Quick Example

From `/company/SRE/`:
```
We have 500 errors from user-api. Checked helm config (correct),
DB is healthy, errors started after latest deploy. Seems like an
application code issue with connection pooling.

Draft a handoff prompt for investigating /company/Dev/user-api/
```

AI generates structured handoff:
```markdown
## Problem: Database connection timeouts in user-api

## Ruled Out (SRE investigation)
- Helm config correct (pool size: 50)
- Database healthy
- Started after deploy at 14:23 UTC

## Investigate in Dev Repo
- Database connection handling code
- Recent changes to connection pooling
- Hardcoded timeouts overriding config
- Connection retry logic

## Context
- Deploy: commit abc123def
- Error rate: 15% of requests
```

**Then**: Open new tab at `/company/Dev/user-api/`, paste handoff, investigate.

**Why this works**: Each agent gets the right AGENTS.md, right context, focused scope. No token waste loading entire codebase into wrong session.

(Module 4 covers multi-tab orchestration in depth.)

---

## Git Organization

Use separate repos, organized by category in your filesystem:

```
/company/SRE/
├── terraform/
│   ├── AGENTS.md           # Maps the repos below
│   ├── azure-infra/        (.git)
│   ├── k8s-clusters/       (.git)
│   └── networking/         (.git)
├── helm/
│   ├── AGENTS.md           # Maps the chart repos
│   ├── service-a/          (.git)
│   ├── service-b/          (.git)
│   └── monitoring/         (.git)
└── notes/                  (.git - shared)
```

**Benefits**:
- Clear ownership per repo
- Independent versioning
- Category-level AGENTS.md explains which repos exist
- Work across multiple repos from category level

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

## Common Mistakes

### ❌ Flat Structure
```
/work/
├── script1.sh
├── chart-values.yaml
├── runbook.md
└── main.tf
```
No organization. AI can't determine context.

### ❌ Too Deep
```
/company/teams/infrastructure/sre/kubernetes/helm/charts/apps/backend/user-api/
```
16 levels deep. Nobody knows where they are.

**Rule of thumb**: 4-5 levels maximum.

### ❌ Inconsistent Naming
```
/company/
├── SRE/
├── dev-team/
├── QualityAssurance/
└── release_management/
```
Pick one style (kebab-case, snake_case, PascalCase) and be consistent.

---

## Quick Wins

1. **Create team-level AGENTS.md** - Single biggest impact. Takes 10 minutes, saves hundreds of tokens per session.

2. **Create notes/ directory** - Even empty, it signals where docs should go.

3. **Use consistent naming** - Pick a convention, stick to it.

4. **Start at team level** - Stop navigating to specific subdirectories. Start at `/company/SRE/` and use explicit paths.

5. **Add category AGENTS.md** - In terraform/, helm/, etc. Maps which repos exist.

---

## Summary

**Good filesystem organization**:
- Mirrors team structure
- Groups related files by tool/function
- Has AGENTS.md at multiple levels
- Uses consistent naming
- Includes notes/ for operational knowledge

**Benefits for Context Engineering**:
- AI reads AGENTS.md automatically
- Starting at team level gives broad access
- Explicit paths in prompts direct AI precisely
- No token waste on exploration
- Natural isolation between teams

**Key principle**: Start where relevant context lives (team/domain level), let AGENTS.md provide the map, use explicit paths to direct AI, only navigate deeper to limit scope.

---

## Next Steps

1. Create `/company/SRE/AGENTS.md` (or equivalent for your team)
2. Add notes/ structure
3. Test: start session at team level, ask AI to find something
4. Iterate: add to AGENTS.md based on what AI asks for

---

**[← Back to Core Concepts](01-core-concepts.md)** | **[MCP Servers →](03-mcp-servers.md)**
