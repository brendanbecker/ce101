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

### Pattern 5: Emergency Response

**Scenario**: Production incident requiring immediate action

**Tab Structure**:
```
Tab 1 (Red): Execution - Execute rollback/fix NOW
Tab 2 (Yellow): Documentation - Real-time incident log
Tab 3 (Blue): Investigation - Root cause analysis (starts after mitigation)
```

**Example execution prompt** (Tab 1):
```
URGENT - user-api v2.1.0 deployed 10 mins ago is returning 500s at 85% rate.
Need to rollback to v2.0.3 (last stable).

Generate rollback commands with:
- Current state verification
- The rollback command
- Success verification
- Error rate check

I'm unsure if there are DB migrations that might break. Flag any warnings.
Need to move fast but safely.
```

**Why this works**: Execution tab focuses on speed, documentation tab captures timeline for post-mortem, investigation happens in parallel after mitigation starts

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

## Practical Guidance

### How Many Tabs?

**Sweet spot**: 2-5 active tabs

- **1 tab**: Simple, single-focus tasks
- **2-3 tabs**: Most common workflows
- **4-5 tabs**: Complex multi-component work
- **6+ tabs**: Too many - consider serializing or consolidating

**Warning signs**: Forgetting which tab is for what, constantly searching for the right tab, duplicate work

### Coordination Techniques

**Copy-paste summaries**: Simple and effective. Collect worker summaries and paste into orchestrator/master tab.

**Shared context files**: Usually not needed with orchestrator pattern. If long-running workers need emerging decisions, create `/tmp/context.md` that all can reference. Better: include decisions in orchestrator's initial prompts.

---

## Session Persistence and Resume

Modern AI coding assistants can save and resume sessions - preserving conversation history, working directory, and context across days or weeks.

### When to Use Resume

**End of day**: Leave tabs open instead of closing them. Resume tomorrow where you left off.

**Context switching**: Pause current project tabs when interrupted. Resume later with full context intact.

**Long-running projects**: Keep tabs open for the entire week/project. No rebuilding context daily.

**Reference tabs**: Yellow tabs with docs loaded - keep resumed for days/weeks rather than reloading.

### Best Practices

**1. Request checkpoint summary before pausing**
```
"I'm stopping for the day. Create a checkpoint summary:
- What we've completed
- Current state (what we're in the middle of)
- Next steps
- Key decisions I might forget

This helps me resume quickly tomorrow."
```

**2. Request refresher when resuming**
```
"Resuming the cluster migration from yesterday. Quick refresher:
- Where we left off
- Important decisions we made
- What the next step was"
```

**3. Use resume for same session, summaries for new sessions**
- Same tab tomorrow → Resume
- New tab/different session → Request summary and handoff

### When NOT to Resume

- Task completely finished
- Context is stale (week-old work, things have changed)
- Need a clean slate (previous approach didn't work)

### Key Insight

Session history preserves YOUR context as much as the AI's - it's documentation of what you discovered, decisions you made, and why. The AI remembers what you've forgotten.

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

**[← Back to MCP Servers](03-mcp-servers.md)** | **[Patterns and Anti-Patterns →](05-patterns-and-antipatterns.md)**
