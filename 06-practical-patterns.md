# Module 6: Practical Patterns

Real-world workflows and examples for common SRE tasks.

---

## Pattern 1: The Investigation Agent

**Use case**: Debugging a production issue that requires exploration and follow-up questions.

### Setup
```bash
# Start Codex in the relevant service directory
cd /company/SRE/helm/charts/my-service/

# Initial prompt
Context: Production pods for my-service are crashlooping
Available info:
- Recent logs saved to /tmp/my-service-crash-logs.txt
- Helm chart in current directory
- kubectl access to production cluster

Task: Investigate the root cause of the crashloop
```

### Workflow
The agent stays alive for iterative investigation:

```
You: "Check the logs for any obvious errors"
Agent: [analyzes logs, finds OOM killer messages]

You: "Look at the current memory limits in our helm values"
Agent: [shows values.yaml with limits: memory: "512Mi"]

You: "Compare to what other similar services use"
Agent: [searches other charts, finds they use 1Gi]

You: "Check our actual memory usage in Prometheus"
Agent: [queries metrics, shows average 800Mi usage]

You: "Create a fix and explain the changes needed"
Agent: [proposes updated values with justification]
```

**Key technique**: Keep the agent alive with all context loaded. Don't start fresh sessions for each question.

---

## Pattern 2: Parallel Updates with Coordination

**Use case**: Making related changes across multiple repositories or components.

### Setup: Blue-Green Cluster Swap

**Task breakdown**:
- Update helm chart A
- Update helm chart B (same repo as A)
- Update cluster sync script
- Search for related work items
- Document all changes

### Tab Layout
```
Tab 1 (Green):  Helm Chart A
  Location: /company/SRE/helm/charts/
  Command: git worktree add ../charts-worktree-a
  Task: Update chart A for new cluster

Tab 2 (Green):  Helm Chart B  
  Location: /company/SRE/helm/charts/
  Command: git worktree add ../charts-worktree-b
  Task: Update chart B for new cluster

Tab 3 (Blue):   Sync Script
  Location: /company/SRE/scripts/
  Task: Update cluster-sync.sh to handle helm changes

Tab 4 (Yellow): Work Item Search
  Location: /company/SRE/notes/
  Task: Search local work item replica for related items
  Status: Stays open as reference

Tab 5 (Green):  Master Coordination
  Location: /company/SRE/
  Task: Aggregate results and create wiki documentation
```

### Coordination Workflow

**Step 1**: Work happens in parallel (Tabs 1-3)

**Step 2**: Aggregate in master tab (Tab 5)
```
I've completed these changes:

Chart A: [paste summary from Tab 1]
Chart B: [paste summary from Tab 2]  
Sync Script: [paste summary from Tab 3]
Related Work Items: [reference from Tab 4]

Please:
1. Create a comprehensive wiki document for these changes
2. Generate a deployment checklist
3. Identify any dependencies I may have missed
```

**Step 3**: Use agent output to update wiki via Azure DevOps MCP

**Why it works**: Each tab maintains focused context. Manual aggregation ensures you review all changes before creating final documentation.

---

## Pattern 3: The Document Analysis Agent

**Use case**: Working with large reference documents (architecture docs, RFCs, vendor documentation).

### Setup
```bash
cd /company/SRE/docs/

# Load the document
Here's our 40-page Kubernetes architecture document [attach or paste]

Keep this loaded. I'll be asking questions about it throughout the day.
```

### Usage Patterns

**Reference queries**:
```
"What's our standard for pod resource requests?"
"Where do we document our backup procedures?"
"What's the process for emergency rollbacks?"
```

**Comparison queries**:
```
"Compare our current ingress config to what the architecture doc recommends"
"Does our implementation match the documented disaster recovery plan?"
```

**Implementation guidance**:
```
"I need to add a new service. According to our architecture doc, what 
do I need to configure for monitoring, logging, and alerting?"
```

**Why it works**: Document stays loaded in context. No need to re-upload or re-explain for each question.

---

## Pattern 4: The Dual Data Store Pattern

**Use case**: Fast local searches combined with live updates.

### Setup: Work Item Management

**Local replica** (for searching):
```
/company/SRE/notes/work-items/
├── my-work-items.json
├── team-work-items.json
└── last-updated.txt
```

**Azure DevOps MCP** (for updating):
- Connected via MCP server
- Used for writes and critical reads

### Workflow

**Tab 1: Search (Local)**
```
Search my local work item replica for all open items related to "helm chart updates"

[Fast search through JSON file]
→ Found items: 12345, 12347, 12389
```

**Tab 2: Update (Live)**
```
Using Azure DevOps MCP:

Update work item 12345:
- Status: In Progress → Done
- Add comment: "Updated ingress-nginx to 4.8, tested in staging"
- Link to related item: 12347
```

**Why both**: Local for fast searches, live for accurate writes.

**Maintenance**: Update local replica weekly or after major changes
```
"Regenerate my work item replica with current data from Azure DevOps"
```

---

## Pattern 5: The Handoff Chain

**Use case**: Long-running work that exceeds context window capacity.

### Monitoring Context Usage

Most tools show context usage. Keep an eye on it - when it starts feeling cluttered or you notice it climbing, consider a handoff.

### Handoff Workflow

**Step 1**: When context is getting full, prepare to handoff
```
Give me a handoff prompt I can copy into a new Codex session to continue this work.
```

**Step 2**: Agent generates comprehensive handoff
```
We're migrating the user-api service to the new Kubernetes cluster.

Location: /company/SRE/helm/charts/user-api/
Current branch: feature/cluster-migration

Completed:
- Updated Chart.yaml to version 2.1.0
- Modified values.yaml for new cluster endpoints
- Updated ingress configuration for new domain
- Tested template rendering with helm template
- Created git worktree at ../user-api-migration/

Remaining tasks:
- Update production values override (values/production.yaml)
- Test deployment in staging environment  
- Update monitoring dashboards for new cluster
- Document changes in wiki

Key decisions made:
- Using ClusterIP service instead of LoadBalancer (cost optimization)
- Maintaining existing resource limits (no changes needed)
- Added new health check endpoint configuration

Known issues:
- Staging namespace doesn't exist yet (needs to be created first)
- Some ConfigMaps reference old cluster name (need updating)

Files modified:
- Chart.yaml
- values.yaml
- templates/deployment.yaml (health check)
- templates/ingress.yaml (domain update)

Next immediate action: Create staging namespace, then test deployment.
```

**Step 3**: Copy entire handoff into new session

**Step 4**: Continue work in fresh context

**Why it works**: Agent knows its own context better than you do. It generates comprehensive handoffs automatically.

---

## Pattern 6: The Multi-Repo Investigation

**Use case**: Tracking down issues that span multiple repositories.

### Scenario
Database connection errors in production. Could be:
- Application code (Dev repo)
- Kubernetes configuration (SRE helm charts)
- Terraform infrastructure (SRE terraform)
- Network policies (SRE ansible)

### Approach: Fan-Out Investigation

```
Tab 1: Application code
  Location: /company/Dev/user-api/
  Task: Check database connection config and retry logic

Tab 2: Kubernetes config
  Location: /company/SRE/helm/charts/user-api/
  Task: Verify secrets, connection strings, and network policies

Tab 3: Infrastructure
  Location: /company/SRE/terraform/azure-infrastructure/
  Task: Check database firewall rules and network configuration

Tab 4: Network policies
  Location: /company/SRE/ansible/
  Task: Review any recent network policy changes

Tab 5: Aggregation
  Location: /company/SRE/
  Task: Collect findings and determine root cause
```

**Each tab** investigates independently, then reports findings to Tab 5 for synthesis.

---

## Pattern 7: The Runbook Generator

**Use case**: Convert an incident resolution into a reusable runbook.

### During Incident

**Investigation tab**:
```
Keep this tab open during the incident.
Document each step as we troubleshoot.

Issue: High database CPU usage
Investigation steps:
[Each command and finding gets added to context]
```

### After Incident

**Same tab**:
```
Based on our troubleshooting session above, create a runbook for future incidents of this type.

Format:
- Symptoms and alerts
- Investigation steps
- Common causes
- Resolution procedures
- Prevention measures

Save to: /company/SRE/notes/runbooks/database-high-cpu.md
```

**Why it works**: All context from the actual incident is already loaded. The runbook reflects real troubleshooting, not theoretical steps.

---

## Pattern 8: The Terraform Drift Detective

**Use case**: Identify differences between actual Azure resources and terraform state.

### Setup: Local Azure Inventory

**Build searchable inventory**:
```bash
cd /company/SRE/notes/inventory/

# Generate current state
Create a script that:
1. Queries all Azure resources via az cli
2. Outputs JSON with: name, type, location, resource group, key properties
3. Saves to azure-resources.json
4. Includes timestamp in last-updated.txt
```

### Drift Detection Workflow

**Tab 1: Inventory current state**
```
Run the Azure inventory script
Save output to azure-resources.json
```

**Tab 2: Compare to terraform**
```
Location: /company/SRE/terraform/azure-infrastructure/

Compare azure-resources.json to our terraform state.

Report:
- Resources in Azure but not in terraform
- Resources in terraform but not in Azure  
- Configuration differences for resources in both

Focus on: VMs, AKS clusters, storage accounts, network resources
```

**Tab 3: Resolution**
```
For each drift identified:
1. Determine if Azure or terraform is correct
2. Generate terraform to import unmanaged resources, OR
3. Generate commands to remove resources that shouldn't exist, OR
4. Generate terraform updates to match desired state
```

---

## Pattern 9: The Emergency Rollback

**Use case**: Fast rollback with documentation for post-mortem.

### Setup
```
Tab 1 (Red): Execute rollback
  - Immediate action
  - Rolling back helm deployment

Tab 2 (Yellow): Document actions  
  - Parallel documentation
  - Captures each step taken

Tab 3 (Blue): Investigation
  - Why did we need to rollback?
  - What broke?
```

### Tab 1: Execution
```
URGENT: Need to rollback user-api deployment

Current version: 2.1.0 (deployed 10 minutes ago)
Previous version: 2.0.3 (stable)
Location: /company/SRE/helm/charts/user-api/

Execute rollback to 2.0.3 now.
Show me each command before running.
```

### Tab 2: Concurrent Documentation
```
Document rollback in progress:

Time: [timestamp]
Service: user-api  
Reason: [paste error messages]
Action: Rolling back 2.1.0 → 2.0.3
Executed by: [your name]

[Keep updating as rollback progresses]
```

### Tab 3: Post-Rollback Analysis
```
Load the diff between versions 2.0.3 and 2.1.0

Analyze what changed and what likely caused the issue
Look for: configuration changes, dependency updates, code changes in critical paths
```

**Why separate tabs**: Rollback happens urgently in Tab 1. Documentation happens in parallel in Tab 2. Investigation can start immediately in Tab 3 without waiting for rollback completion.

---

## Pattern 10: The Configuration Validator

**Use case**: Validate changes across all environments before deploying.

### Setup
```
/company/SRE/helm/charts/my-service/
├── values.yaml (defaults)
├── values/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
```

### Validation Workflow
```
I'm about to change the resource limits in the my-service helm chart.

Please:
1. Show current resource limits in all environment value files
2. After I make changes, validate that:
   - All environments have consistent structure
   - Production has higher limits than staging
   - No environment is missing required fields
   - All syntax is valid YAML
3. Generate helm template output for each environment to catch any issues
```

**Catches**: Syntax errors, missing overrides, environment inconsistencies

---

## Anti-Patterns to Avoid

### ❌ The Everything Tab
One tab trying to do investigation + fixes + testing + documentation + wiki updates

**Why it fails**: Context becomes cluttered, focus is lost, hard to track what's been done

**Instead**: Separate tabs for separate concerns

---

### ❌ The Context-Free Request
```
"Fix the broken thing"
```

**Why it fails**: No information about what's broken, where it is, or what "fixed" looks like

**Instead**: Always provide context
```
The my-service deployment in production is crashlooping.
Logs at /tmp/my-service.log show OOM errors.
Helm chart at /company/SRE/helm/charts/my-service/
Current memory limit: 512Mi
```

---

### ❌ The Stale Data Store
You built a local Azure inventory 3 months ago and never updated it.

**Why it fails**: Agent makes decisions based on outdated information

**Instead**: 
- Update inventories regularly
- Include "last updated" timestamp
- Verify critical info against live sources when it matters

---

## Choosing the Right Pattern

| Scenario | Recommended Pattern |
|----------|-------------------|
| Investigating production issue | Investigation Agent |
| Multi-part infrastructure update | Parallel Updates with Coordination |
| Working with large docs | Document Analysis Agent |
| Managing work items | Dual Data Store |
| Long-running migration | Handoff Chain |
| Cross-repo troubleshooting | Multi-Repo Investigation |
| Post-incident documentation | Runbook Generator |
| Finding terraform drift | Drift Detective |
| Emergency response | Emergency Rollback |
| Pre-deployment validation | Configuration Validator |

---

## Next Steps

- Try one pattern with a real task this week
- Document what worked and what didn't
- Share your experience with the team

**[← Back to Core Concepts](01-core-concepts.md)** | **[Common Pitfalls →](07-common-pitfalls.md)**
