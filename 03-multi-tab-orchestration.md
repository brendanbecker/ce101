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

**Step 4: Return to Orchestrator for Coordination**
After workers complete, return to Tab 1:
```
Worker tabs have completed:

Tab 2 results: [paste summary]
Tab 3 results: [paste summary]
Tab 4 results: [paste summary]

Now:
1. Identify dependencies between these changes
2. Create deployment plan
3. Generate wiki documentation
4. Create PR descriptions
```

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
Before ending session:
"Summarize where we are and what's next for when I resume this tomorrow."

AI provides checkpoint summary.
First thing you see when resuming.
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
2. **Color code consistently** - Visual identification
3. **2-5 active tabs** - Sweet spot for most work
4. **Use git worktrees** - Parallel work on same repo
5. **Master + workers** - Coordination pattern for complex tasks
6. **Orchestrator for complex tasks** - Let one tab generate prompts for others
7. **Resume sessions** - Preserve context across days/weeks, for both AI and human
8. **Close completed tabs** - Reduce cognitive load
9. **Handoff when needed** - Each tab can handoff independently

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
