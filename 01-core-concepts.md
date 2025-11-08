# Module 1: Core Concepts

## The Mental Model Shift

### The Old Way
```
"Write me a script to check disk space"
```

You get a generic script that may or may not fit your environment.

### The New Way
```
I need to monitor disk usage across our Kubernetes cluster.

Relevant files: 
- /monitoring/prometheus-rules.yaml (current alerts)
- /scripts/disk-check.sh (existing script we're replacing)

Requirements:
- Alert at 80% usage
- Integrate with our Slack webhook
- Output JSON for Datadog

Show me the existing script first, then propose improvements.
```

You get a script tailored to your actual infrastructure.

**The difference**: You're giving the AI the context it needs to do the job *right*, not just *done*.

---

## The Four Context Strategies

Context Engineering uses four fundamental strategies for managing information:

### 1. SELECT - Point to the Right Information

**What it is**: Direct the AI to relevant files, directories, or data sources rather than expecting it to guess.

**When to use**:
- Starting a new task
- AI needs domain-specific information
- Working with large codebases

**Examples**:
```bash
# Explicit file selection
"Check /terraform/azure-infrastructure/main.tf for the AKS cluster config"

# Directory-based selection  
"Search the /runbooks directory for any documentation about database failovers"

# Pattern-based selection
"Find all helm charts that use the nginx-ingress controller"
```

**SRE Use Cases**:
- Pointing to terraform state files
- Directing to specific runbooks
- Selecting relevant log files
- Querying MCP servers for live data

---

### 2. WRITE - Persist Information Externally

**What it is**: Save context outside the AI's session so it's available later or across multiple sessions.

**When to use**:
- Need to remember decisions across sessions
- Building reusable knowledge
- Sharing context across multiple agents

**Examples**:
```bash
# Handoff prompts
"Give me a handoff prompt I can use to continue this work in a new session"

# Knowledge bases
Create runbook at /notes/runbooks/new-procedure.md

# Local inventories
Build Azure resource inventory at /notes/inventory/azure-resources.json
```

**SRE Use Cases**:
- Creating handoff prompts when context fills up
- Building searchable incident histories
- Maintaining resource inventories
- Documenting decisions and solutions

---

### 3. ISOLATE - One Agent, One Job

**What it is**: Use separate agents (terminal tabs/sessions) for separate concerns instead of mixing multiple tasks in one context.

**When to use**:
- Complex multi-part tasks
- Independent work streams
- Need to maintain focus on specific aspects

**Examples**:
```bash
# Instead of one tab doing everything:
Tab 1: Update helm chart A
Tab 2: Update helm chart B  
Tab 3: Update sync script
Tab 4: Search work items (reference)
Tab 5: Aggregate and create documentation
```

**SRE Use Cases**:
- Parallel infrastructure updates
- Separating investigation from remediation
- Document analysis in one tab, execution in another
- Different agents for different services

**Why it works**: Each agent maintains focused context without interference from unrelated information.

---

### 4. COMPRESS - Use Only When Forced

**What it is**: Reduce context size through summarization or truncation.

**When to use**: Rarely. Modern context windows are large enough that isolation is usually better.

**When you might need it**:
- Context window approaching limits (50%+)
- Handoff prompts between sessions
- Very large documents that must be in one session

**Our approach**: 
- **Don't preemptively compress**. Tokens are cheap, clarity is expensive.
- **Use handoff prompts** when crossing 50% context utilization
- **Prefer isolation** over compression - split into multiple agents instead

**Example of good compression**:
```
Agent generates its own handoff:
"We've updated the helm chart to version 4.8, modified resource limits, 
and tested rendering. Remaining: update production values and document changes."

vs. keeping the entire 30-message conversation history.
```

---

## The Core Principle

**Make questions easy to answer.**

When you ask a human colleague for help, you provide:
- What you're trying to do
- What you've already tried  
- Relevant context about your environment
- What success looks like

Do the same for AI assistants. They need the same information to help effectively.

---

## Context Engineering vs. Prompt Engineering

| Prompt Engineering | Context Engineering |
|-------------------|---------------------|
| Focus on wording | Focus on information architecture |
| Single clever prompt | System of interconnected agents |
| Static input | Dynamic context gathering |
| "What should I say?" | "What does the AI need to know?" |

Context Engineering is the evolution of prompt engineering for production workflows.

---

## Key Principles

### 1. Specificity Over Cleverness
Bad: "Fix the config"  
Good: "Update /terraform/main.tf to change the VM size from Standard_D2s_v3 to Standard_D4s_v3"

### 2. Context Over Brevity
Don't: Minimal prompts to "save tokens"  
Do: Rich context that enables accurate work

### 3. Tools Over Memory
Don't: Expect the AI to remember your infrastructure  
Do: Give it access to files, APIs, and data stores

### 4. Architecture Over Prompts
Don't: Craft the perfect one-shot prompt  
Do: Design a system of agents with clear responsibilities

---

## Exercise: Transform Your Prompt

Take a task you did recently. Write two versions:

**Version 1 - Basic Prompt**:
```
[What you might naturally type]
```

**Version 2 - Context-Engineered**:
```
[Include: task description, relevant files, requirements, success criteria]
```

### Example

**Version 1**:
```
Update the alert threshold
```

**Version 2**:
```
I need to update our disk space alert threshold from 80% to 85%.

Current alert: /monitoring/prometheus/alerts/disk-space.yaml
Context: We had 47 false positives last month (logged in incidents/2024-11.md)

Please:
1. Show me the current alert rule
2. Update the threshold to 85%
3. Verify syntax is valid
4. Suggest any related alerts that should also be updated
```

---

## Decision Framework

When starting work with an AI assistant, ask yourself:

1. **SELECT**: What files/data does it need to see?
2. **WRITE**: What should be saved for later?
3. **ISOLATE**: Should this be a separate agent/tab?
4. **COMPRESS**: Am I approaching context limits?

In practice, you'll mostly use SELECT and ISOLATE. WRITE comes naturally as you work. COMPRESS is rarely needed.

---

## Common Mistakes

❌ **Vague requests**: "Check the logs"  
✅ **Specific requests**: "Check /var/log/app.log for errors between 14:00-15:00 UTC"

❌ **Assuming knowledge**: "Fix the production issue"  
✅ **Providing context**: "Production app is returning 500s. Error logs in /tmp/errors.log. Last successful deploy was 2 hours ago."

❌ **Mixing concerns**: One tab doing investigation + fixes + documentation  
✅ **Separating concerns**: Tab 1 investigates, Tab 2 implements fix, Tab 3 documents

---

## Next Steps

Now that you understand the core strategies, learn how to apply them:

- **[Filesystem Organization →](02-filesystem-organization.md)** - Structure your workspace for optimal context
- **[Multi-Tab Orchestration →](03-multi-tab-orchestration.md)** - Manage complex tasks across multiple agents

---

**Questions?** Bring them to the workshop or add to the discussion thread.
