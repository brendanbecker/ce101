# Module 5: Multi-Tab Orchestration

Managing multiple AI agents working on different aspects of complex tasks simultaneously.

---

## The Core Concept

**One tab, one job.**

Instead of cramming everything into a single context window, use multiple terminal tabs with isolated AI sessions, each focused on a specific concern.

Think of it like having a team of specialists rather than one generalist trying to do everything.

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

### Advanced: Orchestrator Generates Prompts

For complex tasks, use the orchestrator to analyze your work and generate optimized prompts for worker tabs.

**Example:**
```
I need to migrate user-api, billing-api, and auth-api to the new cluster.
Each needs helm updates, terraform changes, and testing.

Analyze this task and break it down into subtasks that can be worked in parallel.

For each subtask, generate a complete prompt I can paste into a new tab, including:
- Working directory
- Context about the overall migration
- Specific changes needed
- What summary to provide back
```

The orchestrator generates 9-10 detailed prompts (one per service + component). You paste these into new tabs and work in parallel.

**Why this works:**
- Reduces cognitive load (orchestrator designs the prompts)
- Ensures consistency across workers
- Orchestrator identifies optimal work breakdown

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

**Why it works**: Each chart update is independent. No need to wait for one to finish before starting another. Use git worktrees to work on same repo in parallel.

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

**Why it works**: Investigation context stays separate from implementation. Each tab gets exactly the context it needs via summaries.

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

### Pattern 4: Emergency Response

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

Request a checkpoint summary before pausing: "Create a checkpoint summary: what we've completed, current state, next steps, key decisions."

When resuming, ask for a quick refresher on where you left off and important decisions made.

### When NOT to Resume

- Task completely finished
- Context is stale (week-old work, things have changed)
- Need a clean slate (previous approach didn't work)

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

**[← Back to AI Skills](04-ai-skills.md)** | **[Patterns and Anti-Patterns →](06-patterns-and-antipatterns.md)**
