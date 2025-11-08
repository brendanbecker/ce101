# Example Prompts Library

Copy-paste templates for common SRE tasks. Customize for your specific needs.

---

## Investigation & Troubleshooting

### Production Issue Investigation
```
Context: [service-name] in production is [experiencing symptom]

Available information:
- Logs: [path-to-logs]
- Configuration: [path-to-config]
- Recent changes: [describe recent deploys/changes]
- Metrics: [relevant metrics observations]

Task: Investigate root cause and propose solution
```

### Error Log Analysis
```
Analyze the error logs at [log-path]

Focus on:
- Errors in timeframe [start-time] to [end-time]
- Pattern: [specific error message or pattern]
- Related services: [list related services]

Identify: frequency, root cause, and recommend fix
```

### Performance Degradation
```
Service [name] is experiencing performance issues

Symptoms:
- [metric] has increased from [baseline] to [current]
- Started at [timestamp]
- Affecting [scope]

Configuration: [path-to-helm-chart or terraform]
Recent changes: [list recent changes]

Investigate and recommend optimization
```

---

## Configuration Updates

### Helm Chart Update
```
I need to update the [service-name] helm chart

Location: /company/SRE/helm/charts/[service-name]/
Current version: [version]
Change needed: [describe change]
Reason: [why this change]

Please:
1. Show current configuration
2. Make the requested changes
3. Validate syntax
4. Highlight any potential issues
```

### Resource Limit Adjustment
```
Update resource limits for [service-name]

Chart location: [path]
Current values:
- requests: cpu [current], memory [current]
- limits: cpu [current], memory [current]

New values:
- requests: cpu [new], memory [new]
- limits: cpu [new], memory [new]

Justification: [reason based on metrics]

Update and verify no conflicts with HPA or other policies
```

### Environment Variable Update
```
Add/update environment variable in [service-name]

Location: [helm-chart-path]/templates/deployment.yaml
Environment: [dev/staging/production]

Variable: [VAR_NAME]
Value: [value or "from secret"]
Purpose: [why adding this]

Update appropriate files and explain any cascading changes
```

---

## Terraform Operations

### Resource Creation
```
Create new [resource-type] in Azure via Terraform

Location: /company/SRE/terraform/[module-name]/
Resource: [specific resource name]
Specifications:
- [spec 1]
- [spec 2]

Follow existing patterns in this module
Show me the code before we apply
```

### State Analysis
```
Compare terraform state to actual Azure resources

Module: /company/SRE/terraform/[module-name]/
Focus on: [resource types]

Identify:
- Resources in Azure but not in state
- Resources in state but not in Azure
- Configuration drift

Save findings to /notes/drift-report-[date].md
```

### Module Update
```
Update terraform module [module-name]

Current version: [version]
Target version: [version]
Location: [path]

Please:
1. Review CHANGELOG for breaking changes
2. Update module version
3. Identify required configuration changes
4. Generate migration plan
```

---

## Documentation

### Runbook Creation
```
Create runbook for [incident-type]

Based on: Recent incident [INC-number] or [describe situation]
Information sources:
- [incident-log-path]
- [solution-implemented]
- [related-documentation]

Format:
- Symptoms and alerts
- Investigation steps
- Common causes
- Resolution procedures
- Prevention measures

Save to: /company/SRE/notes/runbooks/[name].md
```

### Architecture Documentation
```
Document the architecture for [system/service]

Components:
- [list main components]
- [data flows]
- [dependencies]

Reference:
- Code: [paths]
- Configs: [paths]
- Existing docs: [paths]

Create comprehensive architecture document at /docs/[name]-architecture.md
Include diagrams in mermaid format
```

### Change Documentation
```
Document the changes made in [task/PR/work-item]

Changes:
- [list changes made]

Files modified:
- [paths]

Testing completed:
- [what was tested]

Create deployment notes and update relevant documentation
Format for wiki publication
```

---

## Kubernetes Operations

### Deployment Investigation
```
Investigate deployment [name] in namespace [namespace]

Issue: [describe problem]
Cluster: [cluster-name]

Check:
- Pod status and logs
- Resource utilization
- Events
- Configuration vs. desired state

Helm chart location: [path]
Suggest fixes based on findings
```

### Resource Scaling
```
Scale [deployment-name] resources

Current: [replicas] replicas, [resources]
Target: [new-replicas] replicas, [new-resources]
Reason: [justification with metrics]

Location: [helm-chart-path]

Update configuration and explain any HPA adjustments needed
```

---

## MCP Operations

### Azure Resource Query
```
Using Azure MCP:

Query [resource-type] in resource group [rg-name]
Filter: [specific criteria]
Return: [specific properties needed]

Format results as table/JSON for further analysis
```

### Work Item Management
```
Using Azure DevOps MCP:

Action: [Create/Update/Search] work item
Project: [project-name]
Details:
- [relevant information]

For search: find items matching [criteria]
For update: update item [ID] with [changes]
For create: create new [type] with [details]
```

### Wiki Update
```
Using Azure DevOps MCP:

Update wiki page: [page-path]
Project: [project-name]

Content to add/update:
[describe changes or provide content]

Maintain existing formatting and structure
```

---

## Data Store Operations

### Inventory Generation
```
Generate [type] inventory

Sources: [Azure/Git/Files/etc]
Output location: /company/SRE/notes/inventory/[name].json
Include fields:
- [field 1]
- [field 2]

Make searchable and include last-updated timestamp
Create README with usage instructions
```

### Inventory Search
```
Search local inventory at [path]

Looking for: [search criteria]
Context: [why you need this]

Return matches with relevant details
```

### Inventory Update
```
Update existing inventory at [path]

Method: [regenerate/append/modify]
Source: [where to pull new data]

Maintain format consistency
Update last-modified timestamp
```

---

## Git Operations

### Worktree Setup
```
Set up git worktree for [task]

Repository: [path-to-repo]
Branch: [branch-name]
Worktree location: [where-to-create]

Purpose: [what you'll work on]

Create worktree and set up for work
```

### Commit Message Generation
```
Generate commit message for these changes:

Files modified:
- [file 1]: [what changed]
- [file 2]: [what changed]

Context: [why changes were made]
Related: [work-item or ticket]

Follow conventional commits format
```

---

## Handoff Prompts

### Standard Handoff
```
Give me a handoff prompt I can copy into a new Codex session to continue this work.

Include:
- Current location and files
- Work completed
- Work remaining
- Key decisions made
- Next immediate action
```

### Emergency Handoff
```
Quick handoff needed - context almost full

Summarize:
- Critical context only
- Must-remember decisions
- Immediate next steps

Concise version for emergency continuation
```

---

## Multi-Tab Coordination

### Master Tab Aggregation
```
I've completed work in multiple tabs:

Tab 1 (Helm updates): [paste summary]
Tab 2 (Terraform changes): [paste summary]
Tab 3 (Testing results): [paste summary]

Now:
1. Identify any dependencies or conflicts
2. Create deployment checklist
3. Generate comprehensive documentation
4. Prepare PR description
```

---

## Validation & Testing

### Configuration Validation
```
Validate this configuration before deployment

File: [path]
Type: [helm/terraform/ansible/etc]
Environment: [target environment]

Check:
- Syntax correctness
- Best practices compliance
- Security issues
- Consistency with other environments

Report any issues found
```

### Dry Run Request
```
Perform dry-run/plan for these changes

Configuration: [path]
Target: [environment/resource]

Show me what will change without applying
Highlight any destructive operations
```

---

## Tips for Using These Templates

1. **Replace bracketed placeholders** with your specific information
2. **Add context** relevant to your situation
3. **Include file paths** - always be specific
4. **Adjust detail level** based on complexity
5. **Combine templates** when needed for complex tasks

---

## Creating Your Own Templates

When you develop a good prompt pattern:

1. Save it to this file
2. Share with team
3. Add context about when to use it
4. Include example of filled-in version

**Template structure**:
```
### Task Name
```
[Prompt template with [placeholders]]

Context needed: [list]
When to use: [scenario]
```
```

---

**Need more examples?** Add your own as you discover effective patterns!
