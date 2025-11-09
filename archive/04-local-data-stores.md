# Module 4: Local Data Stores

Building searchable, persistent context that AI agents can access anytime.

---

## The Problem

AI agents don't remember your infrastructure. Each session starts fresh:
- Don't know what Azure resources you have
- Can't recall past incidents
- Unaware of work item history
- No knowledge of your specific environment

**Traditional solution**: Manually explain everything in each session.

**Better solution**: Build searchable local data stores.

---

## What is a Local Data Store?

A structured file or set of files that:
- Contains information you query repeatedly
- Lives on your filesystem (accessible to AI)
- Is searchable via grep, jq, or AI natural language
- Gets updated periodically
- Serves as ground truth for context

**Think of it as**: Lightweight, personal RAG (Retrieval Augmented Generation) without the infrastructure overhead.

---

## When to Build a Data Store

### Good Candidates ✅
- Information queried repeatedly
- Large reference datasets
- Historical data (incidents, changes, decisions)
- Structured inventories (resources, services, configurations)
- Things that don't change every minute

### Poor Candidates ❌
- Real-time data (use live APIs instead)
- Information queried once
- Data that changes constantly
- Secrets (security risk)
- Information already in easily-accessible files

---

## Data Store Types

### Type 1: Resource Inventories

**Purpose**: Snapshot of infrastructure state

**Examples**:
- Azure resources
- Kubernetes resources
- Helm charts deployed
- Terraform-managed infrastructure

**Update frequency**: Weekly or after major changes

---

### Type 2: Work Item Replicas

**Purpose**: Local, searchable copy of work tracking system

**Examples**:
- Your assigned tasks
- Team backlog
- Blocked items
- Recently completed work

**Update frequency**: Daily or weekly

---

### Type 3: Historical Logs

**Purpose**: Searchable history for pattern finding

**Examples**:
- Incident reports
- Deployment logs
- Configuration changes
- Decision records

**Update frequency**: After each incident/deployment/decision

---

### Type 4: Documentation Indexes

**Purpose**: Searchable metadata about documentation

**Examples**:
- Runbook index
- Wiki page index
- External documentation references
- Internal procedures catalog

**Update frequency**: When documentation changes

---

## Format Selection

### JSON: Structured Data

**Use for**:
- Machine-first, human-second
- Complex nested structures
- Need to query specific fields
- Integration with other tools

**Example: Azure Resource Inventory**
```json
{
  "resources": [
    {
      "id": "/subscriptions/.../resourceGroups/production-rg/providers/Microsoft.Compute/virtualMachines/vm-prod-1",
      "name": "vm-prod-1",
      "type": "Microsoft.Compute/virtualMachines",
      "location": "eastus",
      "resourceGroup": "production-rg",
      "properties": {
        "vmSize": "Standard_D4s_v3",
        "osType": "Linux",
        "osName": "Ubuntu 22.04"
      },
      "tags": {
        "environment": "production",
        "owner": "sre-team",
        "cost-center": "infrastructure"
      }
    }
  ],
  "metadata": {
    "lastUpdated": "2024-11-07T10:00:00Z",
    "source": "az cli",
    "subscriptionId": "...",
    "resourceCount": 147
  }
}
```

**AI Usage**:
```
"Search azure-resources.json for all VMs in eastus region"
"Find resources tagged with environment=production"
"List all resources in the production-rg resource group"
```

**Pros**:
- Structured queries with jq
- AI can parse easily
- Programmatic updates simple

**Cons**:
- Not very human-readable
- Requires tools to view nicely
- Can get large

---

### Markdown: Human-Readable Documentation

**Use for**:
- Human-first, machine-second
- Narrative content
- Runbooks, procedures, guides
- Incident reports

**Example: Incident Log**
```markdown
# Incidents - November 2024

## INC-2024-123 - Database Connection Pool Exhausted
**Date**: 2024-11-07 14:23 UTC
**Severity**: P1
**Duration**: 45 minutes
**Services**: user-api, billing-api

### Symptoms
- 500 error rate spiked to 85%
- Database connection timeouts
- Application pods healthy but unresponsive

### Root Cause
Connection pool sized for 10 connections.
Traffic spike from new feature launch increased load 5x.

### Resolution
Increased pool from 10 to 50 connections:
- File: `/company/SRE/helm/charts/user-api/values.yaml`
- PR: #456
- Deployed: 15:00 UTC

### Prevention
- Added connection pool utilization monitoring
- Alert at 70% utilization
- Updated capacity planning runbook

---

## INC-2024-124 - Pod CrashLoop in Staging
...
```

**AI Usage**:
```
"Search incident logs for any issues related to database connections"
"Find all P1 incidents in the last 30 days"
"Has this error message appeared in previous incidents?"
```

**Pros**:
- Very human-readable
- Great for narrative content
- AI understands markdown well
- Easy to manually edit

**Cons**:
- Less structured for queries
- Harder to extract specific fields programmatically

---

### CSV: Simple Tabular Data

**Use for**:
- Simple, flat data
- Quick exports
- When JSON feels like overkill
- Scannable/greppable lists

**Example: Helm Charts Deployed**
```csv
name,namespace,chart_version,app_version,last_updated,status
user-api,production,2.1.0,v1.5.3,2024-11-07,deployed
billing-api,production,1.8.2,v2.0.1,2024-11-05,deployed
nginx-ingress,ingress,4.8.0,1.9.0,2024-11-01,deployed
```

**AI Usage**:
```
"Show me all helm releases in production namespace"
"Which charts were updated in the last week?"
"Find the app version for user-api"
```

**Pros**:
- Very simple
- Easy to create from command output
- Grep-friendly
- Spreadsheet compatible

**Cons**:
- No nested data
- Less expressive than JSON
- No metadata/timestamps built in

---

### Hybrid: JSON + Markdown

**Use for**: Best of both worlds

**Example: Runbook with Index**

**runbooks/index.json**:
```json
{
  "runbooks": [
    {
      "id": "001",
      "file": "disk-space-alerts.md",
      "title": "Disk Space Alert Response",
      "keywords": ["disk", "storage", "prometheus", "alert"],
      "alerts": ["DiskSpaceHigh", "DiskSpaceCritical"],
      "lastUpdated": "2024-11-07",
      "uses": 15
    },
    {
      "id": "002",
      "file": "pod-crashloop.md",
      "title": "Pod CrashLoop Debugging",
      "keywords": ["kubernetes", "pod", "crashloop", "restart"],
      "alerts": ["PodCrashLooping"],
      "lastUpdated": "2024-10-15",
      "uses": 8
    }
  ]
}
```

**runbooks/disk-space-alerts.md**:
```markdown
# Disk Space Alert Response
[Full runbook content in markdown]
```

**AI Usage**:
```
"Search runbook index for anything related to kubernetes crashes"
→ Finds "pod-crashloop.md"

"Open and summarize the pod crashloop runbook"
→ Reads the full markdown file
```

**Benefits**:
- Fast searching via index
- Full content still human-readable
- Best of both worlds

---

## Building Your First Data Store

### Example: Azure Resource Inventory

**Step 1: Decide what to capture**

Minimum:
- Resource name
- Resource type
- Location
- Resource group

Nice to have:
- Tags
- Key configuration properties
- Cost information

**Step 2: Create extraction script**

```bash
cd /company/SRE/notes/inventory/

# AI prompt:
"Create a script that:
1. Uses az cli to list all resources in our subscription
2. For each resource, extract: name, type, location, resourceGroup, tags
3. Output to azure-resources.json in structured format
4. Include metadata: timestamp, resource count
5. Save script as update-azure-inventory.sh"
```

**Generated script** (example):
```bash
#!/bin/bash

OUTPUT_FILE="azure-resources.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "Fetching Azure resources..."

# Get all resources
az resource list --output json > /tmp/az-resources-raw.json

# Transform to our format
jq --arg timestamp "$TIMESTAMP" '{
  resources: [
    .[] | {
      name: .name,
      type: .type,
      location: .location,
      resourceGroup: .resourceGroup,
      tags: .tags,
      id: .id
    }
  ],
  metadata: {
    lastUpdated: $timestamp,
    resourceCount: (. | length),
    source: "az cli"
  }
}' /tmp/az-resources-raw.json > "$OUTPUT_FILE"

echo "Inventory updated: $OUTPUT_FILE"
echo "Resources found: $(jq '.metadata.resourceCount' $OUTPUT_FILE)"
echo "$TIMESTAMP" > last-updated.txt

rm /tmp/az-resources-raw.json
```

**Step 3: Run and validate**
```bash
chmod +x update-azure-inventory.sh
./update-azure-inventory.sh

# Verify
jq '.metadata' azure-resources.json
jq '.resources | length' azure-resources.json
```

**Step 4: Test searchability**
```
"Search azure-resources.json for all resources of type Microsoft.Compute/virtualMachines"
"Find all resources in eastus location"
"Show me resources tagged with environment=production"
```

**Step 5: Schedule updates**
```bash
# Add to crontab or create reminder
# Weekly updates for relatively stable infrastructure
# Daily for rapidly changing environments
```

---

### Example: Work Item Replica

**Step 1: Decide scope**
- My assigned items?
- Entire team?
- Specific project only?

**Step 2: Extract from source**

```bash
cd /company/SRE/notes/work-items/

# Using Azure DevOps MCP
"Use Azure DevOps MCP to:
1. Query all work items assigned to me
2. Include: ID, title, state, assigned to, tags, description
3. Save to my-work-items.json
4. Include timestamp"
```

**Alternative without MCP**:
```bash
# Using Azure DevOps CLI
az boards query \
  --wiql "SELECT [ID], [Title], [State], [Assigned To], [Tags] FROM WorkItems WHERE [Assigned To] = @Me" \
  --output json > my-work-items.json
```

**Step 3: Make human-readable**

**AI Prompt**:
```
"Convert my-work-items.json to a more readable format.

Create my-work-items-readable.md with:
- Summary statistics (total, by state)
- Items grouped by state (In Progress, To Do, Blocked)
- Each item: ID, Title, Tags, link

Keep JSON for querying, markdown for reading."
```

**Step 4: Update regularly**
```bash
# Script: update-work-items.sh
#!/bin/bash

# Fetch latest
az boards query --wiql "..." --output json > my-work-items.json

# Generate readable version
# (AI can generate this script for you)

echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > last-updated.txt
```

---

### Example: Incident History

**Step 1: Create template**

**/company/SRE/notes/incidents/template.md**:
```markdown
# INC-YYYY-NNN - [Brief Title]

**Date**: YYYY-MM-DD HH:MM UTC
**Severity**: P1/P2/P3/P4
**Duration**: [X minutes/hours]
**Services Affected**: [list]

## Timeline
- HH:MM - [Event]
- HH:MM - [Event]
...

## Symptoms
[What users/systems experienced]

## Root Cause
[Technical explanation]

## Resolution
[What fixed it]

**Changed files**:
- [paths]

**Commands executed**:
```
[commands]
```

## Prevention
- [Action 1]
- [Action 2]

## Learnings
[What we learned]

## Related
- Runbook: [if created]
- Work items: [IDs]
- Similar incidents: [INC-XXX]
```

**Step 2: Use for each incident**

```bash
cp template.md 2024-11-07-database-connection-pool.md
# Fill in details during/after incident
```

**Step 3: Create monthly summaries**

**/company/SRE/notes/incidents/2024-11.md**:
```markdown
# Incidents - November 2024

## Summary
- Total incidents: 5
- P1: 1
- P2: 2
- P3: 2
- MTTR: 35 minutes average

## By Service
- user-api: 2 incidents
- database: 1 incident
- ingress: 2 incidents

---

[Individual incident details...]
```

**Step 4: Make searchable**

**AI Usage**:
```
"Search all incident files in /notes/incidents/ for anything related to database connection issues"
"Find all P1 incidents in the last 6 months"
"Has this error message appeared before?"
```

---

## Maintaining Data Stores

### Update Strategies

**Time-based**:
```bash
# Cron job for weekly updates
0 9 * * 1 cd /company/SRE/notes/inventory && ./update-azure-inventory.sh

# Daily work item updates
0 8 * * * cd /company/SRE/notes/work-items && ./update-work-items.sh
```

**Event-based**:
- After major infrastructure changes
- After deploying significant updates
- After incidents (update incident log immediately)

**On-demand**:
```
"Update the Azure inventory to reflect current state"
"Refresh my work items from Azure DevOps"
```

---

### Freshness Indicators

**Always include last-updated timestamp**:
```
/notes/inventory/
├── azure-resources.json
├── last-updated.txt          # "2024-11-07T10:00:00Z"
└── update-azure-inventory.sh
```

**In your data**:
```json
{
  "metadata": {
    "lastUpdated": "2024-11-07T10:00:00Z",
    "validUntil": "2024-11-14T10:00:00Z"  // Optional
  }
}
```

**AI can check freshness**:
```
"Check when azure-resources.json was last updated.
If older than 7 days, remind me to refresh it."
```

---

### Dealing with Stale Data

**Warning prompt**:
```
"Before using azure-resources.json for decisions, check when it was last updated.
If older than 1 week, warn me and suggest refreshing."
```

**Critical decisions**:
```
"Use azure-resources.json to find candidates for cleanup.
Then verify each one against live Azure before taking action."
```

**Rule**: Use local for discovery, verify live for action.

---

## Advanced: Multi-Source Data Stores

### Combining Terraform + Live Azure

**Purpose**: Drift detection

**Step 1: Extract Terraform state**
```bash
cd /company/SRE/terraform/azure-infrastructure/

# AI prompt:
"Extract from terraform state:
- All managed resources
- Resource names, types, key properties
Save to /notes/inventory/terraform-state-export.json"
```

**Step 2: Extract live Azure**
```bash
# Already have azure-resources.json from earlier
```

**Step 3: Compare**
```
"Compare terraform-state-export.json to azure-resources.json

Report:
1. Resources in Azure but not in Terraform (drift - unmanaged)
2. Resources in Terraform but not in Azure (drift - deleted)
3. Configuration differences for resources in both

Focus on: VMs, AKS clusters, storage accounts, networking"
```

**Output**: Drift report
```markdown
# Azure Drift Report - 2024-11-07

## Unmanaged Resources (in Azure, not in Terraform)
- vm-test-123 (probably should be deleted)
- storage-dev-temp (temporary, can ignore)

## Missing Resources (in Terraform, not in Azure)
- None

## Configuration Drift
- vm-prod-1: Size changed from Standard_D4s_v3 to Standard_D8s_v3
  - Terraform says: D4s_v3
  - Azure shows: D8s_v3
  - Action: Update Terraform or revert Azure
```

---

## Searchability Best Practices

### Structure for Queries

**Poor**:
```json
{
  "data": "vm-prod-1,eastus,production,vm-prod-2,westus,staging"
}
```

**Good**:
```json
{
  "resources": [
    {
      "name": "vm-prod-1",
      "location": "eastus",
      "environment": "production"
    },
    {
      "name": "vm-prod-2",
      "location": "westus",
      "environment": "staging"
    }
  ]
}
```

**Why**: Structured queries possible.

---

### Include Keywords

**For markdown files**:
```markdown
# Disk Space Alert Response

**Keywords**: disk, storage, prometheus, alert, cleanup, space
**Related Alerts**: DiskSpaceHigh, DiskSpaceCritical
**Related Services**: All

[Content...]
```

**AI search**:
```
"Search runbooks for keyword 'prometheus'"
```

---

### Use Consistent Naming

**Poor**:
- some-file.json
- AnotherFile.json
- yet_another_file.json

**Good**:
- azure-resources.json
- work-items.json
- helm-deployments.json

Consistency helps AI (and humans) know what to look for.

---

## Security Considerations

### What NOT to Store

❌ **Secrets**:
- Passwords
- API keys
- Certificates
- Connection strings with passwords

❌ **PII**:
- Personal information
- Customer data
- Email addresses (unless necessary)

❌ **Proprietary Code**:
- Be cautious with business logic
- Check company policies

---

### What's Safe

✅ **Resource metadata**:
- Names, types, locations
- Non-sensitive configuration

✅ **Operational data**:
- Incident reports (sanitized)
- Deployment logs
- Runbooks

✅ **Public information**:
- Documentation
- Architecture decisions

---

### Sanitization

**When saving incident logs**:
```
"Create incident report from today's outage.
Sanitize any sensitive information:
- Replace actual API keys with [REDACTED]
- Remove customer identifiers
- Generalize error messages if they contain secrets"
```

---

## Real-World Examples

### Example 1: Helm Chart Inventory

**File**: `/notes/inventory/helm-deployments.json`

**Update script**:
```bash
#!/bin/bash
kubectl get helmreleases -A -o json | \
jq '{
  releases: [
    .items[] | {
      name: .metadata.name,
      namespace: .metadata.namespace,
      chart: .spec.chart.spec.chart,
      version: .spec.chart.spec.version,
      lastApplied: .status.lastAppliedRevision,
      status: .status.conditions[0].status
    }
  ],
  metadata: {
    lastUpdated: now | strftime("%Y-%m-%dT%H:%M:%SZ"),
    cluster: "production"
  }
}' > /company/SRE/notes/inventory/helm-deployments.json
```

**AI Usage**:
```
"Search helm-deployments.json for all charts in the production namespace"
"Which helm releases are using chart version 2.x?"
"Show me any releases with failed status"
```

---

### Example 2: Common Error Patterns

**File**: `/notes/error-patterns.md`

```markdown
# Common Error Patterns and Solutions

## "Connection refused" on port 5432
**Pattern**: `Error: connect ECONNREFUSED 10.0.0.5:5432`
**Cause**: Database not reachable
**Check**:
1. Database pod running?
2. Network policies allowing traffic?
3. Connection string correct?
**Solution**: See runbook `database-connectivity.md`
**Incidents**: INC-2024-089, INC-2024-102

---

## "OOMKilled" in pod logs
**Pattern**: `State: Terminated, Reason: OOMKilled`
**Cause**: Pod exceeded memory limit
**Check**:
1. Current memory limit
2. Actual memory usage (metrics)
3. Memory leaks in application?
**Solution**: See runbook `oom-debugging.md`
**Incidents**: INC-2024-095, INC-2024-110, INC-2024-123

---
```

**AI Usage**:
```
"Search error-patterns.md for anything related to database connection issues"
"I'm seeing 'OOMKilled' - what incidents have we had with this?"
```

---

## Measuring Success

Your data store is working when:

✅ **You search it regularly** instead of querying live systems
✅ **AI finds answers quickly** without clarification
✅ **It's up to date** (last updated within freshness window)
✅ **Others on team use it** (if shared)
✅ **It saves time** vs. manual lookups

---

## Verification Patterns: Keeping Local Data Accurate

**The fundamental challenge**: Local data stores are only useful if they accurately reflect reality.

Stale or inaccurate local data is worse than no local data—it leads to wrong decisions based on outdated information.

### The Verification Principle

**Local data is a cache, not the source of truth.**

Your verification workflow should ensure:
- Data accurately represents production at time of capture
- You know when data was last updated
- You can detect when data has become stale
- You refresh at appropriate intervals
- You verify against live sources before critical decisions

### Verifying Data Accuracy

**When building or updating a data store, verify the extraction is correct.**

**Example: Azure Resource Inventory**

```bash
# After running your inventory script
./update-azure-inventory.sh

# Verify the results make sense
echo "Verification checks:"

# 1. Count matches expectations
RESOURCE_COUNT=$(jq '.metadata.resourceCount' azure-resources.json)
echo "Total resources: $RESOURCE_COUNT"
echo "Expected: ~150 (adjust based on your environment)"

# 2. Spot-check known resources exist
jq '.resources[] | select(.name == "vm-prod-1")' azure-resources.json
echo "✓ Found known VM vm-prod-1"

# 3. Check for resources in expected locations
EASTUS_COUNT=$(jq '[.resources[] | select(.location == "eastus")] | length' azure-resources.json)
echo "Resources in eastus: $EASTUS_COUNT"

# 4. Verify resource groups are complete
jq '[.resources[] | .resourceGroup] | unique' azure-resources.json
echo "Resource groups found - verify none are missing"

# 5. Compare sample to live Azure
echo "Comparing sample resource to live state..."
az resource show --ids "/subscriptions/.../vm-prod-1" --output json > /tmp/live-vm.json
# [Manual verification that key fields match]
```

**For work items**:
```bash
# After extracting work items
./update-work-items.sh

# Verify extraction
echo "Verification:"
echo "Items in JSON: $(jq '. | length' my-work-items.json)"
echo "Expected based on Azure DevOps query: [your count]"

# Spot-check a known item
jq '.[] | select(.id == "12345")' my-work-items.json
echo "✓ Confirmed item 12345 is in export"

# Verify all expected states are present
jq '[.[].state] | unique' my-work-items.json
echo "States found: [should see Active, Closed, etc.]"
```

### Update Frequency Decisions

**Not all data has the same staleness tolerance.**

Different types of data require different refresh frequencies:

**High-frequency refresh (Daily or on-demand)**:
- Deployment status
- Active work items
- Incident logs (during active incident)
- Resource quotas and usage

**Medium-frequency refresh (Weekly)**:
- Infrastructure inventories (VMs, storage, networking)
- Service configurations
- Team membership and permissions
- Helm chart deployments

**Low-frequency refresh (Monthly or on major changes)**:
- Architecture documentation
- Decision logs
- Runbook indexes
- Historical incident archives

**Decision framework**:
```
Ask yourself:
1. How often does this data change in reality?
2. What's the cost of using slightly stale data?
3. How expensive is the refresh operation?
4. Am I using this data for read-only discovery or for actions?

Discovery = can tolerate staleness
Actions = require verification against live sources
```

### Example: Staleness Tolerance by Use Case

**Resource cleanup decision**:
```
Use case: Find old VMs to potentially delete
Tolerance: Medium (1-2 weeks)
Why: Discovery phase, not taking action yet

Workflow:
1. Search local inventory for VMs created >90 days ago
2. Create candidate list
3. VERIFY each candidate against live Azure before deletion
4. Local data found candidates, live data confirmed current state
```

**Incident response**:
```
Use case: Which services depend on the failing database?
Tolerance: Low (must be current)
Why: Making real-time decisions

Workflow:
1. Check local service catalog for quick overview
2. Verify dependencies with live queries
3. Don't trust stale data for incident response
```

**Architecture planning**:
```
Use case: How many microservices do we have?
Tolerance: High (1 month acceptable)
Why: Strategic planning, not operational decisions

Workflow:
1. Use local inventory for counts and patterns
2. No need to refresh for high-level planning
```

### Detecting Stale Data

**Build staleness indicators into your data stores.**

**Timestamp-based detection**:

```bash
# Check when inventory was last updated
LAST_UPDATE=$(cat /notes/inventory/last-updated.txt)
CURRENT_TIME=$(date -u +%s)
LAST_UPDATE_TIME=$(date -d "$LAST_UPDATE" +%s)
AGE_DAYS=$(( ($CURRENT_TIME - $LAST_UPDATE_TIME) / 86400 ))

if [ $AGE_DAYS -gt 7 ]; then
  echo "⚠️  WARNING: Inventory is $AGE_DAYS days old"
  echo "Consider refreshing before making decisions"
fi
```

**AI-assisted staleness checks**:

```
Before using azure-resources.json for cleanup decisions, check the
metadata.lastUpdated field. If older than 7 days, warn me and suggest
refreshing the inventory first.
```

**Staleness warnings in data files**:

```json
{
  "metadata": {
    "lastUpdated": "2024-11-01T10:00:00Z",
    "validUntil": "2024-11-08T10:00:00Z",
    "staleness": "This data is X days old. Verify critical resources against live Azure.",
    "refreshCommand": "./update-azure-inventory.sh"
  }
}
```

### Building Trust in Local Inventories

**Trust is earned through verification.**

**Initial trust building**:

1. **Create inventory** with extraction script
2. **Spot-check** 5-10 items against live sources
3. **Verify counts** match expected reality
4. **Test searches** for known items
5. **Use for discovery** (low-risk queries)
6. **Verify hits against live** before actions
7. **Build confidence** through repeated accuracy

**Ongoing trust maintenance**:

```bash
# Monthly verification script
#!/bin/bash
# verify-inventory-accuracy.sh

echo "Inventory Accuracy Check"
echo "========================"

# 1. Check last update time
echo "Last updated: $(cat last-updated.txt)"

# 2. Sample 5 random resources
echo "Sampling 5 resources for live verification..."
SAMPLE=$(jq -r '.resources[] | .id' azure-resources.json | shuf -n 5)

for resource_id in $SAMPLE; do
  echo "Checking: $resource_id"

  # Check if resource still exists in Azure
  if az resource show --ids "$resource_id" &>/dev/null; then
    echo "  ✓ Exists in Azure"
  else
    echo "  ✗ NOT FOUND in Azure - inventory is stale"
  fi
done

# 3. Check for count drift
LOCAL_COUNT=$(jq '.metadata.resourceCount' azure-resources.json)
LIVE_COUNT=$(az resource list --query 'length(@)')

echo "Resource counts:"
echo "  Local inventory: $LOCAL_COUNT"
echo "  Live Azure: $LIVE_COUNT"

DIFF=$((LIVE_COUNT - LOCAL_COUNT))
if [ ${DIFF#-} -gt 10 ]; then
  echo "  ⚠️  Significant drift detected ($DIFF resources)"
  echo "  Consider refreshing inventory"
else
  echo "  ✓ Counts are reasonably close"
fi
```

### Refresh Patterns and Automation

**Automated refresh with verification**:

```bash
#!/bin/bash
# update-azure-inventory.sh with built-in verification

echo "Updating Azure inventory..."

# Create temporary new inventory
az resource list --output json > /tmp/azure-resources-new.json

# Transform to our format
jq --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{
  resources: [ .[] | {name, type, location, resourceGroup, tags, id} ],
  metadata: {
    lastUpdated: $timestamp,
    resourceCount: (. | length),
    source: "az cli"
  }
}' /tmp/azure-resources-new.json > /tmp/azure-inventory-formatted.json

# Verification before replacing old inventory
OLD_COUNT=$(jq '.metadata.resourceCount' azure-resources.json 2>/dev/null || echo "0")
NEW_COUNT=$(jq '.metadata.resourceCount' /tmp/azure-inventory-formatted.json)

echo "Verification:"
echo "  Old inventory: $OLD_COUNT resources"
echo "  New inventory: $NEW_COUNT resources"

# Sanity check: if new count is drastically different, require confirmation
DIFF=$((NEW_COUNT - OLD_COUNT))
if [ ${DIFF#-} -gt 20 ]; then
  echo "⚠️  Resource count changed by $DIFF"
  echo "This might indicate a problem with the extraction."
  read -p "Continue? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. Old inventory unchanged."
    exit 1
  fi
fi

# Replace old inventory with new
mv /tmp/azure-inventory-formatted.json azure-resources.json
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > last-updated.txt

echo "✓ Inventory updated successfully"
echo "  New count: $NEW_COUNT resources"
echo "  Timestamp: $(cat last-updated.txt)"

# Cleanup
rm -f /tmp/azure-resources-new.json
```

**Scheduled refresh with cron**:

```bash
# Weekly inventory refresh
0 9 * * 1 cd /company/SRE/notes/inventory && ./update-azure-inventory.sh >> refresh.log 2>&1

# Daily work item refresh
0 8 * * * cd /company/SRE/notes/work-items && ./update-work-items.sh >> refresh.log 2>&1

# Monthly verification check
0 10 1 * * cd /company/SRE/notes/inventory && ./verify-inventory-accuracy.sh >> verification.log 2>&1
```

**Event-driven refresh**:

```bash
# After major infrastructure changes
echo "Major infrastructure change completed. Refreshing inventory..."
cd /company/SRE/notes/inventory && ./update-azure-inventory.sh

# After deployment
echo "Deployment complete. Updating helm inventory..."
cd /company/SRE/notes/inventory && ./update-helm-deployments.sh
```

> ⚠️ **Accountability**: You are responsible for the accuracy of your local data stores. Using stale data for production decisions without verification is negligent. Always verify against live sources before taking actions that could impact production systems.

### The Verification Workflow

**Standard pattern for using local data safely**:

```
Phase 1 - Discovery (use local data)
├─ Search local inventory for candidates
├─ Identify patterns and potential issues
├─ Create list of items for investigation
└─ Fast, low-risk exploration

Phase 2 - Verification (use live data)
├─ Check each candidate against live source
├─ Verify current state matches local data
├─ Flag any discrepancies
└─ Ensure accuracy before action

Phase 3 - Action (verified data only)
├─ Make decisions based on verified data
├─ Execute changes with confidence
├─ Document actions taken
└─ Update local inventory if significant changes made
```

### Key Takeaways

1. **Local data is a cache** - Never trust it blindly for production decisions
2. **Different staleness tolerance** - Match refresh frequency to data usage
3. **Verify before actions** - Discovery can use stale data, actions require verification
4. **Build trust through testing** - Spot-check accuracy regularly
5. **Automate verification** - Scripts that check accuracy save time and build confidence
6. **Update after major changes** - Significant infrastructure changes should trigger refresh
7. **You're accountable** - Stale data decisions are your responsibility

---

## Quick Start Checklist

Building your first data store:

1. **Pick one type** - Start small
2. **Choose format** - JSON, Markdown, or both
3. **Create extraction script** - Let AI help
4. **Test searchability** - Can AI find what you need?
5. **Schedule updates** - Cron or manual reminder
6. **Build verification** - Add accuracy checks
7. **Use it for a week** - See if it's valuable
8. **Iterate** - Improve structure based on usage

---

## Next Steps

- Build one data store this week
- Test it with real queries
- Share with your team if useful

---

**[← Back to Multi-Tab Orchestration](03-multi-tab-orchestration.md)** | **[Integration Patterns →](05-integration-patterns.md)**
