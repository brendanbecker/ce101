# Module 2: Filesystem Organization

Your workspace structure is your context architecture. The way you organize files directly impacts how effectively AI assistants can help you.

---

## The Core Principle

**Start close to your work.**

Where you launch an AI session determines what context it naturally has. Starting in the right place means the agent immediately understands:
- What kind of work you're doing
- Where to look for related files
- What patterns and standards apply

---

## AGENTS.md as a First-Class Citizen

Before diving into directory organization, there's one file that deserves special attention: **AGENTS.md** (or **CLAUDE.md** if you exclusively use Claude).

This file is your AI harness's instruction manual for your codebase.

### What is AGENTS.md?

AGENTS.md is a markdown file that tells AI coding assistants how to work with your specific codebase. Think of it as:
- Onboarding documentation for AI
- A context guide that reduces token waste
- Project-specific rules and conventions
- A map of where things are and how they work

**Key principle**: Every repository and major subsystem should have one.

---

### Why Make It a First-Class Citizen?

**Without AGENTS.md**, the AI harness must:
1. Explore your codebase blindly
2. Guess at conventions and patterns
3. Search inefficiently for relevant files
4. Ask you clarifying questions repeatedly

**With AGENTS.md**, the AI harness:
1. Knows your project structure immediately
2. Understands your team's conventions
3. Finds the right files faster
4. Provides contextually appropriate suggestions

**Token savings**: A well-written AGENTS.md can save thousands of tokens per session by preventing exploration and wrong turns.

---

### Where to Place AGENTS.md Files

**Root-level AGENTS.md** - Portfolio overview:
```
/company/
├── AGENTS.md           # High-level: "This is a multi-project workspace"
├── SRE/
├── Dev/
└── QA/
```

**Team-level AGENTS.md** - Team context:
```
/company/SRE/
├── AGENTS.md           # SRE-specific: tools, workflows, conventions
├── terraform/
├── helm/
└── ansible/
```

**Project-level AGENTS.md** - Detailed project rules:
```
/company/SRE/helm/
├── AGENTS.md           # Helm-specific: chart standards, testing
├── charts/
└── values/
```

**Rule of thumb**:
- Root AGENTS.md: "What lives here and how things are organized"
- Team AGENTS.md: "How we work and what tools we use"
- Project AGENTS.md: "Specific rules, commands, and workflows for this codebase"

---

### What Goes in AGENTS.md

Here's a practical template based on real-world usage:

```markdown
# AGENTS.md

## Project Overview
Brief description: what this is, who owns it, primary purpose.

## Repository Structure
```
key-directory-1/  # What lives here
key-directory-2/  # What lives here
key-directory-3/  # What lives here
```

## Common Commands
```bash
# Run tests
pytest

# Deploy to staging
./scripts/deploy.sh staging

# Check infrastructure status
terraform plan
```

## Key File Locations
- Main configuration: `config/production.yaml`
- Test files: `tests/` (pytest)
- Deployment scripts: `scripts/deploy/`
- Documentation: `docs/`

## Development Workflows
1. Make changes in feature branch
2. Run tests locally: `make test`
3. Create PR against main
4. Deploy via GitOps after merge

## Testing Strategies
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- Load tests: `scripts/load-test.sh`

## Important Conventions
- Use kebab-case for file names
- All scripts must have error handling
- Terraform modules follow standard structure
- Helm charts use values/ directory for environments

## Environment Configuration
- `DATABASE_URL`: Required for tests
- `KUBE_CONTEXT`: Kubectl context to use
- `TERRAFORM_WORKSPACE`: Which workspace to target

## Common Pitfalls
- Don't run terraform apply without reviewing plan first
- Always test in dev environment before staging
- Check CHANGELOG.md before updates

## Related Documentation
- Architecture decisions: `docs/architecture/`
- Runbooks: `/company/SRE/notes/runbooks/`
- Team wiki: https://wiki.company.com/sre
```

**Customize this template** for your specific needs. The goal is to answer: "What does someone (or something) need to know to work here effectively?"

---

### Real Example: Multi-Project Repository

Here's an actual AGENTS.md from a multi-project portfolio:

```markdown
# AGENTS.md

## Project Portfolio Overview

This is a multi-project repository containing:
- **mtg_dev_agents**: Multi-agent system for game development
- **beckerkube**: Kubernetes infrastructure (GitOps)
- **montecarlo**: Simulation engine
- **mtgadvsim**: Game simulator core

## ⚠️ CRITICAL: Project-Specific AGENTS.md Files

Each project has its own detailed AGENTS.md:
- `mtg_dev_agents/AGENTS.md` - Agent protocols, testing patterns
- `beckerkube/AGENTS.md` - Security policies, GitOps workflows

**Before working on any project, read the relevant subdirectory
AGENTS.md file first.**

## Common Commands by Project

### beckerkube (Kubernetes Infrastructure)
```bash
# Security validation
./scripts/sec-lint.sh

# Flux reconciliation
flux reconcile kustomization clusters-minikube
```

### montecarlo (Simulation Engine)
```bash
# Run simulations
python phase4_simulation.py
```

## Key File Locations

### beckerkube
- Infrastructure manifests: `infra/` directory
- Security policies: `infra/security/`
- Cluster configs: `clusters/minikube/`
```

**What this accomplishes**:
- Root-level AGENTS.md provides portfolio map
- Points to project-specific AGENTS.md for details
- Shows common commands for quick reference
- Establishes the pattern: read subdirectory AGENTS.md

---

### AGENTS.md vs README.md

**README.md** is for humans:
- Project description and motivation
- Installation instructions
- Usage examples
- Contributing guidelines

**AGENTS.md** is for AI harnesses:
- Where things are located
- What commands to run
- Project-specific rules
- Context and conventions

**Both are valuable**. README helps humans understand *what* and *why*. AGENTS.md helps AI understand *how* and *where*.

**Example relationship**:
```
/company/SRE/helm/
├── README.md      # "This is our Helm chart repository for..."
├── AGENTS.md      # "Charts are in charts/, use helmfile for deploy..."
├── charts/
└── helmfile.yaml
```

---

### Benefits for Context Engineering

When you start a session at `/company/SRE/`:

**Without AGENTS.md**:
```
You: "Update the user-api helm chart resource limits"
AI: *searches entire SRE directory*
AI: "I found several directories. Where are the helm charts located?"
You: "In helm/charts/"
AI: *searches helm/charts/*
AI: "I found user-api. What resource limits did you want?"
```

**With AGENTS.md**:
```
You: "Update the user-api helm chart resource limits to 1Gi memory"
AI: *reads AGENTS.md, knows charts are in helm/charts/*
AI: *reads helm/charts/user-api/values.yaml*
AI: "Current memory limit is 512Mi. I'll update to 1Gi.
     Should I also adjust requests proportionally?"
```

**Token savings**: No exploration, no back-and-forth, context loaded immediately.

---

### How AGENTS.md Enables SRE-Level Starts

This is crucial: **AGENTS.md lets you start sessions at the SRE level** instead of drilling down to specific subdirectories.

**The traditional approach** (without AGENTS.md):
```bash
cd /company/SRE/helm/charts/user-api/  # Navigate deep
# Start AI session here for context
```

**The context-engineered approach** (with AGENTS.md):
```bash
cd /company/SRE/  # Start where relevant context is
# Start AI session here

# In your prompt, be explicit:
"Look in helm/charts/user-api/ and update the resource limits"
```

**Why this is better**:
1. You stay at the level where related context lives
2. You can reference multiple subsystems in one session
3. You only navigate deeper when you want to limit scope
4. AGENTS.md provides the map; you provide the specific directions

---

### Practical Tips

**Start small**:
Don't try to create the perfect AGENTS.md immediately. Begin with:
1. Project overview (2-3 sentences)
2. Directory structure (top-level only)
3. 3-5 most common commands
4. Key file locations

**Iterate based on usage**:
- Notice what questions AI asks repeatedly? Add to AGENTS.md.
- See it searching in wrong places? Update the structure section.
- Repeating the same context? Add to conventions.

**Keep it current**:
- Update AGENTS.md when you reorganize directories
- Add new commands as workflows evolve
- Remove outdated information promptly

**Version control**:
AGENTS.md should be committed to git alongside your code. It evolves with the project.

---

## Recommended Structure for SRE Teams

```
company/
├── AGENTS.md                           # Portfolio-level context
├── SRE/
│   ├── AGENTS.md                       # SRE team-level context
│   ├── terraform/
│   │   ├── AGENTS.md                   # Terraform-specific rules
│   │   ├── azure-infrastructure/
│   │   ├── kubernetes-clusters/
│   │   └── networking/
│   ├── helm/
│   │   ├── AGENTS.md                   # Helm chart standards
│   │   ├── charts/
│   │   │   ├── service-a/
│   │   │   ├── service-b/
│   │   │   └── ingress-nginx/
│   │   └── values/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── production/
│   ├── ansible/
│   │   ├── AGENTS.md                   # Ansible conventions
│   │   ├── playbooks/
│   │   └── roles/
│   ├── flux/
│   │   ├── AGENTS.md                   # GitOps workflow
│   │   └── clusters/
│   ├── notes/
│   │   ├── README.md                   # Human-readable guide
│   │   ├── runbooks/
│   │   ├── incidents/
│   │   ├── inventory/
│   │   └── decisions/
│   ├── scripts/
│   │   ├── README.md                   # Script organization guide
│   │   ├── automation/
│   │   ├── utilities/
│   │   └── monitoring/
│   └── tmp/
├── Dev/
│   ├── AGENTS.md                       # Dev team context
│   ├── app-repo-1/
│   ├── app-repo-2/
│   └── microservices/
├── QA/
│   ├── AGENTS.md                       # QA team context
│   ├── load-testing/
│   └── automation/
└── Release-Management/
    ├── AGENTS.md                       # Release management context
    ├── deployment-scripts/
    └── release-notes/
```

**Note**: Not every directory needs an AGENTS.md. Add them where you have:
- Significant project-specific rules or conventions
- Complex workflows that need explanation
- Common commands that should be documented
- Directory structures that aren't self-explanatory

---

## Why This Structure Works

### 1. Team-Based Top Level
```
/company/SRE/
/company/Dev/
/company/QA/
```

**Benefits**:
- Mirrors organizational boundaries
- Clear ownership and responsibility
- Natural context isolation between teams

**AI Advantage**: When you start in `/company/SRE/`, the agent knows it's working on infrastructure, not application code.

---

### 2. Tool-Based Second Level
```
/company/SRE/terraform/
/company/SRE/helm/
/company/SRE/ansible/
```

**Benefits**:
- Each tool has its own namespace
- Prevents config conflicts
- Easy to find related files

**AI Advantage**: Starting in `/terraform/` means the agent looks for `.tf` files and understands terraform patterns.

---

### 3. The Notes Directory
```
/company/SRE/notes/
├── runbooks/
├── incidents/
├── inventory/
└── decisions/
```

**This is your context gold mine.**

**Runbooks**: Searchable procedures
```
runbooks/
├── database-failover.md
├── pod-crashloop.md
├── disk-space-alerts.md
└── index.json  # Metadata for search
```

**Incidents**: Historical learning
```
incidents/
├── 2024-11.md
├── 2024-10.md
└── major-incidents/
    └── 2024-09-15-database-outage.md
```

**Inventory**: Local data stores
```
inventory/
├── azure-resources.json
├── work-items.json
├── helm-charts-index.json
└── last-updated.txt
```

**Decisions**: Architecture decision records
```
decisions/
├── 001-kubernetes-cluster-sizing.md
├── 002-monitoring-strategy.md
└── template.md
```

---

### 4. The Scripts Directory
```
/company/SRE/scripts/
├── automation/
├── utilities/
└── monitoring/
```

**Keep scripts organized by purpose**:
- **automation**: Deployment, scaling, routine tasks
- **utilities**: One-off helpers, data extraction
- **monitoring**: Custom metrics, health checks

**AI Advantage**: When generating scripts, agent can reference existing patterns in the same category.

---

### 5. The Tmp Directory
```
/company/SRE/tmp/
```

**Use for**:
- Downloaded logs
- Temporary analysis files
- One-off experiments
- Quick tests

**Important**: Keep this clean. Not for long-term storage.

**AI Usage**:
```
"Save the error logs to /company/SRE/tmp/service-errors.log for analysis"
```

---

## Starting Sessions in the Right Place

The right starting location depends on **where relevant context lives**, not how specific your task is.

**Core principle**: Start at the team or domain level (like `/company/SRE/`) and use explicit path mentions + AGENTS.md to guide the AI. Only navigate deeper when you want to limit the scope of what the AI can see.

---

### ❌ Too Broad
```bash
cd /
# Start AI here
"Update the helm chart"
```

Too much context. The AI has to search your entire filesystem. Slow and error-prone.

---

### ❌ Still Too Broad
```bash
cd /company
# Start AI here
"Update the helm chart"
```

Better, but still unclear. Which team owns this? Which subsystem?

---

### ✅ Just Right - Start Where Relevant Context Lives
```bash
cd /company/SRE/
# Start AI here
"Look in helm/charts/my-service/ and update resource limits to 1Gi memory"
```

**Why this works**:
- You're at the SRE level where all your infrastructure context lives
- Your AGENTS.md tells the AI about directory organization
- You explicitly mention the path in your prompt
- The AI can reference related SRE resources (runbooks, other charts, terraform)
- You maintain flexibility to work across multiple subsystems

**What the AI gets from this location**:
- Reads `/company/SRE/AGENTS.md` for context
- Knows this is infrastructure work (not dev/QA)
- Has access to runbooks, scripts, notes if needed
- Can compare across helm charts or reference terraform configs
- Understands SRE conventions and workflows

**Natural language enhancement**:
```
I need to update resource limits for my-service in helm/charts/my-service/.
We've been seeing OOMKilled pods in production, and monitoring shows we're
consistently hitting 80% of our 512Mi memory limit during peak hours.

Can you:
1. Look at helm/charts/my-service/values.yaml and show current limits
2. Suggest new limits with appropriate headroom (thinking 1Gi memory)
3. Make sure requests/limits ratio still makes sense

I want to avoid OOMKills but also not over-provision since our nodes are
already pretty packed.
```

---

### ✅ When to Navigate Deeper - Limiting Scope

Only navigate to a specific subdirectory when you want to **limit what the AI can access**:

```bash
cd /company/SRE/helm/charts/my-service/
# Start AI here
"Update resource limits in this chart"
```

**Use this approach when**:
- You want the AI to focus only on one specific component
- You're working in a large monorepo and want to reduce noise
- You need to prevent the AI from accidentally modifying other services
- The specific directory has its own AGENTS.md with detailed rules

**Trade-off**: You lose access to broader context (other charts, runbooks, related scripts).

---

### 🎯 The SRE-Level Start Pattern (Recommended)

For most SRE work, starting at `/company/SRE/` gives you the best balance:

```bash
cd /company/SRE/
# Start AI here
```

**Example prompts from this location**:

**Focused task with explicit path**:
```
Look in helm/charts/user-api/ and update the ingress configuration to use
the new domain new-domain.company.com instead of old-domain.company.com.

I'm not sure if we need to support both domains during migration or if we
can do a hard cutover. Check if there are any related runbooks in notes/runbooks/
about domain migrations.
```

**Cross-system investigation**:
```
I'm trying to understand our database failover process. Can you:

1. Search notes/runbooks/ for database failover procedures
2. Check helm/charts/*/values.yaml for database connection configs
3. Look in terraform/ for database infrastructure setup

I need to see how all the pieces connect - the infrastructure, the app
configuration, and the operational procedures.
```

**Exploratory search**:
```
Search through all helm charts for services that use nginx-ingress. We're
planning to upgrade to version 1.5 and I want to assess the impact.

Look for:
- Direct nginx-ingress references in Chart.yaml dependencies
- Ingress resources in templates/ directories
- Annotations that might reference nginx-ingress classes

List which services are affected and note what patterns they're using.
```

**Why these work**:
- Started at SRE level for broad context access
- Explicitly mentioned paths (helm/charts/, notes/runbooks/, terraform/)
- AGENTS.md provides the directory map
- Can reference multiple subsystems in one session
- Natural language explains the goal and constraints

---

## Cross-Team Investigations: When to Use Subagents

Starting at the SRE level gives you visibility into the entire infrastructure context. But sometimes an SRE problem requires investigating code in a dev repository.

**This is a perfect opportunity for multi-tab orchestration with handoff prompts.**

### Real-World Scenario

You're investigating a production issue from your SRE workspace:

```bash
cd /company/SRE/
# Start AI session here
```

**Initial investigation**:
```
We're seeing 500 errors from the user-api service. I've checked:

1. helm/charts/user-api/ - deployment configuration looks correct
2. notes/incidents/ - no similar recent incidents
3. Prometheus metrics - shows errors started after last deploy

The errors are "database connection timeout" but our database is healthy.
I think the issue might be in how the application code is handling connection
pooling, which would be in the dev repo at /company/Dev/user-api/.

Can you summarize what we know so far and draft a handoff prompt for a
subagent that will investigate the dev repo?
```

**AI generates handoff prompt**:
```
Based on the SRE investigation, here's a handoff prompt for the dev repo:

---
I need to investigate a production issue with database connection timeouts
in the user-api service.

## Context from SRE investigation:
- Errors started after deployment at 14:23 UTC today
- Helm chart configuration shows correct connection pool settings (pool size: 50)
- Database is healthy and responding normally
- Error message: "database connection timeout after 5000ms"
- Prometheus shows 500 error rate at 15% of requests

## What I need from you:
1. Look in the application code for database connection handling
2. Check if there were recent changes to connection pooling logic
3. Look for any hardcoded timeouts that might override the config
4. Check if connection retry logic changed

## Specific questions:
- Is the app respecting the pool size from config?
- Are connections being properly released back to the pool?
- Did recent commits change transaction handling?

The deployment that introduced this was commit abc123def.
---
```

### Using the Handoff Pattern

**Step 1: Generate handoff in SRE session**
```
"Draft a handoff prompt for investigating this issue in the dev repo"
```

**Step 2: Open new tab/session in dev repo**
```bash
cd /company/Dev/user-api/
# Start new AI session here
```

**Step 3: Paste handoff prompt**
The new session has:
- Dev repo AGENTS.md context (code structure, testing patterns)
- Git history access
- Full source code
- Focus on application-level investigation

**Step 4: Investigation results come back**
The dev-scoped agent finds:
```
Found the issue in src/database/pool.py:

Recent commit abc123def changed connection pool from using config value
to a hardcoded `max_connections=10`. This overrides the helm chart config
of 50 connections.

Line 42: pool = ConnectionPool(max_connections=10)  # BUG: should use config

This was likely a debugging change that got committed by mistake.
```

**Step 5: Return to SRE session for fix**
```bash
cd /company/SRE/
# Back to original session
```

Now you know the root cause and can coordinate the fix:
- Dev team reverts the hardcoded value
- You prepare for redeployment
- Update incident log and runbook

---

### Why This Pattern Works

**Keeps context scoped**:
- SRE agent sees infrastructure, config, metrics
- Dev agent sees code, git history, tests
- Each agent reads the appropriate AGENTS.md

**Enables focused investigation**:
- Dev agent isn't distracted by helm charts and terraform
- SRE agent isn't overwhelmed by application source code
- Each agent operates in its domain

**Handoff prompt captures essential context**:
- What you've already ruled out
- Specific questions to answer
- Business context (production impact)
- Technical constraints (timing, commit hash)

**Prevents token waste**:
- Don't load entire dev repo into SRE session
- Don't load entire infrastructure into dev session
- Each agent has focused, relevant context

---

### Practical Handoff Template

When generating handoffs from SRE to dev investigations:

```markdown
## Problem Statement
[Brief description of the production issue]

## What We've Ruled Out
- Infrastructure: [findings]
- Configuration: [findings]
- Database/External services: [findings]

## What We Need to Investigate
[Specific areas in the dev repo to examine]

## Specific Questions
1. [Question about code behavior]
2. [Question about recent changes]
3. [Question about configuration handling]

## Context
- Deployment: [commit hash, timestamp]
- Error rate: [percentage, count]
- Affected users: [scope]
- Timeline: [when it started]
```

This pattern extends to any cross-team investigation:
- SRE → Dev (application issues)
- SRE → QA (load testing results)
- Dev → SRE (deployment pipeline questions)
- QA → Dev (test failure analysis)

**Preview**: Module 4 (Multi-Tab Orchestration) covers this pattern in depth, including parallel investigations and result synthesis.

---

## The Notes Directory in Detail

This is where Context Engineering really shines.

### Runbook Format

**Example: disk-space-alerts.md**
```markdown
# Disk Space Alert Response

**Alert Name**: DiskSpaceHigh
**Severity**: Warning
**Threshold**: 80% usage

## Symptoms
- Prometheus alert firing
- Pod evictions may occur
- Performance degradation possible

## Investigation Steps

1. Check actual disk usage
   ```bash
   df -h
   ```

2. Identify largest directories
   ```bash
   du -sh /* | sort -rh | head -10
   ```

3. Check for specific issues:
   - Docker images: `docker system df`
   - Logs: `journalctl --disk-usage`
   - Temp files: `ls -lh /tmp`

## Common Causes
- Old Docker images not pruned
- Log files not rotated properly
- Application temp files accumulating
- Database backups filling disk

## Resolution

### Quick fix (temporary)
```bash
# Clean docker
docker system prune -af --volumes

# Clean logs older than 7 days
journalctl --vacuum-time=7d

# Clean temp files
find /tmp -type f -atime +7 -delete
```

### Permanent fix
- Verify log rotation is configured
- Set up automated docker cleanup
- Implement proper temp file cleanup
- Consider disk expansion if persistent

## Related Incidents
- INC-2024-089 (2024-11-01) - Docker images caused issue
- INC-2024-102 (2024-10-15) - Log rotation failed

## Last Updated
2024-11-07 by @yourname
```

**Why this format works**:
- AI can parse structure easily
- Humans can read it clearly
- Searchable by symptoms, causes, solutions
- Links to historical incidents

**Communicating about runbooks with AI** (natural language):
```
Command-style (less effective):
"Check runbook for disk space"

Natural language (more effective):
"We're getting the DiskSpaceHigh alert again. I know we have a runbook for this
in the runbooks directory, but I can't remember the exact filename. Can you:
1. Find the disk space runbook
2. Show me the investigation steps
3. Let me know if there's anything about Docker image cleanup specifically

I think the issue might be related to old images, but I want to follow the
proper procedure first."
```

**What natural language adds**:
- Context about the current situation (alert firing)
- Admission of uncertainty (can't remember filename, "I think")
- Specific question about subset of content (Docker cleanup)
- Commitment to proper procedure

---

### Incident Log Format

**Example: 2024-11.md**
```markdown
# Incidents - November 2024

## INC-2024-123 - Database Connection Pool Exhausted
**Date**: 2024-11-07
**Severity**: P1
**Duration**: 45 minutes
**Services Affected**: user-api, billing-api

### Timeline
- 14:23 UTC - Alerts start firing (500 errors increasing)
- 14:25 UTC - On-call engineer paged
- 14:30 UTC - Investigation begins
- 14:45 UTC - Root cause identified (connection pool too small)
- 15:00 UTC - Fix deployed (increased pool size)
- 15:08 UTC - Services recovered

### Root Cause
Database connection pool was configured for 10 connections.
Traffic spike from new feature launch increased load 5x.

### Resolution
Updated helm values to increase pool from 10 to 50 connections:
- File: `/company/SRE/helm/charts/user-api/values.yaml`
- Commit: abc123def

### Prevention
- Added monitoring for connection pool utilization
- Created alert at 70% pool usage
- Updated capacity planning runbook
- Added load testing to deployment checklist

### Learnings
- Should have tested with realistic traffic before launch
- Need better visibility into connection pool metrics
- Consider auto-scaling connection pools based on load

### Related
- Runbook created: `/notes/runbooks/connection-pool-exhaustion.md`
- Work item: WORK-12345
```

---

### Decision Log Format

**Example: 001-kubernetes-cluster-sizing.md**
```markdown
# ADR 001: Kubernetes Cluster Sizing Strategy

## Status
Accepted - 2024-11-01

## Context
We need to determine sizing strategy for new Kubernetes clusters.
Current production cluster is frequently hitting resource limits.

## Decision
We will use the following sizing strategy:

**Node Pools**:
- System pool: 3 nodes, Standard_D4s_v3 (dedicated to system services)
- Application pool: 5-20 nodes, Standard_D8s_v3 (auto-scaling)
- Database pool: 3 nodes, Standard_E8s_v3 (memory-optimized)

**Resource Reservations**:
- System pool: 25% reserved for Kubernetes overhead
- Application pool: 15% reserved
- Database pool: 20% reserved for buffer

**Scaling Triggers**:
- Scale up at 70% average utilization
- Scale down at 30% average utilization
- Min 5-minute stabilization period

## Rationale
- Separate system services prevents application load from affecting cluster management
- Memory-optimized nodes for databases improve performance
- Conservative scaling thresholds prevent flapping
- Auto-scaling reduces manual intervention

## Consequences

**Positive**:
- Better resource isolation
- Improved stability
- Reduced manual scaling
- Cost optimization through auto-scaling

**Negative**:
- More complex architecture
- Higher minimum cost (more nodes)
- Need to monitor multiple node pools

## Alternatives Considered

1. **Single node pool**: Simpler but less resilient
2. **Larger cluster with no auto-scaling**: Expensive and wasteful
3. **Smaller nodes with more replicas**: More overhead, more complex

## Implementation
- Terraform code: `/company/SRE/terraform/kubernetes-clusters/aks-sizing.tf`
- Monitoring dashboards: Created for each node pool
- Runbook: `/notes/runbooks/cluster-scaling.md`

## Review Date
2025-02-01 (3 months)
```

**AI Usage with natural language**:
```
Terse command (works, but limited):
"Search decision logs for cluster sizing"

Natural language (better results):
"I'm working on right-sizing our new Kubernetes cluster and want to understand
the reasoning behind our current cluster architecture. Can you search through
the decision logs in /notes/decisions/ for anything related to cluster sizing,
node pools, or resource allocation?

I'm particularly interested in:
- Why we chose separate node pools for system vs application workloads
- What scaling thresholds we decided on and why
- Any alternatives we considered but rejected

This will help me avoid repeating past mistakes or reinventing solutions we've
already evaluated."
```

**What the natural language version accomplishes**:
- Explains the broader context (right-sizing new cluster)
- Specifies what aspects matter most (node pools, scaling)
- Shows awareness of organizational learning (past decisions)
- Makes it clear why this information is needed (avoid mistakes)

---

## Practical Exercise: Organize Your Workspace

### Step 1: Audit Current Structure
```bash
cd /company  # Or wherever your work lives
tree -L 3 -d  # See current structure
```

Ask yourself:
- Can I find things easily?
- Is there clear separation of concerns?
- Would an AI know where to look?

---

### Step 2: Create Missing Directories
```bash
mkdir -p SRE/notes/{runbooks,incidents,inventory,decisions}
mkdir -p SRE/scripts/{automation,utilities,monitoring}
mkdir -p SRE/tmp
```

---

### Step 3: Move Files to Logical Locations
Don't do everything at once. Pick one category:
```bash
# Example: Organize runbooks
mv scattered-doc-1.md SRE/notes/runbooks/disk-space-alerts.md
mv scattered-doc-2.md SRE/notes/runbooks/pod-crashloop.md
```

---

### Step 4: Create AGENTS.md and README Files

Create both AGENTS.md (for AI) and README.md (for humans) at appropriate levels:

**Example: /company/SRE/AGENTS.md**
```markdown
# AGENTS.md

## SRE Team Workspace

This directory contains all SRE infrastructure and operations code.

## Repository Structure
```
terraform/     # Infrastructure as Code
helm/          # Kubernetes chart repository
ansible/       # Configuration management
flux/          # GitOps configurations
notes/         # Runbooks, incidents, decisions, inventory
scripts/       # Automation and utilities
tmp/           # Temporary files (not committed)
```

## Common Commands
```bash
# Terraform
cd terraform/ && terraform plan

# Helm
helmfile -e production sync

# Flux
flux reconcile kustomization clusters-minikube
```

## Key Conventions
- All infrastructure changes require terraform plan review
- Helm charts use values/ directory for environment configs
- Scripts must include error handling and dry-run mode
- Document major decisions in notes/decisions/
```

**Example: /company/SRE/notes/README.md**
```markdown
# SRE Notes and Documentation

## Structure

- `runbooks/` - Step-by-step procedures for common issues
- `incidents/` - Post-mortem reports and incident logs
- `inventory/` - Searchable data stores (Azure resources, work items, etc.)
- `decisions/` - Architecture Decision Records (ADRs)

## For Human Readers

This directory contains our operational knowledge base. When responding to
incidents, start with runbooks. When planning changes, review past incidents
and decision records.

## Maintenance

- Update incident logs monthly
- Refresh inventory weekly or after major changes
- Review and update runbooks after each use
- Decision logs reviewed quarterly
```

**Key difference**:
- **README.md**: Context for humans, describes *what* and *why*
- **AGENTS.md**: Context for AI, describes *where* and *how*

---

### Step 5: Test with AI
```bash
cd /company/SRE/notes/
# Start AI session

Command-style test:
"Describe what kind of documentation lives here based on the directory structure"

Natural language test (better):
"I just reorganized our documentation into this directory structure. Based on
what you can see here, can you tell me:

1. What kinds of documentation we have
2. How you would find information about a specific topic (like database failovers)
3. Whether the organization makes sense or if you'd suggest improvements

I want to make sure this structure is intuitive not just for me, but for anyone
(human or AI) who needs to find information quickly during an incident."
```

**Why the natural language version is better**:
- Explains the context (just reorganized)
- Asks for specific feedback (what, how to find, improvements)
- Shows the intended use case (finding info during incidents)
- Invites collaborative improvement

If the agent can figure it out AND provides useful structural feedback, your organization is working.

---

## Git Integration

### Repository Organization Pattern

Use separate git repositories for each project or subsystem, organized by category in your filesystem.

**Recommended structure**:
```
/company/SRE/
├── AGENTS.md                    # SRE team-level context
├── terraform/
│   ├── AGENTS.md                # Maps terraform repos in this category
│   ├── azure-infrastructure/    (.git - separate repo)
│   ├── kubernetes-clusters/     (.git - separate repo)
│   └── networking/              (.git - separate repo)
├── helm/
│   ├── AGENTS.md                # Maps helm chart repos in this category
│   ├── service-a-chart/         (.git - separate repo)
│   ├── service-b-chart/         (.git - separate repo)
│   └── monitoring-charts/       (.git - separate repo)
├── ansible/
│   ├── AGENTS.md                # Maps ansible repos in this category
│   ├── base-config/             (.git - separate repo)
│   └── app-deployment/          (.git - separate repo)
└── notes/                       (.git - shared documentation repo)
```

**Why this works**:
- **Separate repos**: Clear ownership, independent versioning, separate lifecycle
- **Category organization**: Logically group related repos in filesystem
- **Category-level AGENTS.md**: Explains which repos exist and how to use them
- **Easy navigation**: Start at SRE level, navigate to category, AI reads AGENTS.md

**Example category-level AGENTS.md**:

**/company/SRE/terraform/AGENTS.md**:
```markdown
# Terraform Repositories

This directory contains our infrastructure-as-code repositories.

## Repositories

### azure-infrastructure/
- **Purpose**: Azure resource provisioning (VNets, storage, databases)
- **Owner**: Platform team
- **Deployment**: Manual apply after review

### kubernetes-clusters/
- **Purpose**: AKS cluster definitions and node pools
- **Owner**: SRE team
- **Deployment**: Automated via GitOps

### networking/
- **Purpose**: Network policies, DNS, load balancers
- **Owner**: Network engineering team
- **Deployment**: Manual apply after review

## Common Commands

```bash
# Plan changes
terraform plan -out=tfplan

# Review plan
terraform show tfplan

# Apply after approval
terraform apply tfplan
```

## Conventions

- All changes require plan review before apply
- Use terraform workspaces for environments (dev/staging/prod)
- State stored in Azure Storage backend
- Lock files committed to repo
```

**Benefits of category-level AGENTS.md**:
- AI understands the landscape of repos in a category
- Documents ownership and deployment patterns
- Provides common commands applicable to all repos in category
- You can work across multiple repos from the category level

---

### Working with Git Worktrees

For parallel updates to same repo:
```bash
cd /company/SRE/helm/

# Create worktrees for parallel work
git worktree add ../helm-worktree-service-a
git worktree add ../helm-worktree-service-b

# Now you can work in both simultaneously
# Each in its own terminal tab with its own AI agent
```

**AI prompt for each tab**:
```
Tab 1 (command-style):
"Working on service-a helm chart in this worktree.
Update resource limits based on recent metrics."

Tab 1 (natural language - better):
"I'm in a git worktree for service-a's helm chart. We've been monitoring
resource usage for the past week, and I can see in Grafana that we're
consistently using about 80% of our memory limits during peak hours.

Can you:
1. Show me the current resource limits in values.yaml
2. Suggest new limits with appropriate headroom
3. Make sure requests/limits ratio makes sense

I want to avoid OOMKills, but also not over-provision since our nodes are
already pretty packed."

Tab 2 (natural language):
"This worktree is for service-b's helm chart. We're migrating to a new domain
(new-domain.company.com) and I need to update the ingress configuration.

The current ingress is set up for old-domain.company.com. I'm not sure if we
need to support both domains during the migration period or if we can do a
hard cutover.

Can you show me the current ingress config and suggest how to handle the
domain migration? Include any considerations about certificate management."
```

**What natural language adds to worktree coordination**:
- Explains why you're in a worktree (parallel work context)
- Provides business context for changes (metrics, migration)
- Expresses uncertainty where it exists (support both domains?)
- Helps AI understand constraints (nodes are packed)

---

## Environment-Specific Organization

### Values Files Structure
```
helm/charts/my-service/
├── Chart.yaml
├── values.yaml              # Defaults
├── values/
│   ├── dev.yaml            # Dev overrides
│   ├── staging.yaml        # Staging overrides
│   └── production.yaml     # Production overrides
└── templates/
```

**AI Usage**:
```
Command-style:
"Compare resource limits across all environment value files.
Ensure production has at least 2x the resources of staging."

Natural language (more effective):
"I want to verify our environment progression for resource limits. We should
have production running with at least 2x the resources of staging, and staging
with at least 2x dev.

Can you compare the resource limits (CPU and memory) across:
- values/dev.yaml
- values/staging.yaml
- values/production.yaml

I'm particularly concerned about whether we've maintained this ratio as we've
been updating charts over time. If you find any violations of the 2x rule,
flag them and suggest appropriate values.

Also, let me know if you see any environments where limits and requests are
significantly different - that might indicate we're not getting realistic
resource usage data."
```

**What natural language adds**:
- Explains the principle (environment progression, 2x rule)
- Shows awareness of drift over time
- Asks for specific analysis (violations, suggestions)
- Adds a second concern based on operational experience (limits vs requests)

---

### Terraform Workspaces vs. Directories

**Directory-based** (Recommended):
```
terraform/
├── dev/
│   ├── main.tf
│   └── variables.tf
├── staging/
│   ├── main.tf
│   └── variables.tf
└── production/
    ├── main.tf
    └── variables.tf
```

**Benefits for AI**:
- Clear separation
- Can work on multiple environments in parallel
- Less risk of applying to wrong environment

---

## Common Mistakes

### ❌ Flat Structure
```
/work/
├── script1.sh
├── chart1-values.yaml
├── runbook.md
├── main.tf
└── ...
```

No organization. AI can't determine context.

---

### ❌ Too Deep
```
/company/teams/infrastructure/sre/kubernetes/helm/charts/applications/backend/user-api/
```

16 directories deep. Nobody knows where they are.

**Rule of thumb**: 4-5 levels maximum.

---

### ❌ Inconsistent Naming
```
/company/
├── SRE/
├── dev-team/
├── QualityAssurance/
└── release_management/
```

Mix of cases and separators. Hard to remember, hard to navigate.

**Choose a standard**:
- Kebab-case: `release-management`
- Snake_case: `release_management`
- PascalCase: `ReleaseManagement`

Be consistent.

---

## Quick Wins

### 1. Create an AGENTS.md File
Start with your team-level directory (like `/company/SRE/AGENTS.md`). Include:
- Brief overview of what's here
- Directory structure (top-level)
- 3-5 most common commands

This single file can save hundreds of tokens per session.

### 2. Create a Notes Directory
Even if nothing else, having `/notes/` for runbooks and incidents is huge.

### 3. Use Consistent Naming
Pick a pattern and stick to it.

### 4. Add README Files for Humans
A README in each major directory helps human collaborators understand context.

### 5. Keep Tmp Clean
Delete old files regularly. Don't let it become a dumping ground.

### 6. Start Sessions at the Right Level
Start at team/domain level (like `/company/SRE/`) and use explicit paths in prompts. Only navigate deeper when you need to limit scope.

---

## Summary

**Good filesystem organization**:
- Mirrors your team structure
- Groups related files logically
- Has clear naming conventions
- Includes searchable documentation
- Separates long-term storage from temporary files
- **Includes AGENTS.md files to guide AI harnesses**

**Benefits for Context Engineering**:
- AI knows where to look (via AGENTS.md)
- Starting at team level provides broad context access
- Use explicit paths to direct AI within that context
- AGENTS.md reduces exploration time and token waste
- Better search results from proper organization
- Natural isolation of concerns

**Key principle**: Start where relevant context lives (team/domain level), use AGENTS.md + explicit paths to guide the AI, only navigate deeper to limit scope.

---

## Next Steps

1. Audit your current structure
2. Create your first AGENTS.md (start at team level)
3. Create `/notes/` directories
4. Move a few files to logical locations
5. Test with AI from team-level directory - can it navigate with your AGENTS.md?
6. Iterate: add to AGENTS.md based on questions AI asks repeatedly

---

**[← Back to Core Concepts](01-core-concepts.md)** | **[Multi-Tab Orchestration →](03-multi-tab-orchestration.md)**
