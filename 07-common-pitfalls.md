# Module 7: Common Pitfalls

Learn from these mistakes so you don't have to make them yourself.

---

## Pitfall 1: The Everything Tab

### What It Looks Like

One terminal tab trying to handle:
- Investigation of production issue
- Implementing the fix
- Testing the fix
- Updating documentation  
- Creating work item updates
- Writing post-mortem

### Why It Fails

- Context becomes cluttered with mixed concerns
- Hard to track what's been done vs. what's remaining
- When you need to handoff, the summary is overwhelming
- Can't parallelize independent work
- Easy to lose focus

### The Fix

**Use isolation strategy**: One tab per concern

```
Tab 1 (Blue):  Investigation - stays focused on root cause
Tab 2 (Green): Implementation - isolated fix work
Tab 3 (Green): Documentation - aggregates from tabs 1-2
```

### Real Example

**Bad**: "Help me investigate this issue and also update the helm chart and write a runbook and update the work item"

**Good**: 
- Tab 1: "Investigate crashloop in production"
- Tab 2: "Update helm chart based on findings from investigation"
- Tab 3: "Create runbook from investigation and fix"
- Tab 4: "Update work item with details from all above"

---

## Pitfall 2: Vague File References

### What It Looks Like

```
"Check the config file"
"Update the deployment"
"Look at the logs"
"Fix the terraform"
```

### Why It Fails

- Agent doesn't know which file you mean
- May find wrong file or guess incorrectly
- Wastes time clarifying
- Results may be for wrong component

### The Fix

**Always use absolute paths**

```
"Check /company/SRE/terraform/azure-infrastructure/main.tf"
"Update /company/SRE/helm/charts/my-service/values/production.yaml"
"Look at /var/log/my-service/error.log"
```

### Pro Tip

Use tab completion in terminal, copy the full path, paste into prompt.

---

## Pitfall 3: Assuming Prior Knowledge

### What It Looks Like

```
"Fix the production issue"
"Update that thing we talked about yesterday"
"Make it work like the other one"
```

### Why It Fails

- AI has no memory between sessions
- Can't reference "yesterday" or "that thing"
- No context about your environment
- Results will be generic or wrong

### The Fix

**Provide complete context every time**

```
The user-api service in production is returning 500 errors.

Context:
- Started 30 minutes ago
- Error logs at /tmp/user-api-errors.log
- Last deploy was 2 hours ago (v2.1.0)
- Service config: /company/SRE/helm/charts/user-api/

Investigate and propose fix.
```

---

## Pitfall 4: Stale Data Stores

### What It Looks Like

You built an Azure resource inventory 3 months ago. You're still using it to make decisions today.

### Why It Fails

- Infrastructure changes constantly
- Agent bases recommendations on outdated info
- Drift detection is meaningless if baseline is wrong
- Can lead to wrong decisions about resource state

### The Fix

**Maintain your data stores**

```
# Include update timestamp
/notes/inventory/
├── azure-resources.json
└── last-updated.txt  # "Last updated: 2024-11-07"

# Schedule updates
- After major infrastructure changes
- Weekly for active projects
- Monthly minimum for reference data

# Verify critical info
When decisions matter, double-check against live sources
```

---

## Pitfall 5: No Handoff Strategy

### What It Looks Like

You work in a session until it crashes or becomes unusable. When you start fresh, you lose all context and have to re-explain everything.

### Why It Fails

- Context window eventually fills
- No way to continue work seamlessly
- Knowledge is lost
- Have to rebuild context from scratch

### The Fix

**Use handoff prompts when context gets high**

```
# Monitor context usage
Most tools show: "Context: 47,000 / 100,000 tokens"

# When it's climbing and feeling cluttered, generate handoff
"Give me a handoff prompt I can copy to continue this work"

# Start new session with that prompt
→ Seamless continuation with full context
```

**Guideline**: Many people find 40-60% a good range to start thinking about handoffs, but it's not a hard rule. Trust your judgment.

---

## Pitfall 6: Starting in Wrong Directory

### What It Looks Like

```bash
cd /
# Start Codex here

"Update the helm chart"
```

Agent now has to search your entire filesystem to find helm charts.

### Why It Fails

- Agent lacks context about what you're working on
- Has to guess or ask clarifying questions
- May find wrong files
- Slower and less accurate

### The Fix

**Navigate first, then start session**

```bash
cd /company/SRE/helm/charts/my-service/
# Start Codex here

"Update resource limits in this helm chart"
```

Agent immediately knows context: SRE work, helm chart, specific service.

---

## Pitfall 7: Over-Compression

### What It Looks Like

Trying to minimize tokens at all costs:
- Stripping context to bare minimum
- Using abbreviations
- Removing examples
- Cutting out relevant files

### Why It Fails

- Agent lacks information needed to do good work
- Results are generic or wrong
- Have to provide context anyway through multiple clarifications
- Actually uses MORE tokens through back-and-forth

### The Fix

**Tokens are cheap, clarity is expensive**

Don't compress unless you're truly hitting limits. Provide rich context upfront.

**Instead of compressing, use isolation**: Split into multiple tabs rather than cramming everything into compressed context.

---

## Pitfall 8: Ignoring Tool Output

### What It Looks Like

Agent says: "I found these issues in the helm chart template..."

You: "Okay, now do this other thing" (without addressing issues)

### Why It Fails

- Agent identified real problems
- Moving forward without fixing them compounds issues
- May deploy broken configuration
- Wastes agent's analytical work

### The Fix

**Review and address agent findings**

```
Agent: "Template validation shows missing required field 'resources.limits'"

You: "Good catch. Add standard resource limits based on our other services"

[Wait for fix]

You: "Validate again to confirm all issues resolved"
```

---

## Pitfall 9: Not Using Available Tools

### What It Looks Like

You manually copy-paste Azure resource information into prompts when you have Azure MCP available.

You manually search through wikis instead of letting agent use Azure DevOps MCP.

### Why It Fails

- More manual work for you
- Information may be incomplete or outdated
- Agent could do this automatically
- Slower workflow

### The Fix

**Leverage MCPs and integrations**

```
# Instead of:
"Here's a list of our VMs I copied from Azure Portal..."

# Do this:
"Use Azure MCP to list all VMs in the production resource group"

# Instead of:
"Let me find that wiki page..."

# Do this:
"Search the Azure DevOps wiki for documentation about deployment procedures"
```

---

## Pitfall 10: Mixing Read and Write Operations Carelessly

### What It Looks Like

In the same prompt:
```
"Check if the database is healthy and if not, restart it"
```

### Why It Fails

- No chance to review findings before action
- Agent might make wrong decision
- Can't intervene if analysis is incorrect
- Dangerous for production systems

### The Fix

**Separate analysis from action**

```
Step 1: "Check database health and report findings"

[Review results]

Step 2: "Based on the findings above, here's what to do: [your decision]"
```

For critical systems, always review before executing changes.

---

## Pitfall 11: Not Coloring Tabs

### What It Looks Like

10 terminal tabs all the same color. Which one was investigation? Which was fix implementation?

### Why It Fails

- Can't quickly identify tab purposes
- Waste time clicking through tabs
- Risk of making changes in wrong tab
- Mental overhead tracking what's what

### The Fix

**Use consistent color coding**

- 🟢 Green: Active work, making changes
- 🔵 Blue: Read-only, investigation, reference
- 🟡 Yellow: Long-running reference tabs
- 🔴 Red: Urgent/emergency work

Quick visual scan tells you everything.

---

## Pitfall 12: Forgetting Context Reset

### What It Looks Like

```
Session 1: "Update the user-api helm chart" [done]

Session 2 (later): "Now update it to use the new image tag"
```

Session 2 has no idea what you did in Session 1.

### Why It Fails

- Each session is independent
- No memory of previous sessions
- Agent doesn't know current state
- Gives generic or wrong advice

### The Fix

**Each session needs full context**

```
Session 2: 
"I previously updated the user-api helm chart at /company/SRE/helm/charts/user-api/.

Current state: Chart is at version 2.1.0, using image my-registry/user-api:v1.5

Now I need to: Update to use image tag v1.6"
```

Or use handoff prompts from previous session.

---

## Pitfall 13: Not Testing Agent Output

### What It Looks Like

Agent generates terraform/helm/script.

You: "Great!" and immediately deploy to production.

### Why It Fails

- Agent can make mistakes
- Syntax might be wrong
- Logic might have flaws
- Security issues might exist

### The Fix

**Always validate and test**

```
1. Review generated code carefully
2. Test syntax (helm lint, terraform validate)
3. Test in non-production first
4. Have agent explain its changes
5. Spot check critical sections

Example:
"Explain what this change does and why you made this choice"
"Are there any potential issues with this approach?"
"Test this configuration before I apply it"
```

---

## Pitfall 14: Poor Data Store Design

### What It Looks Like

**Azure inventory JSON**:
```json
{"resources": "vm-prod-1,vm-prod-2,aks-prod,storage-prod..."}
```

Unstructured, unsearchable, not useful.

### Why It Fails

- Can't search effectively
- No structure for queries
- Human and LLM both struggle to use it
- Misses important metadata

### The Fix

**Design for searchability**

```json
{
  "resources": [
    {
      "name": "vm-prod-1",
      "type": "VirtualMachine",
      "location": "eastus",
      "resourceGroup": "production-rg",
      "properties": {
        "vmSize": "Standard_D4s_v3",
        "os": "Ubuntu 22.04"
      }
    }
  ],
  "metadata": {
    "lastUpdated": "2024-11-07T10:00:00Z",
    "source": "az cli"
  }
}
```

Now searchable by type, location, size, etc.

---

## Pitfall 15: Abandoning Multi-Tab Workflow Too Quickly

### What It Looks Like

"This multi-tab thing is complicated, I'll just use one tab"

After first minor confusion, reverting to old habits.

### Why It Fails

- Miss out on major productivity gains
- Complex tasks remain difficult
- Can't parallelize work
- Context management stays hard

### The Fix

**Give it time to become natural**

- Start with simple 2-tab workflows
- Gradually increase complexity
- Practice on non-critical tasks first
- Use color coding to reduce confusion
- After 2-3 weeks, it becomes second nature

Like learning git: awkward at first, invaluable later.

---

## Quick Diagnostic Guide

**Problem**: Agent seems confused

**Check**:
- [ ] Did I provide file paths?
- [ ] Did I explain context?
- [ ] Am I in right directory?

**Problem**: Results aren't what I need

**Check**:
- [ ] Was my prompt specific enough?
- [ ] Did I explain success criteria?
- [ ] Is my data store up to date?

**Problem**: Context keeps filling up

**Check**:
- [ ] Should I split into multiple tabs?
- [ ] Time for a handoff prompt?
- [ ] Am I mixing too many concerns?

**Problem**: Can't keep track of tabs

**Check**:
- [ ] Am I using color coding?
- [ ] Do I have too many tabs open?
- [ ] Should I close finished tabs?

---

## The One Thing to Remember

**Context Engineering is about making the agent's job easy.**

If the agent is struggling, confused, or giving poor results:
- You probably didn't give it enough context
- Not the agent's fault
- Fix: More specificity, more file paths, more explanation

Like managing humans: clear communication = good results.

---

## Next Steps

Review this list regularly. When something goes wrong, check if it matches a pitfall.

**Most common pitfalls for beginners**:
1. Vague file references
2. Starting in wrong directory
3. Assuming prior knowledge

Master these three first, then worry about advanced pitfalls.

---

**[← Back to Practical Patterns](06-practical-patterns.md)** | **[Quick Reference →](quick-reference.md)**
