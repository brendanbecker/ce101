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

## Recommended Structure for SRE Teams

```
company/
├── SRE/
│   ├── terraform/
│   │   ├── azure-infrastructure/
│   │   ├── kubernetes-clusters/
│   │   └── networking/
│   ├── helm/
│   │   ├── charts/
│   │   │   ├── service-a/
│   │   │   ├── service-b/
│   │   │   └── ingress-nginx/
│   │   └── values/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── production/
│   ├── ansible/
│   │   ├── playbooks/
│   │   └── roles/
│   ├── flux/
│   │   └── clusters/
│   ├── notes/
│   │   ├── runbooks/
│   │   ├── incidents/
│   │   ├── inventory/
│   │   └── decisions/
│   ├── scripts/
│   │   ├── automation/
│   │   ├── utilities/
│   │   └── monitoring/
│   └── tmp/
├── Dev/
│   ├── app-repo-1/
│   ├── app-repo-2/
│   └── microservices/
├── QA/
│   ├── load-testing/
│   └── automation/
└── Release-Management/
    ├── deployment-scripts/
    └── release-notes/
```

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

### ❌ Too Broad
```bash
cd /
# Start AI here
"Update the helm chart"
```

Agent has to search everything. Slow and error-prone.

---

### ❌ Still Too Broad
```bash
cd /company
# Start AI here
"Update the helm chart"
```

Better, but which team? Which chart?

---

### ✅ Just Right
```bash
cd /company/SRE/helm/charts/my-service/
# Start AI here
"Update resource limits in this chart"
```

Agent immediately knows:
- SRE work (not dev)
- Helm chart (not terraform)
- Specific service
- Expects Chart.yaml, values.yaml, templates/

**Natural language enhancement**:
```
I need to update resource limits for my-service. We've been seeing OOMKilled
pods in production, and I think we need to increase memory from 512Mi to 1Gi.

The chart is right here in this directory. Can you:
1. Show me the current resource limits
2. Suggest appropriate values based on our production node capacity
3. Update the values.yaml file
```

This combines the right starting location with natural language that provides context about *why* you're making changes.

---

### ✅ Even Better for Investigation
```bash
cd /company/SRE/
# Start AI here
"Search through our helm charts for services using nginx-ingress"
```

Broad enough for searching, specific enough for context.

**Natural language version** (more effective):
```
I'm trying to understand which of our services are using nginx-ingress, because
we're planning to upgrade to a new version and I want to assess the impact.

Starting here in /company/SRE/, can you:
1. Search through all helm charts for nginx-ingress references
2. List which services are affected
3. Note what versions they're currently using

I'm not sure if all references will be obvious - some might use annotations
or custom ingress classes instead of directly referencing nginx-ingress.
```

**Why this works better**:
- Explains the goal (upgrade planning)
- Acknowledges uncertainty (might use annotations)
- Asks for organized output (list, note versions)
- Provides context about your starting location

---

## Repository Organization

### Monorepo vs. Multiple Repos

**Monorepo Approach**:
```
/company/SRE/helm/
├── charts/
│   ├── service-a/
│   ├── service-b/
│   └── service-c/
└── .git/
```

**Pros**:
- Centralized changes
- Easier cross-chart updates
- Consistent versioning

**AI Advantage**: Agent can compare across all charts easily.

---

**Multi-Repo Approach**:
```
/company/SRE/helm/
├── service-a-chart/  # separate repo
├── service-b-chart/  # separate repo
└── service-c-chart/  # separate repo
```

**Pros**:
- Independent versioning
- Smaller, focused repos
- Clearer ownership

**AI Consideration**: Use git worktrees for parallel updates:
```
"Set up git worktrees for service-a and service-b charts so we can update both in parallel"
```

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

### Step 4: Create README Files
Each major directory should have a README:

**Example: /company/SRE/notes/README.md**
```markdown
# SRE Notes and Documentation

## Structure

- `runbooks/` - Step-by-step procedures for common issues
- `incidents/` - Post-mortem reports and incident logs
- `inventory/` - Searchable data stores (Azure resources, work items, etc.)
- `decisions/` - Architecture Decision Records (ADRs)

## Usage with AI Assistants

Point agents to specific subdirectories:
- "Search runbooks for database failover procedures"
- "Check incidents log for similar errors"
- "Look in inventory for Azure VM details"

## Maintenance

- Update incident logs monthly
- Refresh inventory weekly or after major changes
- Review and update runbooks after each use
- Decision logs reviewed quarterly
```

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

### Repository Structure

**Option 1: Separate repos for each tool**
```
/company/SRE/
├── terraform/  (.git)
├── helm/       (.git)
├── ansible/    (.git)
└── notes/      (.git)
```

**Option 2: Single SRE monorepo**
```
/company/SRE/  (.git)
├── terraform/
├── helm/
├── ansible/
└── notes/
```

**Option 3: Mixed approach**
```
/company/SRE/
├── infrastructure/  (.git - contains terraform + ansible)
├── helm/           (.git - separate for deployment velocity)
└── notes/          (.git - separate for easier sharing)
```

Choose based on your team's workflow.

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

### 1. Create a Notes Directory
Even if nothing else, having `/notes/` for runbooks and incidents is huge.

### 2. Use Consistent Naming
Pick a pattern and stick to it.

### 3. Add README Files
A README in each major directory helps humans AND AI.

### 4. Keep Tmp Clean
Delete old files regularly. Don't let it become a dumping ground.

### 5. Start Sessions Closer
Navigate to specific directories before starting AI sessions.

---

## Summary

**Good filesystem organization**:
- Mirrors your team structure
- Groups related files logically
- Has clear naming conventions
- Includes searchable documentation
- Separates long-term storage from temporary files

**Benefits for Context Engineering**:
- AI knows where to look
- Starting location provides implicit context
- Easier to point to specific files
- Better search results
- Natural isolation of concerns

---

## Next Steps

1. Audit your current structure
2. Create `/notes/` directories
3. Move a few files to logical locations
4. Test with AI - can it navigate?
5. Iterate and improve

---

**[← Back to Core Concepts](01-core-concepts.md)** | **[Multi-Tab Orchestration →](03-multi-tab-orchestration.md)**
