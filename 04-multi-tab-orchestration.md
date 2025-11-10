# Module 4: Multi-Tab Orchestration

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

## The Orchestrator-Worker Pattern

The most effective multi-tab workflow combines rich natural language prompts with intelligent context management.

### How It Works

```
1. Orchestrator designs the work
   ↓
2. Start workers with detailed natural language prompts
   ↓
3. Workers execute autonomously (manage their own context)
   ↓
4. Workers complete and generate summaries
   ↓
5. Orchestrator aggregates summaries and coordinates next steps
```

### Key Principles

**Use natural language when starting workers:**
- Give complete context upfront
- Explain the "why" not just the "what"
- Describe how this work fits into the larger task
- Specify what you need back (summary, specific outputs)

**Let workers manage their own context:**
- No need for elaborate mid-work coordination
- Workers focus on their specific concern
- The orchestrator pattern handles dependencies

**Request summaries when work completes:**
- Ask workers to summarize what they accomplished
- Specify what information you need for coordination
- Feed these summaries back to the orchestrator

### Example: Starting a Worker

**Command-style prompt (minimal):**
```
Update service-a helm chart for new cluster
```

**Natural language prompt (effective):**
```
I'm working on migrating our services to a new Kubernetes cluster. This tab
is dedicated to updating the service-a helm chart as part of that migration.

Context about the migration:
- Moving from old-cluster to new-cluster
- New cluster has larger nodes (we can increase resource limits)
- New ingress domain: *.new.company.com
- This is happening in parallel with service-b and service-c updates

For this specific chart (service-a), I need you to:
1. Update cluster endpoint in values.yaml
2. Update ingress hostname for new domain
3. Increase memory limit from 2Gi to 4Gi (new nodes support this)
4. Verify the chart renders correctly

When you're done, I'll need a summary to take back to my orchestrator tab
that's coordinating all three service migrations. Include:
- What files you changed
- Any issues or dependencies you discovered
- Whether the chart is ready for deployment
```

**Why this works:**
- Worker has full context about the migration
- Understands how it fits with other work (parallel migrations)
- Knows what to deliver back (summary with specific info)
- Can work autonomously without mid-work check-ins

### Example: Collecting Summaries

When workers complete, ask each for a summary:

```
You've completed the helm chart updates for service-a. Before I move to
coordinating with the other workers, give me a summary I can take back to
my orchestrator tab:

1. What files did you modify?
2. What changes did you make?
3. Did you discover any dependencies or blockers?
4. Is this chart ready for deployment, or is there follow-up work needed?
```

Then bring these summaries to your orchestrator:

```
I'm coordinating migrations for three services. Here are the summaries from
each worker tab:

[Tab 1 - service-a summary]
[Tab 2 - service-b summary]
[Tab 3 - service-c summary]

Based on these results, help me:
1. Identify any cross-service dependencies
2. Determine the right deployment order
3. Flag any risks or blockers
4. Create a deployment checklist
```

### When NOT to Use This Pattern

**Single simple task:**
- One file to update, straightforward change
- Use a single tab, no need for orchestration

**Highly sequential work:**
- Each step depends on previous step's detailed output
- Better to work in one tab, build context progressively

**Exploratory investigation:**
- Don't know what you're looking for yet
- Single tab lets you explore and pivot easily

### The Power of This Approach

**For students/practitioners:**
- Natural language prompts are easier to write than command-style
- No need to track complex handoffs mid-work
- Orchestrator maintains the big picture
- Workers stay focused on their specific concerns

**For the AI:**
- Clear scope per worker (better focus)
- Orchestrator can reason about the whole system
- Summaries provide exactly the context needed for coordination
- No context pollution from unrelated work

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
3. Start each tab with rich natural language prompt
4. Workers execute in parallel (no blocking)
5. Collect summaries when complete

**Why it works**: Each chart update is independent. No need to wait for one to finish before starting another.

**Example initial prompt for Tab 1:**
```
I'm working on a multi-service migration to a new Kubernetes cluster. This tab
is dedicated to updating the service-a helm chart.

Context:
- This is one of three services being migrated (service-a, service-b, service-c)
- Each service has its own tab working in parallel via git worktrees
- New cluster: prod-cluster-v2 (larger nodes, new ingress domain)
- Goal: All three charts ready for coordinated deployment

For service-a specifically:
- Update cluster endpoint in values.yaml
- Update ingress hostname to *.v2.company.com
- Increase memory limit from 2Gi to 4Gi (new nodes support this)
- Verify chart renders successfully

Watch for:
- Shared ConfigMaps or dependencies that other services might need
- Settings that should be consistent across all three services

When complete, I'll need a summary including:
- Files modified
- Any shared dependencies discovered
- Whether chart is deployment-ready
```

**After all three tabs complete**, collect summaries and bring to orchestrator for coordination.

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
2. Tab 1: Generate investigation summary
3. Tab 2: Start with summary, implement fix
4. Tab 2: Generate implementation summary
5. Tab 3: Start with both summaries, create documentation

**Why it works**: Separation of concerns. Investigation context doesn't clutter implementation. Each tab focuses on its specific task.

**Step 1: Request summary from investigation tab**
```
You've completed the investigation into the crashloop issue. Before I hand
this off to an implementation tab, give me a comprehensive summary:

1. What was the root cause?
2. What evidence led to this conclusion?
3. What needs to be fixed? (immediate mitigation vs long-term solution)
4. Which files/components are involved?
5. Any risks or considerations for the fix?
```

**Step 2: Start implementation tab with that summary**
```
I'm implementing a fix for a production issue. Another tab completed the
investigation. Here's what they found:

[Paste investigation summary]

Based on this investigation, implement the immediate mitigation:
- Reduce worker concurrency from 10 to 5 in values.yaml
- Verify chart renders correctly
- Note what still needs to be done for the long-term fix

The investigation tab is still open if you need to reference it.
```

**Step 3: Start documentation tab with both summaries**
```
I need to document a production issue we just resolved. Here's what happened:

Investigation findings:
[Paste investigation summary]

Fix implemented:
[Paste implementation summary]

Create:
1. Runbook entry for this issue
2. Incident log update
3. TODO for long-term fix (connection pool management)
```

**Why this works**:
- Each tab gets exactly the context it needs
- No elaborate mid-work handoffs required
- Summaries are reusable (documentation tab uses both)
- Investigation and implementation contexts stay separate

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
1. Tabs 1-3: Work independently with rich initial prompts
2. Tab 4: Provides reference context (stays open)
3. Each worker generates summary when complete
4. Collect summaries and bring to master tab
5. Master creates final deliverables

**Step 1: Request summary from each worker when complete**

Ask Tab 1 (Helm):
```
You've completed the helm chart updates for this migration. Give me a summary
for the master coordination tab:

1. What charts did you update?
2. What specific changes were made?
3. Any shared dependencies or blockers discovered?
4. Is everything ready for deployment?
```

Similarly for Tabs 2 (Terraform) and 3 (Testing).

**Step 2: Aggregate summaries in master tab (Tab 5)**
```
I'm coordinating a cluster migration across multiple worker tabs. Each has
completed its work and provided a summary. Help me synthesize these into
final deliverables.

**Tab 1 Summary - Helm updates:**
[Paste summary from Tab 1]

**Tab 2 Summary - Terraform changes:**
[Paste summary from Tab 2]

**Tab 3 Summary - Testing results:**
[Paste summary from Tab 3]

**Tab 4 Reference - Work items:**
[Paste relevant findings from Tab 4]

Based on these summaries:
1. Flag any dependencies or risks across the work
2. Determine the right deployment sequence
3. Create a deployment checklist with proper ordering
4. Draft comprehensive documentation
5. Generate PR descriptions for each component

I'm uncertain about:
- Whether to deploy all at once or service-by-service
- How to handle the ConfigMap dependency Tab 1 discovered
```

**Why this works**:
- Workers provide structured summaries (you asked for specific info)
- Master gets clean, focused context from each worker
- You use natural language to ask for strategic synthesis
- Expresses uncertainty so AI provides guidance, not just execution

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

**Tab 1 Example** (Command-style):
```
URGENT: Need to rollback user-api deployment

Current: v2.1.0 (deployed 10 minutes ago, causing 500s)
Previous stable: v2.0.3
Location: /company/SRE/helm/charts/user-api/

Execute rollback immediately. Show commands before running.
```

**Tab 1 Example** (Natural language - better for incidents):
```
URGENT INCIDENT - I need help executing a rollback quickly but safely.

**Situation:**
user-api v2.1.0 deployed 10 minutes ago (14:13 UTC) is returning 500 errors at
85% rate. Users are affected. I need to rollback to v2.0.3 which was stable.

**What I need:**
Generate the helm rollback commands for me to review and execute. Include:
1. Commands to verify current state
2. The actual rollback command
3. How to verify rollback succeeded
4. How to check error rate is dropping

**What I'm unsure about:**
- Whether there are database migrations in v2.1.0 that might break if we rollback
- If we need to coordinate with the dev team first or just roll back

We're in an active incident - I need to move fast but not break things worse.
Show me the commands and any warnings, I'll make the call.
```

**Tab 2 Example** (Natural language documentation):
```
I'm documenting an incident that's happening right now in Tab 1 (execution tab).
I need you to help me maintain a structured incident log as I feed you updates.

**Start the incident log with what I know:**
- Service: user-api
- Time started: 14:23 UTC
- Symptom: 500 error rate jumped from 2% to 85%
- Suspected cause: Recent deployment of v2.1.0 (10 minutes ago)
- Action being taken: Rollback to v2.0.3 in progress (Tab 1)
- Incident commander: [my name]

I'll keep you updated with actions as they happen. After each update, show me
the current state of the incident log so I can verify it's accurate.

Also flag anything that seems important for the post-mortem - things we should
have done differently or questions we need to answer later.
```

**Why natural language helps in emergencies**:
- Reduces cognitive load (AI handles structure)
- Expresses uncertainty without shame (database migrations?)
- Gets AI to think about risks (warnings)
- Parallel documentation captures real-time timeline
- AI can flag process improvements even during the incident

---

### Pattern 6: Orchestrator Tab for Prompt Generation

**Scenario**: Complex task that needs to be broken down into multiple parallel subtasks

**Use case**: Instead of manually designing each tab's prompt, use one tab to analyze the task and generate optimized prompts for other tabs.

**Tab Structure**:
```
Tab 1 (Blue): Orchestrator/Planner
  Location: /company/SRE/
  Task: Analyze overall task and generate prompts for worker tabs
  Stays open: Yes - for coordination

Tabs 2-N (Green): Worker tabs
  Created based on orchestrator's recommendations
  Each receives custom-generated prompt from Tab 1
```

**Workflow**:

**Step 1: Task Analysis (Orchestrator Tab)**
```
I need to perform a blue-green cluster swap with infrastructure upgrades.

Analyze this task and break it down into independent subtasks that can be worked on in parallel.

For each subtask:
1. Identify what needs to be done
2. Determine the working directory
3. List relevant files/contexts
4. Generate a complete, context-rich prompt I can paste into a new tab

Generate 3-5 prompts for me to open in new tabs.
```

**Step 2: Orchestrator Generates Prompts**
```
Based on your task, here are the subtasks:

=== TAB 2: Helm Chart A Updates ===
Working directory: /company/SRE/helm/charts/
Setup: Create git worktree

Prompt to paste:
---
Set up git worktree for service-a helm chart updates:
git worktree add ../charts-worktree-a

Task: Update service-a chart for new cluster
Changes needed:
- Update cluster endpoints in values.yaml
- Modify ingress for new domain
- Update resource limits (new cluster has better nodes)

Files to modify:
- values.yaml
- templates/ingress.yaml

Color: Green
---

=== TAB 3: Helm Chart B Updates ===
[Similar detailed prompt]

=== TAB 4: Sync Script Updates ===
[Detailed prompt for script changes]

=== TAB 5: Work Item Search ===
[Prompt for finding related work items]
```

**Step 3: Create Worker Tabs**
- Open new tabs
- Paste generated prompts
- Color code as recommended
- Begin parallel work

**Step 4: Collect Summaries from Workers**
After each worker completes, ask for a summary:

Tab 2 (Helm Charts):
```
You've finished the helm chart updates. Give me a summary to bring back
to the orchestrator tab:

1. What charts were updated?
2. What changes were made?
3. Any dependencies or issues discovered?
4. Ready for deployment?
```

Similarly for Tabs 3 (Terraform), 4 (Sync Script), etc.

**Step 5: Return to Orchestrator with Summaries**
```
The worker tabs have completed. Here are their summaries:

**Tab 2 - Helm Chart Updates:**
[Paste summary]

**Tab 3 - Terraform Infrastructure:**
[Paste summary]

**Tab 4 - Sync Script:**
[Paste summary]

Based on these results, help me:
1. Create deployment sequence accounting for dependencies
2. Identify risks or gaps in our approach
3. Draft documentation explaining the migration strategy
4. Generate PR descriptions for each component

I'm uncertain about:
- How to handle the ConfigMap dependency (separate PR or fold in?)
- Whether we need additional coordination steps
```

**Why this works**:
- Orchestrator generates rich prompts (Step 1-2)
- Workers execute with clear context (Step 3)
- Summaries bring focused results back (Step 4-5)
- Orchestrator synthesizes without context pollution

**Why This Pattern Works**:
- **Reduces cognitive load**: You don't have to design each prompt manually
- **Consistency**: Orchestrator ensures all worker tabs have proper context
- **Optimization**: Orchestrator can identify the best way to split the work
- **Context preservation**: Orchestrator maintains the big picture while workers focus on details

**Example: Real-World Usage**
```
Task given to orchestrator:
"I need to migrate user-api, billing-api, and auth-api services to the new Kubernetes cluster. Each needs helm chart updates, terraform changes, and testing."

Orchestrator generates 9 prompts:
- 3 for helm updates (one per service)
- 3 for terraform changes (one per service)
- 3 for testing (one per service)

Plus 1 coordination prompt for the master tab.

You paste these into 10 tabs and work in parallel.
```

**Advanced: Iterative Refinement**
```
If worker tabs hit issues, return to orchestrator:

"Tab 3 (billing-api helm) found an issue: chart depends on a shared ConfigMap that doesn't exist in new cluster.

How should I handle this? Update the orchestration plan."

Orchestrator:
"Good catch. Here's the updated plan:
1. Tab 3 should pause
2. Open new Tab 10: Create shared ConfigMap
3. Here's the prompt for Tab 10: [detailed prompt]
4. After Tab 10 completes, Tab 3 can proceed"
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

### Shared Context Files (Usually Not Needed)

**Note**: With the orchestrator-worker pattern, you usually don't need shared context files. The orchestrator provides context when starting workers, and workers report back summaries.

**However**, if you have long-running parallel workers that need to coordinate on emerging decisions:

```
Create: /tmp/current-task-context.md

Update it when decisions are made:
"We decided to use ClusterIP for internal services due to cost concerns.
Update /tmp/current-task-context.md to document this so other workers
can follow the same pattern."

Workers can reference it:
"Check /tmp/current-task-context.md for any design decisions I should
follow for this service's configuration."
```

**Better alternative**: Include such decisions in the orchestrator's initial prompts, or collect them during summary phase.

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

**Symptoms**: Multiple tabs have high context usage simultaneously

**Solutions**:
- Generate handoffs for each tab that needs it
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

## Session Persistence and Resume

One of the most powerful features of modern AI coding assistants like Codex and Claude Code: **session persistence**.

### The Problem: Human Context Loss

**Scenario**: You're working on a complex migration. It's 5 PM, you need to leave.

**Traditional approach**:
- Close all tabs
- Tomorrow: "What was I doing? Where did I leave off?"
- Spend 20 minutes getting back into context
- Lose momentum and mental state

**Better approach**: Session persistence

---

### What is Session Resume?

Both Codex and Claude Code can save and resume sessions:
- **Full conversation history preserved**
- **Working directory remembered**
- **File context maintained**
- **Mental model retained**

**Think of it as**: Hibernating your work, not closing it.

---

### When to Use Resume

✅ **End of day**
```
Tab 1: Investigation in progress - 30 messages deep
Tab 2: Implementation - partially complete
Tab 3: Reference docs loaded

Don't close. Let them persist.
Tomorrow: Resume all three tabs right where you left off.
```

✅ **Context switching**
```
Working on migration project.
Urgent production issue interrupts.

Pause migration tabs (don't close).
Open new tabs for incident.
After incident: Resume migration tabs with full context intact.
```

✅ **Long-running projects**
```
Week-long migration project.
Multiple tabs with accumulated knowledge.

Each day: Resume tabs from yesterday.
No rebuilding context.
Continuous workflow.
```

✅ **Complex investigations**
```
Deep dive into codebase structure.
Loaded multiple files, explored patterns, built understanding.

Resume tomorrow: All that context is still there.
No need to re-explore.
```

---

### The Real Benefit: Human Context Recovery

**The AI isn't the only one lacking context** - humans forget too.

**Example workflow**:

**Friday 5 PM**:
```
Tab 1 (Investigation): 50 messages exploring helm chart dependencies
Tab 2 (Implementation): 30 messages updating charts
Tab 3 (Reference): Architecture docs loaded

You: "I need to leave. We'll continue Monday."
→ Tabs persist
```

**Monday 9 AM**:
```
You: "What was I working on again?"

Resume Tab 1:
- Scroll up through conversation history
- "Oh right, we found that Chart A depends on ConfigMap X"
- "And we determined Chart B needs updating first"
- Full context restored

Resume Tab 2:
- "We were updating the values.yaml"
- "We had decided to use 8Gi memory based on metrics"
- Continue exactly where you left off
```

**The AI remembers what you've forgotten.**

---

### Practical Patterns

#### Pattern 1: Daily Resume

```
End of day:
- Leave tabs open
- Notes in tab names (if using terminal tab naming)
- Color coding already in place

Next morning:
- Resume all tabs
- Quick scroll through recent messages to remember context
- Continue work immediately
```

#### Pattern 2: Multi-Project Management

```
Project A tabs (migration):
- Tab 1-3: Migration work
- Leave open/resumed when not active

Project B tabs (optimization):
- Tab 4-6: Optimization work
- Leave open/resumed when not active

Switch between projects:
- Resume relevant tabs
- Full context for each project maintained
```

#### Pattern 3: Investigation Preservation

```
Deep investigation:
- Tab explores complex codebase
- Builds understanding over 100+ messages
- Loads many files for reference

Without resume:
- Would need to reload everything
- Lose accumulated insights
- Rebuild mental model

With resume:
- Return to investigation anytime
- All context preserved
- Reference what AI discovered last week
```

---

### Best Practices

**1. Name your tabs/sessions meaningfully**
```
Bad: "Tab 1", "Session 2"
Good: "Migration-HelmCharts", "Investigation-AuthFlow"
```

**2. Add a summary comment before pausing**
```
Command-style:
"Summarize where we are and what's next for when I resume this tomorrow."

Natural language (more effective):
"I need to stop for the day, but I'll be resuming this work tomorrow morning.
Can you create a comprehensive checkpoint summary that will help me (and you)
get back into context quickly?

Include:
1. What we've completed so far
2. What we're in the middle of (current state)
3. What's left to do (next steps)
4. Any decisions we made that I might forget overnight
5. Any blockers or questions that came up

I want tomorrow-me to be able to read this summary and pick up exactly where
we left off without having to scroll through our entire conversation.

Also, if there's anything I should think about or research overnight (like that
database migration question we had), flag it."

AI provides comprehensive checkpoint summary.
First thing you see when resuming.
```

**When you resume** (natural language):
```
Command-style resume:
"Continue from yesterday"

Natural language resume:
"I'm resuming work on the cluster migration we were working on yesterday.
Before we dive back in, can you:

1. Give me a quick refresher on where we left off
2. Remind me of any important decisions we made
3. Let me know what our next step was going to be

I've had a night's sleep and some context has faded - help me get back up to
speed efficiently."
```

**3. Use resume for reference tabs**
```
Tab with 40-page architecture doc loaded:
Don't close and reload daily.
Keep resumed for the entire week/project.
```

**4. Resume trumps handoff for same session**
```
Same tab, continuing work tomorrow:
→ Use Resume (preserves everything)

Different tab, transferring context:
→ Use Handoff (fresh start with summary)
```

---

### When NOT to Resume

❌ **Task completely finished**
- Close and free up mental space

❌ **Context is stale**
- Week-old investigation, information changed
- Better to start fresh

❌ **You need a clean slate**
- Previous approach didn't work
- Want to rethink from scratch

---

### Resume vs. Handoff: Decision Tree

```
Need to continue this exact conversation?
├─ Yes → Resume the session
└─ No → Need to transfer context to new session/tab?
    ├─ Yes → Use Handoff
    └─ No → Start fresh
```

**Examples**:

**Resume**:
- "Continue investigating this issue tomorrow"
- "Come back to this implementation next week"
- "Reference this analysis again later"

**Handoff**:
- "Move to new tab to implement findings"
- "Share context with teammate"
- "Context too full, need fresh session"

**Fresh Start**:
- "Previous approach failed, trying new direction"
- "Task complete, starting different work"

---

### Combining Resume with Other Patterns

**Resume + Orchestrator**:
```
Orchestrator tab generates prompts for 5 worker tabs.
All 6 tabs remain open/resumed throughout the project.
Orchestrator tracks overall state.
Workers handle specific subtasks.
```

**Resume + Reference Tabs**:
```
Yellow reference tab with docs loaded.
Keep resumed for entire project (days/weeks).
Query it whenever needed.
Never reload the same docs.
```

**Resume + Investigation**:
```
Blue investigation tab.
Resume daily as you explore.
Builds accumulated knowledge.
Review history to see how understanding evolved.
```

---

### Advanced: Session Libraries

**Create a "shelf" of resumed sessions**:
```
Active Projects:
- Migration project (3 tabs resumed)
- Optimization work (2 tabs resumed)
- Documentation update (1 tab resumed)

Reference Sessions:
- Architecture analysis (1 tab, resumed monthly)
- Incident patterns (1 tab, updated weekly)

On Ice:
- Future projects (tabs saved, not actively resumed)
```

**Jump between projects**: Resume relevant tabs, pause others.

---

### Key Insight

**You're not just preserving AI context - you're preserving YOUR context.**

The conversation history in a resumed session is documentation of:
- What you discovered
- Decisions you made
- Why you made them
- What you tried
- What worked and what didn't

**Resume isn't just a feature - it's a knowledge management tool.**

---

## Key Takeaways

1. **One tab, one job** - Keep focus tight
2. **Use natural language prompts** - Give workers rich context when starting
3. **Request summaries, not mid-work handoffs** - Let workers manage their own context
4. **Orchestrator pattern** - Start workers with detailed prompts, collect summaries when done
5. **Color code consistently** - Visual identification (Green/Blue/Yellow/Red)
6. **2-5 active tabs** - Sweet spot for most work
7. **Use git worktrees** - Parallel work on same repo
8. **Resume sessions** - Preserve context across days/weeks, for both AI and human
9. **Close completed tabs** - Reduce cognitive load

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

**[← Back to MCP Servers](03-mcp-servers.md)** | **[Integration Patterns →](05-integration-patterns.md)**
