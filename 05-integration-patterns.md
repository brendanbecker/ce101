# Module 5: Integration Patterns

Connecting AI agents to live systems via MCP servers, CLIs, and APIs.

---

## The Integration Landscape

You have three ways to give AI access to external systems:

1. **Local Data Stores** - Static snapshots (covered in Module 4)
2. **CLI Tools** - Command-line interfaces (az, kubectl, etc.)
3. **MCP Servers** - Model Context Protocol integrations

Each has its place.

---

## Decision Framework: Live vs. Local

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

### Hybrid Approach: The Best Pattern

Use **local for discovery, live for action**:

```
Step 1: Search local inventory
"Search azure-resources.json for all VMs tagged environment=staging"
→ Fast, finds candidates: vm-staging-1, vm-staging-2

Step 2: Verify live
"Using az cli, check current status of vm-staging-1 and vm-staging-2"
→ Confirms they still exist and gets current state

Step 3: Take action
"Stop vm-staging-2 to save costs"
→ Executes against live system
```

**Why this works**:
- Fast initial search (local)
- Verified before action (live)
- Reduced API calls (efficiency)

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

### When to Use MCP vs. CLI

| Scenario | MCP | CLI | Reason |
|----------|-----|-----|--------|
| Query Azure resources | ✅ Prefer | ✅ Works | MCP might be more structured |
| Complex az commands | ❌ No | ✅ Prefer | CLI more flexible |
| Update work items | ✅ Prefer | ✅ Works | MCP designed for this |
| Execute kubectl | ❌ No | ✅ Only option | MCP doesn't support |
| Search wiki | ✅ Prefer | ❌ Hard | MCP understands wiki structure |
| Git operations | ❌ No | ✅ Only option | Use git CLI |

**Reality**: You'll often default to CLI because it's familiar and flexible. Use MCP when it offers clear advantages.

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

```
Need current state?
├─ Yes → Live query (MCP/CLI)
└─ No → Check local data store

Making changes?
├─ Yes → Use CLI (more control)
└─ No → MCP or CLI both fine

Large dataset?
├─ Yes → Pull once, save locally, query local
└─ No → Direct query fine

Queried frequently?
├─ Yes → Local data store
└─ No → Live query acceptable

Destructive operation?
├─ Yes → Multi-step verification + CLI
└─ No → Standard workflow
```

---

## Summary

**Integration types**:
- Local data stores (fast, historical, bulk queries)
- CLI tools (flexible, full control)
- MCP servers (structured, AI-friendly)

**Best practice**: Combine all three
- Local for discovery
- MCP for verification
- CLI for action

**Safety**:
- Read operations: generally safe
- Write operations: review first
- Destructive operations: multi-step verification

---

## Next Steps

1. Identify which MCPs you have access to
2. Test MCP queries vs. equivalent CLI commands
3. Build local data stores for frequently queried data
4. Create integration workflows for your common tasks

---

**[← Back to Local Data Stores](04-local-data-stores.md)** | **[Practical Patterns →](06-practical-patterns.md)**
