# Module 4: Integration Patterns

Connecting AI agents to live systems via MCP servers, CLIs, and APIs.

---

## The Integration Landscape

You have three fundamental approaches for giving AI access to external system information:

### The Three Integration Options

**1. Local Data Stores** - Efficient, offline snapshots
- Periodic exports of system state
- Fast local searches with no API calls
- No context cost (data read only when needed)
- Build searchable inventories of your systems

**2. Live Queries** - Real-time access via CLI tools or APIs
- Command-line tools (az, kubectl, terraform, etc.)
- Direct API calls for current state
- No context overhead (tools invoked only when needed)
- Real-time data, higher latency per query

**3. MCP Servers** - Protocol-based integrations
- Standardized tool interfaces
- Live access to external systems
- **Context cost every conversation** (tool schemas always loaded)
- Covered in depth in **[Module 7](07-mcp-servers.md)**

### The Critical Trade-off: Context Cost

**Local data stores and live CLI queries** share a key advantage: **zero persistent context cost**. You only pay tokens when you actually read the data or invoke the tool.

**MCP servers** trade context efficiency for convenience: their tool schemas consume context in every conversation, whether you use them or not.

**The decision framework**: Choose based on frequency of use, need for real-time data, and context budget.

| Approach | Context Cost | Data Freshness | Query Speed | Best For |
|----------|-------------|----------------|-------------|----------|
| **Local Data** | None (data read as needed) | Periodic snapshots | Very fast | Frequent queries, historical data |
| **Live CLI** | None (tools invoked as needed) | Real-time | Moderate (API latency) | On-demand current state |
| **MCP Server** | Every conversation | Real-time | Fast | High-frequency daily use |

Each has its place. The key is matching the approach to your usage pattern.

---

## Decision Framework: Three Integration Approaches

Choosing between local data, live CLI queries, and MCP servers depends on **frequency**, **freshness requirements**, and **context budget**.

### Use Live Queries When:

✅ **Current state needed**
```
"What's the current CPU usage of our production VMs?"
"Are there any pods crashlooping right now?"
"What's the status of the latest deployment?"
```

✅ **Making changes**
```
"Scale the deployment to 5 replicas"
"Update work item 12345 status to Done"
"Restart the failing pod"
```

✅ **Data changes frequently**
```
"Show me active alerts"
"What's current memory usage?"
"List running CI/CD pipelines"
```

---

### Use Local Data Stores When:

✅ **Historical data**
```
"Has this error happened before?"
"Show incidents from last quarter"
"What alerts have we tuned in the past?"
```

✅ **Large datasets**
```
"Search all runbooks for database procedures"
"Find every mention of 'connection pool' in our docs"
```

✅ **Repeated searches**
```
"Show me all VMs in eastus" (asked 10 times today)
```

✅ **Fast searches needed**
```
"Quick lookup of service configuration" (faster than API call)
```

---

### Use MCP Servers When:

✅ **High-frequency daily use**
```
"I query incident management 20+ times during my on-call shift"
"I check GitHub PRs 15 times per day"
"I need deployment status constantly throughout the day"
```

✅ **Complex multi-step workflows benefit from standardization**
```
"Updating work items involves checking status, reading comments, updating fields"
"Deployment verification needs status + logs + metrics from one system"
"Incident coordination requires alerts + tickets + team communications"
```

✅ **Real-time data critical AND used constantly**
```
"On-call week: PagerDuty queries every hour"
"Active project: deployment status checks 10+ times daily"
"Security audit: vulnerability scans multiple times per day"
```

⚠️ **Context cost warning**:
- Each MCP server consumes tokens every conversation
- Multiple servers compound the cost
- Only worth it if you use the tools **daily** and **intentionally**
- See **[Module 7](07-mcp-servers.md)** for detailed evaluation framework

---

### Three-Way Comparison: Real SRE Scenarios

**Scenario 1: Checking cloud resource inventory**

| Approach | How It Works | Context Cost | When to Use |
|----------|-------------|--------------|-------------|
| **Local Data** | Export resources weekly to JSON, search locally | None | You query resource lists 5+ times per day (dev work, planning, audits) |
| **Live CLI** | Run `az resource list` when needed | None | You check resources occasionally (1-2 times per week) |
| **MCP Server** | MCP provides live resource queries | ~2-5k tokens/conversation | You query resources 20+ times daily AND need real-time state |

**Best choice for most teams**: Local data (frequent queries, data doesn't change hourly)

---

**Scenario 2: Incident management during on-call**

| Approach | How It Works | Context Cost | When to Use |
|----------|-------------|--------------|-------------|
| **Local Data** | Historical incidents in markdown files | None | Researching past incidents, finding patterns |
| **Live CLI** | Use incident system CLI or web UI | None | Not on-call, occasional lookups |
| **MCP Server** | PagerDuty/incident tool MCP server | ~3-8k tokens/conversation | **On-call week**: querying incidents 15+ times per day |

**Best choice**:
- **On-call week**: Install MCP server for high-frequency use
- **Off-call**: Remove MCP, use local incident history for research
- **Occasional lookup**: Use web UI or CLI

---

**Scenario 3: Service catalog and dependency information**

| Approach | How It Works | Context Cost | When to Use |
|----------|-------------|--------------|-------------|
| **Local Data** | Export service catalog monthly, search locally | None | Planning, architecture reviews, general reference (most common use) |
| **Live CLI** | Query service catalog API when needed | None | Occasional verification of current service state |
| **MCP Server** | Service catalog MCP providing live queries | ~2-4k tokens/conversation | You reference service catalog 20+ times daily |

**Best choice for most teams**: Local data (catalog doesn't change frequently, queried often)

---

**Scenario 4: Deployment and release status**

| Approach | How It Works | Context Cost | When to Use |
|----------|-------------|--------------|-------------|
| **Local Data** | Snapshot deployment state daily | None | Historical "what was deployed when" queries |
| **Live CLI** | `kubectl get deployments`, `helm list` | None | Occasional verification, troubleshooting |
| **MCP Server** | K8s/deployment status MCP | ~5-10k tokens/conversation | Active deployment day: checking status 30+ times |

**Best choice**:
- **Normal operations**: Live CLI (real-time when needed, no context cost)
- **Active deployment project**: Consider temporary MCP installation
- **Historical analysis**: Local data snapshots

---

**Scenario 5: Work item and ticket management**

| Approach | How It Works | Context Cost | When to Use |
|----------|-------------|--------------|-------------|
| **Local Data** | Export your work items daily to JSON | None | Quick reference to your task list, planning |
| **Live CLI** | Use Azure DevOps/Jira CLI | None | Updating tickets occasionally |
| **MCP Server** | Work item system MCP | ~3-6k tokens/conversation | You update tickets 15+ times daily, every conversation |

**Best choice for most people**:
- Local data for reference (your task list)
- CLI for updates (simple commands)
- MCP only if you're doing heavy ticket management as primary work

---

### The Context Cost Reality

**Example: Three MCP servers installed**

```
Your setup:
- PagerDuty MCP (8 tools) → ~3k tokens
- GitHub MCP (15 tools) → ~5k tokens
- AWS MCP (30 tools) → ~8k tokens
Total context cost: ~16k tokens per conversation

Your usage:
- PagerDuty: Used daily during on-call week (1 week/month)
- GitHub: Used 3-4 times per week
- AWS: Installed 2 months ago, used twice

Analysis:
- PagerDuty: Good value during on-call, remove when off-call
- GitHub: Moderate use - consider CLI + AI instead
- AWS: Pure waste - remove immediately, use 'aws' CLI

Action: Remove AWS MCP, reclaim 8k tokens
Consider: Remove PagerDuty between on-call rotations
```

**The principle**: Every MCP server should justify its context cost through **daily, intentional use**. If you're using it weekly or monthly, alternatives are more efficient.

See **[Module 7](07-mcp-servers.md)** for comprehensive evaluation framework and audit process.

---

### Hybrid Approach: The Best Pattern

**Combine all three approaches** strategically:

**Pattern: Local discovery → Live verification → Action**

```
Step 1: Search local inventory (fast, no context cost)
"Search azure-resources.json for all VMs tagged environment=staging"
→ Fast, finds candidates: vm-staging-1, vm-staging-2

Step 2: Verify live (current state, no context cost)
"Using az cli, check current status of vm-staging-1 and vm-staging-2"
→ Confirms they still exist and gets current state

Step 3: Take action
"Stop vm-staging-2 to save costs"
→ Executes against live system
```

**Why this works**:
- Fast initial search (local data)
- Verified before action (live CLI)
- Reduced API calls (efficiency)
- Zero persistent context cost (no MCP needed)

---

**Pattern: MCP for high-frequency active work, local for research**

```
On-call week scenario:

Active incident management (MCP):
"Using PagerDuty MCP, show current P1 incidents"
→ Used 20+ times during shift, context cost justified

Historical pattern research (local):
"Search local incident files for similar database timeout issues"
→ Fast searches, no API calls, no context cost

Combined value:
- MCP for real-time active work
- Local data for research and patterns
- Remove MCP when off-call rotation ends
```

**The principle**:
- **Default to local data** for frequent reference queries
- **Use live CLI** for on-demand current state
- **Install MCP** only for high-frequency daily use during active work periods
- **Remove MCP** when that work period ends

See **[Module 7: MCP Servers](07-mcp-servers.md)** for task-specific installation patterns.

---

## CLI Tools Integration

### Common CLIs for SRE Work

- **az** - Azure CLI
- **kubectl** - Kubernetes
- **helm** - Helm charts
- **terraform** - Infrastructure as code
- **git** - Version control
- **jq** - JSON processing
- **flux** - GitOps

### Basic Pattern

**AI can execute CLI commands**:
```
"Using kubectl, show me all pods in the production namespace"

AI executes:
kubectl get pods -n production

Returns output for analysis.
```

---

### Multi-Step CLI Workflows

**Investigation with multiple commands**:
```
Context: Pod crashlooping in production
Namespace: production
Pod name: user-api-7d4f8b9c-x5k2j

Investigate:
1. Get pod details: kubectl describe pod
2. Check recent logs: kubectl logs --tail=100
3. Check previous logs: kubectl logs --previous
4. Get events: kubectl get events --field-selector involvedObject.name=...

Analyze and identify root cause.
```

**AI orchestrates the commands**, analyzes output, provides diagnosis.

---

### CLI for Verification

**Before making changes**:
```
"I'm about to update the helm chart to increase replicas from 3 to 5.

Using helm and kubectl:
1. Show current replica count
2. Check if HPA is enabled (would conflict)
3. Verify enough cluster capacity for 2 more pods
4. Confirm no Pod Disruption Budget issues

If all clear, proceed. If issues, report them."
```

**AI as safety check** - validates before you commit.

---

### CLI Pipelines

**Combining multiple tools**:
```
"Use az cli to get all VM names in production-rg,
then for each VM, check its current status,
format as a table with: Name, Status, Location, Size"

AI might generate:
az vm list -g production-rg --query "[].name" -o tsv | \
  while read vm; do
    az vm show -g production-rg -n "$vm" --query "{Name:name, Status:powerState, Location:location, Size:hardwareProfile.vmSize}" -o table
  done
```

---

## MCP (Model Context Protocol) Servers

### What is MCP?

**Model Context Protocol**: A standard way for AI agents to interact with external systems.

**Think of it as**: API + AI-friendly interface

**Your MCPs**:
- Azure MCP - Query Azure resources
- Azure DevOps MCP - Work items, wikis, repos

---

### Azure MCP

**Capabilities**:
- Query resources
- Get resource details
- List by type, location, resource group
- Check status, configuration

**Example Usage**:

**Query all VMs**:
```
"Using Azure MCP, list all virtual machines in the production resource group.

For each VM show:
- Name
- Size
- Status (running/stopped)
- Location"
```

**Get specific resource**:
```
"Using Azure MCP, get details for vm-prod-1:
- Current SKU
- Network configuration
- Attached disks
- Tags"
```

**Filter and analyze**:
```
"Using Azure MCP, find all resources:
- Tagged with environment=production
- In eastus location
- Created in the last 30 days

Group by resource type and count."
```

---

### Azure DevOps MCP

**Capabilities**:
- Query work items
- Update work items
- Search wiki
- Access repositories
- Trigger pipelines (potentially)

#### Work Item Operations

**Search work items**:
```
"Using Azure DevOps MCP, find all work items:
- Assigned to me
- State: Active or In Progress
- Tags contain: 'helm' or 'kubernetes'

Sort by priority."
```

**Update work item**:
```
"Using Azure DevOps MCP, update work item 12345:

Changes:
- State: In Progress → Done
- Add comment: 'Updated ingress-nginx to version 4.8. Tested in staging, deployed to production.'
- Add tag: 'deployed-2024-11-07'
- Link to related item: 12347"
```

**Create work item**:
```
"Using Azure DevOps MCP, create new work item:

Type: Bug
Title: 'Pod crashloop in user-api production'
Description: [detailed description]
Assigned to: [your name]
Priority: 1
Tags: 'production', 'incident', 'user-api'
Related: Link to incident INC-2024-123"
```

---

#### Wiki Operations

**Search wiki**:
```
"Using Azure DevOps MCP, search the wiki for:
- Pages about database failover procedures
- Any mentions of connection pool configuration
- Deployment checklists

Summarize findings."
```

**Read wiki page**:
```
"Using Azure DevOps MCP, read wiki page at path:
/Infrastructure/Database/Failover-Procedures

Summarize the key steps."
```

**Update wiki**:
```
"Using Azure DevOps MCP, update wiki page at:
/Infrastructure/Kubernetes/Deployment-Guide

Add new section:
## Helm Chart Updates
[content...]

Maintain existing formatting."
```

---

### When to Use MCP vs. CLI vs. Local Data

**Context-aware decision matrix:**

| Scenario | Local Data | CLI | MCP Server | Context Cost Winner |
|----------|-----------|-----|------------|-------------------|
| Query Azure resources | ✅ Best for repeated queries | ✅ Best for occasional | ⚠️ Only if 20+ queries/day | **Local** (zero cost) |
| Complex az commands | N/A | ✅ Preferred | ❌ No | **CLI** (zero cost) |
| Update work items | For reference only | ✅ Simple updates | ⚠️ Only if constant use | **CLI** (zero cost) |
| Execute kubectl | N/A | ✅ Only option | ❌ No | **CLI** (zero cost) |
| Search wiki | ✅ Export wiki periodically | ❌ Hard | ⚠️ Only if daily searches | **Local** (zero cost) |
| Git operations | N/A | ✅ Only option | ❌ No | **CLI** (zero cost) |
| Historical incident patterns | ✅ Best | N/A | N/A | **Local** (zero cost) |

**Key insight**: Notice how **CLI and local data** win most scenarios due to **zero context cost**. MCP servers need **very high frequency** to justify their context overhead.

**Reality**: Default to CLI and local data. Only install MCP servers when you can justify daily, high-frequency use (15-20+ queries per day).

> ⚠️ **Accountability**: Installing MCP servers without considering context cost is like deploying services without resource limits. Every MCP server you install reduces context available for your actual work. Be intentional about what tools live in your context window.

---

## Integration Patterns

### Pattern 1: MCP Discovery + CLI Action

**Use case**: Find resources via MCP, act via CLI

```
Step 1: Discovery (MCP)
"Using Azure MCP, find all stopped VMs in dev resource group"
→ Returns: vm-dev-1, vm-dev-2, vm-dev-5

Step 2: Analysis
"These VMs have been stopped for 30+ days. Candidates for deletion?"

Step 3: Action (CLI)
"Using az cli, delete vm-dev-5 (confirmed unused)"
→ Executes: az vm delete -g dev -n vm-dev-5 --yes
```

---

### Pattern 2: Local Discovery + MCP Verification + CLI Action

**Use case**: Three-tier verification

```
Step 1: Local search (Fast)
"Search azure-resources.json for all VMs in eastus"
→ Finds 15 VMs from last week's snapshot

Step 2: MCP verification (Current state)
"Using Azure MCP, verify these 15 VMs still exist and get current status"
→ 13 exist, 2 deleted, 1 stopped

Step 3: CLI action (Modification)
"Using az cli, start the stopped VM: vm-prod-7"
→ Executes: az vm start -g prod -n vm-prod-7
```

**Why three tiers**:
- Local: Fast filtering
- MCP: Current state verification
- CLI: Action execution

---

### Pattern 3: Work Item Workflow Automation

**Use case**: End-to-end work item management

```
Step 1: Query (MCP)
"Using Azure DevOps MCP, find my highest priority work item"
→ Returns: WORK-12345 - Update helm charts for cluster migration

Step 2: Research (Local + CLI)
"Search local work item history for similar migrations.
Then search git history for previous chart updates."

Step 3: Execute work (CLI)
[Do the actual helm chart updates via CLI]

Step 4: Update (MCP)
"Using Azure DevOps MCP, update WORK-12345:
- State: Done
- Comment: Updated charts A, B, C. PR #456.
- Add tag: completed-2024-11-07"

Step 5: Document (MCP)
"Using Azure DevOps MCP, update wiki page:
/Migrations/Cluster-Migration-Status

Add entry for charts completed today."
```

---

### Pattern 4: Incident Response Integration

**Use case**: Incident with multi-system coordination

```
Tab 1 (Blue): Investigation
"Using kubectl, investigate pod crashloop:
1. Get pod logs
2. Describe pod
3. Check events
4. Get resource usage

Identify root cause."

Tab 2 (Red): Immediate fix
"Using kubectl, implement fix:
1. Update deployment (increase memory)
2. Verify pods healthy

Using helm, deploy updated chart."

Tab 3 (Yellow): Documentation
"Create incident report at /notes/incidents/2024-11-07-crashloop.md

Using Azure DevOps MCP:
1. Search for related work items
2. Create new bug for underlying issue
3. Update wiki with new runbook section"
```

**Multi-system integration**: kubectl + helm + MCP + local files

---

## Advanced: Creating Custom Integrations

### When CLI is Awkward

Sometimes you need structured data that CLI doesn't provide easily.

**Option 1: Create wrapper scripts**

```bash
# get-vm-detailed.sh
az vm show -g "$1" -n "$2" --query "{
  name: name,
  status: powerState,
  size: hardwareProfile.vmSize,
  location: location,
  nics: networkProfile.networkInterfaces[].id,
  disks: storageProfile.osDisk.name
}" -o json
```

**AI usage**:
```
"Run ./get-vm-detailed.sh production-rg vm-prod-1"
→ Gets structured output ready for analysis
```

---

### When You Need Persistence

**Option 2: Create sync scripts**

**sync-k8s-state.sh**:
```bash
#!/bin/bash
# Syncs current Kubernetes state to local inventory

kubectl get deployments -A -o json | jq '[.items[] | {
  name: .metadata.name,
  namespace: .metadata.namespace,
  replicas: .spec.replicas,
  available: .status.availableReplicas,
  image: .spec.template.spec.containers[0].image
}]' > /company/SRE/notes/inventory/k8s-deployments.json

echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > /company/SRE/notes/inventory/k8s-last-updated.txt

echo "Kubernetes state synced to inventory"
```

**Usage**:
```
# Run daily or after deployments
./sync-k8s-state.sh

# Then AI can query locally
"Search k8s-deployments.json for all deployments using image version 1.5.x"
```

---

## Security and Safety

### Read Operations: Generally Safe

✅ **Safe queries**:
- List resources
- Get status
- Search documentation
- Query work items

These are read-only, low risk.

---

### Write Operations: Require Care

⚠️ **Requires verification**:
- Update configurations
- Modify work items
- Change wiki pages

**Pattern**: Review before executing
```
Step 1: "Show me what the update will change"
Step 2: [Review]
Step 3: "Proceed with the update" (explicit confirmation)
```

---

### Destructive Operations: Maximum Caution

🚨 **High risk**:
- Delete resources
- Restart services
- Modify production

**Pattern**: Multi-step verification
```
Step 1: "Identify resources to delete"
Step 2: [Review list]
Step 3: "Verify these resources are unused" (check metrics, logs, dependencies)
Step 4: [Final approval]
Step 5: "Delete [specific resource]" (one at a time, not bulk)
```

**Rule**: Never let AI delete things without explicit verification.

---

### Rate Limiting and Quotas

Be aware of API limits:
- Azure API throttling
- Kubernetes API server limits
- DevOps API rate limits

**Pattern**: Use local data stores for bulk queries
```
# Instead of 100 API calls:
"Using Azure MCP, query every VM individually..."

# Do this:
"Using Azure MCP, get all VMs in one query, save to local inventory.
Then search inventory 100 times without hitting API."
```

---

## Practical Examples

### Example 1: Deployment Verification

```
Task: Verify helm deployment succeeded

Using multiple tools:

1. Helm status check
"Using helm, check status of release 'user-api' in namespace 'production'"

2. Pod verification
"Using kubectl, verify all pods are running and ready"

3. Health check
"Using kubectl, exec into one pod and curl the health endpoint"

4. Metrics verification
"Using Azure MCP, check Application Insights for any errors in last 5 minutes"

5. Update tracking
"Using Azure DevOps MCP, update deployment work item with successful deployment"

All systems integrated for end-to-end verification.
```

---

### Example 2: Cost Optimization Workflow

```
Task: Find unused resources to reduce costs

Step 1: Inventory (MCP)
"Using Azure MCP, list all resources with their costs (if available)"

Step 2: Analysis (CLI + Local)
"For each VM:
1. Check last start time (az cli)
2. Search local incident logs - was it used recently?
3. Check local deployment records - is it referenced?"

Step 3: Verification (MCP)
"Using Azure MCP, check metrics for each candidate:
- CPU usage last 30 days
- Network activity
- Disk operations"

Step 4: Decision (Human)
[Review findings, decide what to delete]

Step 5: Action (CLI)
"Using az cli, delete confirmed unused resources"

Step 6: Documentation (MCP + Local)
"Using Azure DevOps MCP, update cost optimization wiki page.
Save resource list to /notes/deleted-resources-2024-11.md"
```

---

### Example 3: Compliance Audit

```
Task: Verify all production resources have required tags

Step 1: Get resources (MCP)
"Using Azure MCP, get all resources in production resource groups"

Step 2: Check tags (Analysis)
"For each resource, verify tags exist:
- environment (required)
- owner (required)
- cost-center (required)

List non-compliant resources."

Step 3: Find owners (Local + MCP)
"Search local notes for ownership information.
Check Azure DevOps wiki for resource ownership records."

Step 4: Create remediation items (MCP)
"For each non-compliant resource, using Azure DevOps MCP:
Create work item to add missing tags.
Assign to resource owner if known."

Step 5: Generate report (Local)
"Create compliance report at /notes/compliance/2024-11-07-tagging-audit.md"
```

---

## Debugging Integration Issues

### MCP Not Working

**Check**:
```
1. Is MCP server configured correctly?
2. Do you have authentication?
3. Are there permission issues?
4. Try equivalent CLI command - does that work?
```

**Fallback**: Use CLI instead
```
"MCP isn't working for this query. Use az cli instead to list resources."
```

---

### CLI Command Failing

**Debug approach**:
```
"The az command failed with error: [error message]

Debug:
1. Is my authentication valid? (az account show)
2. Do I have permissions for this operation?
3. Is the syntax correct?
4. Does the resource exist?

Suggest fixes."
```

---

### Rate Limiting Hit

**Mitigation**:
```
"I'm hitting Azure API rate limits.

Solutions:
1. Use local data store for this query instead
2. Batch queries more efficiently
3. Wait and retry
4. Use cached/approximate data if acceptable"
```

---

## Quick Reference

### Integration Decision Tree

**Updated decision flow with MCP considerations:**

```
Need current state?
├─ Yes → Continue to frequency check
└─ No → Use local data store (Module 4)

How often will you query this?
├─ 20+ times per day, every day → Consider MCP (Module 7 evaluation)
├─ Few times per day → Live CLI (az, kubectl, etc.)
└─ Few times per week → Live CLI as needed

If considering MCP:
├─ Can you quantify daily usage? (Be honest)
│   ├─ Yes, 15+ uses daily → MCP might make sense
│   └─ "Frequently" (vague) → Use CLI instead
│
├─ Is this temporary high-frequency work? (on-call, project)
│   ├─ Yes → Install MCP temporarily, remove after
│   └─ No, ongoing → MCP might make sense
│
├─ Could local data + periodic refresh work?
│   ├─ Yes → Use local data (better efficiency)
│   └─ No, need real-time → MCP might make sense
│
└─ Context cost justified? (Module 7 framework)
    ├─ Yes → Install MCP with audit schedule
    └─ No → Use CLI + AI instead

Making changes?
├─ Yes → Use CLI (more control, verification)
└─ No → Any approach works

Large dataset?
├─ Yes → Pull once, save locally, query local
└─ No → Direct query fine

Destructive operation?
├─ Yes → Multi-step verification + CLI
└─ No → Standard workflow
```

**Key principle**: Default to local data or CLI. Only install MCP servers when you can justify the context cost with **daily, intentional, high-frequency use**.

**See also**:
- **[Module 7](07-mcp-servers.md)**: Complete MCP evaluation framework and decision criteria

---

## Summary

**Three integration approaches**:
1. **Local data stores** (Module 4)
   - No context cost
   - Fast queries
   - Periodic snapshots
   - Best for: Frequent reference queries, historical data

2. **Live CLI queries**
   - No context cost
   - Real-time data
   - API latency per query
   - Best for: On-demand current state, occasional queries

3. **MCP servers** (Module 7)
   - Context cost every conversation
   - Real-time data
   - Standardized tool interfaces
   - Best for: High-frequency daily use (20+ queries/day)

**The context cost trade-off**:
- Local data and CLI: Pay tokens only when used
- MCP servers: Pay tokens every conversation
- Choose MCP only when daily usage justifies context cost

**Best practice**: Strategic combination
- **Default**: Local data for frequent queries, CLI for current state
- **High-frequency work**: Install MCP temporarily for active periods
- **Always verify**: Local for discovery, live for action verification

**Safety**:
- Read operations: generally safe
- Write operations: review first
- Destructive operations: multi-step verification

**Decision framework**: Match approach to usage frequency and freshness needs
- See **[Module 7](07-mcp-servers.md)** for MCP evaluation and management

---

## Next Steps

1. **Audit your current integration approach**:
   - What systems do you query repeatedly?
   - How often? (Be specific: times per day/week)
   - Could local data stores work? (See Module 4)

2. **Evaluate any installed MCP servers**:
   - When did you last use each one?
   - How often do you actually use it?
   - Does daily usage justify context cost?
   - See **[Module 7](07-mcp-servers.md)** for audit framework

3. **Build strategic local data stores**:
   - Start with most frequently queried data
   - Create searchable inventories of your systems

4. **Test the three-way comparison**:
   - Pick one task you do regularly
   - Try local data, CLI, and MCP approaches (if applicable)
   - Measure: context cost, query speed, your preference
   - Choose based on actual usage patterns

5. **Create integration workflows** matching your needs:
   - Local discovery + Live verification pattern
   - Task-specific MCP installation for high-frequency periods
   - Default to zero-context-cost approaches

---

**[← Back to Local Data Stores](04-local-data-stores.md)** | **[Practical Patterns →](06-practical-patterns.md)**
