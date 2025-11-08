# Module 3: Multi-Tab Orchestration

Managing multiple AI agents working on different aspects of complex tasks simultaneously.

---

## The Core Concept

**One tab, one job.**

Instead of cramming everything into a single context window, use multiple terminal tabs with isolated AI sessions, each focused on a specific concern.

Think of it like having a team of specialists rather than one generalist trying to do everything.

---

## Why Multi-Tab Orchestration Works

### The Problem with Single-Tab Everything

```
One tab trying to:
- Investigate production issue
- Update helm chart
- Modify terraform
- Test changes
- Update documentation
- Create work items
- Write post-mortem
```

**What happens**:
- Context becomes cluttered
- Hard to track progress
- Easy to lose focus
- Can't parallelize work
- Difficult to handoff
- Context window fills faster

---

### The Multi-Tab Solution

```
Tab 1 (Blue):  Investigation
Tab 2 (Green): Helm updates
Tab 3 (Green): Terraform updates
Tab 4 (Yellow): Work item search (reference)
Tab 5 (Green): Master coordination
```

**Benefits**:
- Each agent stays focused
- Parallel work on independent tasks
- Clear separation of concerns
- Easier to track what's done
- Better handoffs
- More efficient context usage

---

## Tab Types and Color Coding

Use consistent colors to quickly identify tab purposes.

### 🟢 Green: Active Work
**Purpose**: Making changes, implementing solutions

**Examples**:
- Updating helm charts
- Writing terraform code
- Modifying scripts
- Creating documentation

**Characteristics**:
- Write operations
- Modifying files
- Git commits

---

### 🔵 Blue: Investigation / Read-Only
**Purpose**: Gathering information, analyzing

**Examples**:
- Investigating errors
- Analyzing logs
- Reviewing configurations
- Searching documentation

**Characteristics**:
- Read operations
- No file modifications
- Exploratory work

---

### 🟡 Yellow: Long-Running Reference
**Purpose**: Stays open with reference material loaded

**Examples**:
- Document analysis agent with architecture docs
- Work item search results
- Metrics/monitoring data
- Configuration references

**Characteristics**:
- Rarely modified
- Queried repeatedly
- Stays open all day/week
- Large context loaded

---

### 🔴 Red: Urgent / Emergency
**Purpose**: Critical work requiring immediate attention

**Examples**:
- Production incident response
- Emergency rollbacks
- Hotfix implementations
- Critical outage investigation

**Characteristics**:
- High priority
- Time-sensitive
- Requires focus
- Often documented in parallel (Blue tab)

---

## Multi-Tab Patterns

### Pattern 1: Parallel Independent Work

**Scenario**: Update multiple helm charts in the same repository

**Tab Structure**:
```
Tab 1 (Green): Chart A - git worktree
  Location: /company/SRE/helm/charts-worktree-a/
  Task: Update service-a chart for new cluster

Tab 2 (Green): Chart B - git worktree
  Location: /company/SRE/helm/charts-worktree-b/
  Task: Update service-b chart for new cluster

Tab 3 (Green): Chart C - git worktree
  Location: /company/SRE/helm/charts-worktree-c/
  Task: Update service-c chart for new cluster
```

**Workflow**:
1. Set up git worktrees (or have AI do it)
2. Open separate tab for each worktree
3. Work on each chart independently
4. No blocking - all work happens in parallel

**Why it works**: Each chart update is independent. No need to wait for one to finish before starting another.

---

### Pattern 2: Investigation → Implementation → Documentation

**Scenario**: Troubleshoot and fix production issue

**Tab Structure**:
```
Tab 1 (Blue): Investigation
  Location: /company/SRE/
  Task: Investigate root cause of crashloop
  Stays alive: Yes - reference during implementation

Tab 2 (Green): Implementation
  Location: /company/SRE/helm/charts/my-service/
  Task: Implement fix based on findings from Tab 1
  Context: Receives summary from Tab 1

Tab 3 (Yellow): Documentation
  Location: /company/SRE/notes/
  Task: Create runbook and update incident log
  Context: Receives summary from Tabs 1 and 2
```

**Workflow**:
1. Tab 1: Investigate until root cause found
2. Tab 2: Start implementation (Tab 1 stays alive for questions)
3. Tab 3: Document while Tab 2 implements
4. Tab 3 aggregates everything at the end

**Why it works**: Separation of concerns. Investigation context doesn't clutter implementation. Documentation can happen in parallel.

---

### Pattern 3: Multi-Repo Investigation

**Scenario**: Track down issue spanning multiple repositories

**Tab Structure**:
```
Tab 1 (Blue): Application Code
  Location: /company/Dev/user-api/
  Task: Check connection handling and retry logic

Tab 2 (Blue): Kubernetes Config
  Location: /company/SRE/helm/charts/user-api/
  Task: Verify secrets and network policies

Tab 3 (Blue): Infrastructure
  Location: /company/SRE/terraform/azure-infrastructure/
  Task: Check database firewall rules

Tab 4 (Blue): Network Policies
  Location: /company/SRE/ansible/
  Task: Review recent network policy changes

Tab 5 (Green): Synthesis & Fix
  Location: /company/SRE/
  Task: Collect findings and implement solution
```

**Workflow**:
1. Tabs 1-4: Investigate independently
2. Each tab reports findings
3. Tab 5: Synthesize findings, identify root cause
4. Tab 5: Coordinate fix (may delegate to other tabs)

**Why it works**: Parallel investigation across different repos. Each specialist (tab) knows its domain.

---

### Pattern 4: Master + Workers with Aggregation

**Scenario**: Complex multi-component update

**Tab Structure**:
```
Tab 1 (Green): Worker - Helm updates
  Task: Update all helm charts
  Output: Summary of changes

Tab 2 (Green): Worker - Terraform updates
  Task: Update infrastructure code
  Output: Summary of changes

Tab 3 (Blue): Worker - Testing validation
  Task: Validate changes in staging
  Output: Test results

Tab 4 (Yellow): Reference - Work items
  Task: Search related work items
  Output: Context about requirements

Tab 5 (Green): Master - Coordination
  Task: Aggregate all work and create deliverables
  Input: Summaries from Tabs 1-4
  Output: PR descriptions, wiki docs, deployment plan
```

**Workflow**:
1. Tabs 1-3: Work independently
2. Tab 4: Provides reference context to others
3. Workers complete their tasks
4. Workers report to master (manual copy-paste or handoff)
5. Master creates final deliverables

**Coordination Prompt** (in Tab 5):
```
I've completed work in multiple tabs:

Tab 1 - Helm updates:
[paste summary]

Tab 2 - Terraform changes:
[paste summary]

Tab 3 - Testing results:
[paste summary]

Related work items (from Tab 4):
[paste relevant items]

Now:
1. Identify any dependencies or conflicts between these changes
2. Create a deployment checklist
3. Generate comprehensive documentation for the wiki
4. Draft PR description with all context
```

---

### Pattern 5: Emergency Response with Parallel Documentation

**Scenario**: Production incident requiring immediate action

**Tab Structure**:
```
Tab 1 (Red): Execution
  Location: /company/SRE/helm/charts/my-service/
  Task: Execute rollback NOW
  Characteristic: Speed matters

Tab 2 (Yellow): Documentation
  Location: /company/SRE/notes/incidents/
  Task: Document actions in real-time
  Updates: As Tab 1 progresses

Tab 3 (Blue): Investigation
  Location: /company/SRE/
  Task: Determine what went wrong
  Starts: After rollback initiated
```

**Workflow**:
1. Tab 1: Immediate action (rollback, scale down, etc.)
2. Tab 2: Document every step as it happens
3. Tab 3: Investigate cause in parallel
4. Post-incident: Tab 2 aggregates into final report

**Tab 1 Example**:
```
URGENT: Need to rollback user-api deployment

Current: v2.1.0 (deployed 10 minutes ago, causing 500s)
Previous stable: v2.0.3
Location: /company/SRE/helm/charts/user-api/

Execute rollback immediately. Show commands before running.
```

**Tab 2 Example**:
```
Document incident in progress:

Service: user-api
Time started: 14:23 UTC
Symptom: 500 error rate 85%
Action: Rollback v2.1.0 → v2.0.3
Executed by: [name]

[Keep updating as actions taken in Tab 1]
```

---

## Setting Up Git Worktrees for Parallel Work

When you need to work on the same repository in multiple tabs:

### The Problem
```
One repo, multiple tasks:
- Update chart A
- Update chart B
- Both in same repo
- Can't have different branches checked out simultaneously
```

### The Solution: Git Worktrees
```bash
cd /company/SRE/helm/charts/

# Create worktrees
git worktree add ../charts-worktree-a main
git worktree add ../charts-worktree-b main

# Now you have:
# /company/SRE/helm/charts/          (original)
# /company/SRE/helm/charts-worktree-a (independent working directory)
# /company/SRE/helm/charts-worktree-b (independent working directory)
```

**Each tab**:
```
Tab 1:
cd /company/SRE/helm/charts-worktree-a/
# Start AI agent
"Update chart A..."

Tab 2:
cd /company/SRE/helm/charts-worktree-b/
# Start AI agent
"Update chart B..."
```

**AI can create worktrees for you**:
```
"Set up two git worktrees for this repository so I can work on chart A and chart B in parallel.

Create:
- Worktree A at ../charts-worktree-a for updating chart A
- Worktree B at ../charts-worktree-b for updating chart B
```

---

## Tab Management Strategies

### How Many Tabs?

**Sweet spot**: 2-5 active tabs

**Rules**:
- **1 tab**: Simple, single-focus tasks
- **2-3 tabs**: Most common workflows
- **4-5 tabs**: Complex multi-component work
- **6+ tabs**: Probably too many - consider if tasks can be serialized

**Warning signs**:
- Forgetting which tab is for what
- Constantly switching to find the right tab
- Duplicate work happening in multiple tabs

---

### Tab Lifecycle

**Opening**:
- Open when you identify independent work
- Name/color immediately
- Start with clear context

**During**:
- Keep focused on single concern
- Use handoffs if context fills
- Update status (what's done, what's left)

**Closing**:
- Close when task complete
- Extract important information first
- Reference tabs can stay open longer

**Example**:
```
Tab 1: Investigation (Blue)
- Open: Start of incident
- During: Gather findings
- Close: After root cause found, findings copied to implementation tab

Tab 2: Implementation (Green)
- Open: After investigation complete
- During: Build and test fix
- Close: After fix deployed and verified

Tab 3: Documentation (Yellow)
- Open: Early in process
- During: Accumulate notes throughout
- Close: After final documentation committed
```

---

## Coordination Techniques

### Manual Copy-Paste Aggregation

**When**: You need to combine outputs from multiple tabs

**How**:
```
Master tab:
I've completed work across multiple tabs. Here are the summaries:

[Tab 1 output]
[Tab 2 output]
[Tab 3 output]

Now create: [combined deliverable]
```

**Simple and effective**. No complex tooling needed.

---

### Shared Context Files

**When**: Multiple tabs need access to same information

**How**:
```
Create: /company/SRE/tmp/current-task-context.md

Contents:
- Task description
- Requirements
- Constraints
- Shared decisions

All tabs can read this file for context.
```

**Master tab updates it** as decisions are made:
```
"Update /tmp/current-task-context.md with our decision to use ClusterIP instead of LoadBalancer"
```

**Worker tabs reference it**:
```
"Check /tmp/current-task-context.md for any relevant constraints before proceeding"
```

---

### Sequential Handoffs

**When**: Work must flow from tab to tab

**Pattern**:
```
Tab 1: Investigation
  → Generates summary

Tab 2: Receives summary, implements fix
  → Generates change summary

Tab 3: Receives change summary, creates documentation
  → Generates final deliverables
```

Each tab adds to the story.

---

## Common Workflows

### Daily Standup Workflow
```
Tab 1 (Yellow): Work Item Search
  "Search my work items for anything in progress or blocked"
  Stays open for reference

Tab 2 (Green): Primary Work
  Based on highest priority item from Tab 1
  Main work happens here

Tab 3 (Green): Secondary Work
  Based on second priority item
  Switch to when blocked on Tab 2
```

---

### Code Review Workflow
```
Tab 1 (Blue): PR Review
  "Load PR #123 and analyze the changes"
  Stays open during review

Tab 2 (Blue): Related Code Search
  "Search codebase for similar patterns"
  Reference for review

Tab 3 (Green): Test Creation
  "Create tests for the changes in this PR"
  If you're adding tests during review
```

---

### Migration Workflow
```
Tab 1 (Blue): Source Analysis
  Location: Old system
  "Understand current implementation"

Tab 2 (Green): Target Implementation
  Location: New system
  "Implement equivalent in new system"
  References Tab 1 findings

Tab 3 (Green): Migration Script
  Location: /scripts/
  "Create migration script for data/config"

Tab 4 (Blue): Validation
  "Compare old vs new to verify equivalence"
```

---

## Troubleshooting Multi-Tab Workflows

### Problem: Lost Track of Tabs

**Symptoms**: Can't remember which tab is for what

**Solutions**:
- Use color coding consistently
- Keep count low (2-5 active)
- Close completed tabs promptly
- Use terminal's tab naming feature

**Terminal tab naming**:
```bash
# In bash
echo -e "\033]0;Investigation\007"

# Or have AI do it
"Set this terminal tab's title to 'Helm Updates - Service A'"
```

---

### Problem: Duplicating Work

**Symptoms**: Doing same thing in multiple tabs

**Solutions**:
- Start each tab with clear, specific purpose
- Review tab purposes before opening new one
- Consolidate if you catch duplication

---

### Problem: Can't Synthesize Results

**Symptoms**: Have outputs from multiple tabs but can't combine them

**Solutions**:
- Create master/coordination tab
- Use structured output format
- Have each worker tab summarize its results
- Copy-paste summaries into master tab

**Worker summary format**:
```
## Tab N: [Task Name]

### Completed
- Item 1
- Item 2

### Changed Files
- /path/to/file1
- /path/to/file2

### Key Decisions
- Decision 1: Rationale
- Decision 2: Rationale

### Remaining Work
- Next step 1
- Next step 2
```

---

### Problem: Context Overflow in Multiple Tabs

**Symptoms**: All tabs hitting 50% context simultaneously

**Solutions**:
- Generate handoffs for each tab
- Consider if tasks can be consolidated
- Close and summarize completed tabs
- Start fresh tabs with handoff prompts

---

## Decision Tree: When to Split into Multiple Tabs?

```
Are the tasks independent? (can work in parallel)
├─ YES → Separate tabs
└─ NO → Can they share context efficiently?
    ├─ YES → Same tab
    └─ NO → Would separate tabs reduce confusion?
        ├─ YES → Separate tabs
        └─ NO → Same tab
```

**Examples**:

**Independent tasks** → Separate:
- Update chart A, update chart B
- Investigate logs, implement fix (both start immediately)
- Search docs, write code

**Shared context, efficient** → Same tab:
- Investigate → analyze findings → propose solution
- Read file → understand → modify same file
- Sequential debugging steps

**Not independent, but separate reduces confusion** → Separate:
- Deep documentation analysis + implementation work
- Load 40-page doc in Tab 1 (reference), implement in Tab 2
- Investigation generating tons of output + clean implementation workspace

---

## Advanced: Tab Templates

Create reusable tab setups for common scenarios.

### Template: Service Update
```
Tab 1: Helm chart updates
  cd /company/SRE/helm/charts/[service]/
  Color: Green

Tab 2: Testing
  cd /company/SRE/
  Color: Blue

Tab 3: Documentation
  cd /company/SRE/notes/
  Color: Yellow
```

### Template: Incident Response
```
Tab 1: Investigation
  cd /company/SRE/
  Color: Blue

Tab 2: Execution
  cd /company/SRE/[affected-component]/
  Color: Red

Tab 3: Documentation
  cd /company/SRE/notes/incidents/
  Color: Yellow
  Start: Immediate (parallel)
```

### Template: Multi-Service Deployment
```
Tab 1-N: One per service
  cd /company/SRE/helm/charts/[service-name]/
  Color: Green

Tab N+1: Master coordination
  cd /company/SRE/
  Color: Green
  Purpose: Aggregate and create deployment plan
```

**Create a file**: `/company/SRE/notes/tab-templates.md` with your common patterns.

---

## Key Takeaways

1. **One tab, one job** - Keep focus tight
2. **Color code consistently** - Visual identification
3. **2-5 active tabs** - Sweet spot for most work
4. **Use git worktrees** - Parallel work on same repo
5. **Master + workers** - Coordination pattern for complex tasks
6. **Close completed tabs** - Reduce cognitive load
7. **Handoff when needed** - Each tab can handoff independently

---

## Practice Exercise

Pick a real task you're working on. Design your tab layout:

```
Task: [Describe your task]

Tab 1 ([Color]): [Purpose]
  Location: [Directory]
  Task: [Specific work]

Tab 2 ([Color]): [Purpose]
  Location: [Directory]
  Task: [Specific work]

[etc...]

Workflow:
1. [Step 1]
2. [Step 2]
...
```

**Try it out**. See what works and what doesn't.

---

**[← Back to Filesystem Organization](02-filesystem-organization.md)** | **[Local Data Stores →](04-local-data-stores.md)**
