# Module 7: Common Pitfalls

Learn from these mistakes so you don't have to make them yourself.

---

## Section 1: Communication Pitfalls

How you communicate with AI directly impacts the quality of results. These pitfalls stem from unclear, incomplete, or ineffective communication patterns.

---

## Pitfall 1: Vague File References

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

## Pitfall 2: Assuming Prior Knowledge

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

## Pitfall 3: Forgetting Context Reset

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

## Pitfall 4: Command-Style Communication Anti-Patterns

### What It Looks Like

Treating AI like a command-line interface instead of a knowledgeable coworker:

```
"Fix disk space alert threshold to 85%"
"Write terraform for S3 bucket"
"Check the logs"
"Deploy to production"
```

**What's missing**: Context, reasoning, uncertainty, environment details.

### Why It Fails

**1. Tokens aren't that expensive**

People think: "I'll save tokens by being brief"

Reality:
- Brief prompt: 10 tokens, unclear result: restart conversation (100+ tokens)
- Rich prompt: 50 tokens, clear result: done first try

**Net result**: Being too brief wastes MORE tokens through clarification cycles.

**2. You miss the learning opportunity**

Command-style prompts get answers, not explanations:

```
Command: "Fix the alert"
Result: Changed threshold
You learned: Nothing

Natural language: "I need to update our disk alert threshold from 80% to 85%.
We've been getting too many false positives. I'm not sure if 85% is right, or
if we should look at rate of change instead. Can you explain the trade-offs?"

Result: Changed threshold WITH explanation of why
You learned: When to use threshold vs rate-of-change alerts
```

**3. Hiding uncertainty increases hallucination risk**

Counter-intuitive truth: **Expressing doubt makes AI more accurate.**

```
Command-style (confident): "Deploy the new configuration"
AI thinks: They know what they're doing, proceed confidently
Risk: High - no verification prompts

Natural (expressing uncertainty): "I need to deploy this configuration, but
I'm not sure if I should test in staging first or if this is safe to go
straight to prod. What do you recommend?"

AI thinks: They want guidance, provide thorough explanation
Risk: Low - AI explains options and safety considerations
```

**4. Missing environmental context causes wrong solutions**

```
Command: "Write backup script"
Result: Generic backup script

vs.

Natural: "I need to implement backups for our PostgreSQL database. Looking at
our existing backups in /company/SRE/scripts/backups/, it seems we use pg_dump,
but I'm not sure if that's the right approach for our 500GB database. We need
point-in-time recovery capability. What approach should we use?"

Result: Tailored solution considering size, existing patterns, requirements
```

### The Fix

**Talk like you're explaining to a skilled coworker who needs context**

Use the natural language communication pattern from Module 1:

1. **What you're trying to accomplish** (the goal)
2. **What you know and what you're unsure about** (context + uncertainty)
3. **What you've already tried or checked** (prior work)
4. **Where the relevant information is** (file paths, systems)
5. **What success looks like** (acceptance criteria)

### Real Examples: Before and After

**Example 1: Infrastructure Change**

❌ **Command-style (ineffective)**:
```
"Update memory limits"
```

✅ **Natural language (effective)**:
```
I need to increase memory limits for our user-api service. Currently set to
512Mi in /company/SRE/helm/charts/user-api/values.yaml, but pods are getting
OOMKilled during peak traffic (I saw this in the logs at /tmp/oom-events.log).

I'm not sure if we should go to 1Gi or 2Gi. Our similar auth-api service uses
1Gi and seems fine. What would you recommend based on the OOM patterns in
those logs?
```

**What you get**:
- Analysis of OOM patterns
- Recommendation with reasoning
- Comparison to similar services
- You learn how to size memory limits

---

**Example 2: Troubleshooting**

❌ **Command-style (ineffective)**:
```
"Fix database connections"
```

✅ **Natural language (effective)**:
```
Our application started getting database connection errors about 20 minutes ago.
Looking at /var/log/app.log, I see "connection timeout" errors, but I'm not
sure if that's the root cause or a symptom of something else.

I've checked:
- Database is running (pg_isready says yes)
- Connection string hasn't changed in the app config
- No recent deploys to the app or database

I'm not very experienced with PostgreSQL connection debugging. Can you help me:
1. Understand what else to check
2. Interpret the error messages in the logs
3. Determine if this is an app issue or database issue
```

**What you get**:
- Diagnostic guidance
- Education on PostgreSQL troubleshooting
- Step-by-step investigation plan
- You learn connection debugging patterns

---

**Example 3: New Tool/Technology**

❌ **Command-style (ineffective)**:
```
"Set up Istio service mesh"
```

✅ **Natural language (effective)**:
```
I need to implement a service mesh for our microservices architecture. I've
heard Istio is the standard choice, but I've never set one up before and I'm
not sure if it's the right fit for our environment.

Current state:
- 15 microservices running in Kubernetes
- Using nginx-ingress for external traffic
- Need mutual TLS between services
- Need better observability and traffic management

I'm uncertain about:
- Whether Istio is the right choice vs Linkerd or Consul
- How complex the migration will be
- What the performance impact might be
- If our cluster has enough resources (currently running 20 nodes)

Can you help me understand the trade-offs and whether Istio makes sense for us?
Then we can plan the implementation if it's the right choice.
```

**What you get**:
- Comparison of service mesh options
- Evaluation based on your specific requirements
- Migration complexity assessment
- Resource requirement analysis
- You learn service mesh architecture and can make informed decision

---

### Common Command-Style Mistakes

❌ **Being too brief to save tokens**
```
"Fix it"
```
Tokens saved: 5
Tokens wasted on clarification: 200+

✅ **Rich context costs more upfront, saves overall**
```
"The deployment is failing with 'ImagePullBackOff' error. The image exists in
our registry at registry.company.com/user-api:v2.1.0. I can pull it manually
from my laptop. The deployment YAML is at /company/SRE/k8s/user-api-deployment.yaml.
I think it might be an image pull secret issue, but I'm not sure how to verify that."
```
Tokens used: 60
Tokens wasted: 0 (solved first try)

---

❌ **Hiding uncertainty to seem confident**
```
"Deploy this configuration to production"
```
Result: AI proceeds confidently with potentially risky action

✅ **Expressing uncertainty triggers safety checks**
```
"I've created this configuration change, but I'm not sure if I should test it
in staging first or if there are any risks I'm not seeing. What's the safest
way to deploy this?"
```
Result: AI provides safety guidance, testing recommendations, risk analysis

---

❌ **Using jargon without context**
```
"Fix the CRD"
```
Which CRD? What's broken? What's the desired state?

✅ **Explain terms in context**
```
"Our Istio VirtualService CRD (Custom Resource Definition) for the user-api
service isn't routing traffic correctly. The YAML is at /k8s/user-api-virtualservice.yaml.
Traffic should be going to v2 of the service, but it's still hitting v1. I'm
not very familiar with VirtualService routing rules - can you help me understand
what's wrong and how to fix it?"
```

---

### When Being Brief is Okay

**Quick factual lookups**:
```
"What's the kubectl command to get pod logs from last hour?"
```

**Follow-up questions in an ongoing conversation**:
```
[After detailed discussion of a configuration]
"What about the timeout settings?"
```

**But default to natural language for**:
- New tasks
- Complex problems
- Unfamiliar territory
- Production changes
- Anything safety-critical

### The Meta-Benefit

Natural language communication skills transfer:

- **Writing documentation**: Same clarity helps readers
- **Creating tickets**: Same context helps teammates
- **Incident reports**: Same detail aids post-mortems
- **Asking colleagues for help**: Same pattern works with humans

**Communication is a professional skill, whether you're talking to AI or people.**

> ⚠️ **Accountability**: When you communicate poorly with AI and get poor results, that's on you, not the AI. Treat AI communication as a professional skill worth developing, just like writing good documentation or creating clear tickets.

### Key Takeaway

**Stop writing commands. Start providing context.**

The few extra seconds of explanation save minutes (or hours) of clarification, rework, and debugging.

---

## Section 2: Workflow Organization Pitfalls

How you structure your AI-assisted work impacts productivity and clarity. These pitfalls arise from poor task organization and workflow management.

---

## Pitfall 5: The Everything Tab

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

## Pitfall 7: Not Coloring Tabs

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

## Pitfall 8: Over-Compression

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

## Pitfall 9: No Handoff Strategy

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

## Pitfall 10: Abandoning Multi-Tab Workflow Too Quickly

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

## Section 3: Data and Context Management Pitfalls

How you manage information sources and tools impacts efficiency and context usage. These pitfalls involve poor data management and tool selection.

---

## Pitfall 11: Stale Data Stores

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

## Pitfall 12: Poor Data Store Design

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

## Pitfall 13: Not Using Available Tools

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

## Pitfall 14: Over-Installing MCP Servers

### What It Looks Like

Your MCP server configuration keeps growing:

```json
{
  "mcpServers": {
    "jira": {...},
    "github": {...},
    "aws": {...},
    "azure": {...},
    "pagerduty": {...},
    "notion": {...},
    "weather": {...},
    "slack": {...},
    "kubernetes-dashboard": {...},
    "database-query": {...}
  }
}
```

You installed them "just to try" or "might need someday."

**Reality check**: When's the last time you actually used the weather API integration?

### Why It Fails

**1. Context pollution**

Every MCP server consumes context tokens:
- Tool schemas are loaded at session start
- 10 servers with 10 tools each = 100 tool schemas in your context
- That's 20k-30k tokens before you type a single word
- Less room for your actual work

**2. The "forgot what's installed" problem**

```
You: [Running monthly audit]
You: "Wait, I have a Notion MCP installed?"
You: "I don't even use Notion anymore"
Server: [Has been wasting context for 6 months]
```

**3. The "might need it someday" trap**

```
Thought process:
"This weather API could be useful for on-call planning"
"I'll install it just in case"

Reality:
- Installed: March
- Last used: March (during testing)
- Context cost: Every. Single. Session.
- Actual value: Zero
```

**4. Using 1 tool from a 50-tool server**

```
AWS MCP provides:
- EC2 tools (15 tools)
- S3 tools (12 tools)
- RDS tools (10 tools)
- Lambda tools (8 tools)
- VPC tools (5 tools)

You actually use: S3 bucket listing

Context cost: 50 tool schemas
Value delivered: 1 tool's worth
Efficiency: Terrible
```

### The Fix

**Pattern 1: Intentional, audited installation**

```bash
# Before installing, answer these questions:

1. What specific, recurring task will this solve?
   ❌ "Might be useful"
   ✅ "I check PagerDuty 15+ times during on-call weeks"

2. How often will I actually use it?
   ❌ "Occasionally"
   ✅ "Daily during incident response"

3. Can I accomplish this another way?
   ✅ Check if built-in tools work
   ✅ Consider local data store (create searchable inventories)
   ✅ Evaluate if CLI + AI works instead

4. What's the context cost vs. value?
   Server tools: 20 tools = ~5k tokens
   Usage frequency: Daily = high value
   Decision: Worth it

   vs.

   Server tools: 30 tools = ~8k tokens
   Usage frequency: Monthly = low value
   Decision: Not worth it
```

**Pattern 2: Task-specific installation and removal**

```bash
# On-call rotation example

# Starting on-call week
echo "Installing PagerDuty MCP for on-call rotation"
# [Add to config]

# Use heavily during on-call
# High value this week: 20+ incident queries

# End of on-call rotation
echo "Removing PagerDuty MCP - rotation complete"
# [Remove from config]

# Result: Zero context cost when not on-call
```

**Pattern 3: Monthly audit ritual**

```bash
# First Monday of each month
# List installed servers
cat ~/.claude-code/config.json | jq '.mcpServers | keys'

# For each server, ask:
1. When did I last use this?
   - This week: Keep
   - This month: Evaluate frequency
   - Can't remember: Remove immediately

2. What specific task required it?
   - Can name tasks: Good sign
   - "General purpose": Warning sign
   - Can't remember: Remove

3. How many tools do I actually use vs. how many it provides?
   - Using most: Efficient
   - Using 1-2: Find alternative

# Be ruthless about removal
# Context is too valuable to waste on unused servers
```

### Real Example: The Context Cost

**Scenario**: Complex Kubernetes debugging session

**What you need**:
- Read 10 YAML manifests (~15k tokens)
- Include recent logs (~10k tokens)
- Reference architecture doc (~20k tokens)
- Iterative troubleshooting (~30k tokens)
- **Total: ~75k tokens**

**With 5 unused MCP servers installed**:
- MCP tool schemas: ~12k tokens
- Available for actual work: ~63k tokens
- **Result: Might hit context limits, need to restart session, lose debugging context**

**With intentional MCP management**:
- Removed unused servers
- Available for actual work: ~75k tokens
- **Result: Complete debugging session without context issues**

**The 12k tokens you saved by removing unused servers = room for your actual work**

### Common Excuses (and Rebuttals)

❌ **"But context windows are huge now (200k tokens)!"**

True, but:
- Complex tasks still consume context quickly
- Multiple files, large docs, long conversations add up
- 10 MCP servers = 20-30k tokens you'll never get back
- That's 10-15% of your context budget, wasted on tools you don't use

✅ **Better**: Treat context like memory in production systems. Just because you have 64GB RAM doesn't mean you run 50 services you don't need.

---

❌ **"I might need it for an edge case someday"**

You can install it when that day comes:
- Installation takes 2 minutes
- You'll remember to install when you actually need it
- No context cost in the meantime

✅ **Better**: Just-in-time installation. Install when needed, remove when done.

---

❌ **"I want to try out new MCP servers as they come out"**

Exploration is fine, but:
- Try them in a test session
- Don't leave them permanently installed
- Remove after evaluation period (1 week max)

✅ **Better**: Trial period pattern. Install → Test for 1 week → Decide (keep/remove) → Default to remove.

### Reference Module 3 for Deep Dive

This pitfall is covered in depth in **Module 3: MCP Servers - When and Why**, which includes:
- Full evaluation framework for deciding to install
- Technical deep-dive on context cost
- Decision trees and usage patterns
- Best practices for MCP server management
- When local data stores are better than MCP servers

> ⚠️ **Accountability**: Every MCP server you install consumes context in every session. If you can't justify the context cost with specific, frequent usage, you're wasting resources. Audit monthly. Be ruthless about removal. Context is too valuable to waste on "might need someday" tools.

### Quick Self-Check

```
Right now, without looking:

1. How many MCP servers do you have installed?
   - Don't know: Go audit immediately
   - Know exactly: Good start

2. When did you last use each one?
   - Can't remember: Time to remove it
   - This week: Probably worth keeping
   - This month: Evaluate frequency

3. Which tools from each server do you actually use?
   - "All of them": Efficient, keep it
   - "A few": Consider alternatives
   - "Not sure": Definitely remove it
```

If you failed this self-check, **stop reading and go audit your MCP servers right now.** Seriously. You're wasting context in every session.

---

## Section 4: Safety and Accountability Pitfalls

How you verify and validate AI-generated work impacts production safety. These pitfalls involve insufficient verification, blind trust, and accountability failures.

---

## Pitfall 15: Blind Trust in AI Outputs

### What It Looks Like

**Scenario 1**: Treating AI as infallible
```
AI: "Here's a database migration script"
You: "Perfect!" [Runs in production without reading]
Result: Data corruption, emergency rollback, incident
```

**Scenario 2**: Not understanding the code
```
AI: [Generates 200-line Terraform module]
You: "Looks good!" [Merges PR without understanding]
Teammate: "What does this module do?"
You: "Uh... AI wrote it"
Teammate: "But what does it DO?"
You: "I'm not sure..."
```

**Scenario 3**: Skipping peer review because "AI wrote it"
```
You: "AI wrote this, so it's probably fine"
You: [Skips normal code review process]
You: [Deploys to production]
Result: Security vulnerability ships to prod
```

### Why It Fails

**1. AI makes mistakes**

AI is powerful but not perfect:
- Can misunderstand requirements
- May miss edge cases
- Sometimes hallucinates functions that don't exist
- Can introduce security vulnerabilities
- Might use deprecated patterns

**Example: The subtle bug**
```python
# AI-generated code
def cleanup_old_files(directory, days=7):
    cutoff = datetime.now() - timedelta(days=days)
    for file in os.listdir(directory):
        if os.path.getmtime(file) < cutoff.timestamp():
            os.remove(file)  # BUG: missing join with directory
```

If you don't read it carefully, you won't notice `file` needs to be joined with `directory`.

**2. You're accountable, not the AI**

When production breaks:
- "AI wrote the code" is not an acceptable excuse
- Your name is on the commit
- You executed the change
- You are responsible

From Module 1 Accountability Framework:

> **AI can read prod. You execute against prod.**

**3. You miss learning opportunities**

```
Blind trust approach:
- Copy AI code
- Deploy it
- Learn nothing
- Can't maintain it
- Can't debug it
- Depend on AI for every change

Understanding approach:
- Read AI code
- Understand what it does
- Ask questions about unfamiliar patterns
- Learn new techniques
- Can maintain and modify it
- Build expertise
```

**4. You can't explain it to others**

**In incident post-mortem**:
```
Manager: "Why did the script delete production data?"
You: "Um, AI wrote the script"
Manager: "But you ran it. Did you understand what it would do?"
You: "I trusted the AI"
Manager: "..."

This is a career-limiting conversation.
```

### The Fix

**Apply the same standards as human-written code**

**Standard 1: Review thoroughly**

```
When AI generates code:

□ Read every line
□ Understand what each section does
□ Check for security issues
□ Look for error handling
□ Verify edge cases are handled
□ Ensure it matches requirements
□ Ask AI to explain anything unclear
```

**If you can't explain what the code does, don't run it.**

**Standard 2: Test before production**

From Module 6 Progressive Verification:

```
1. Dev environment: Test with dry-run, then actual run
2. Staging environment: Verify with production-like conditions
3. Production: Execute with monitoring and rollback ready

Never skip stages for high-risk changes.
```

**Standard 3: Peer review**

AI-generated code should go through the same review as human-written code:

```markdown
## PR Description
Database cleanup script for old session records.

Testing:
- [x] Tested with --dry-run in dev
- [x] Ran actual cleanup in dev (deleted 1000 test records)
- [x] Tested in staging (deleted 50k old sessions)
- [x] Verified data integrity after cleanup

Notes:
- Initial script generated by AI
- I reviewed all code and tested thoroughly
- Added additional error handling for database connection issues
- Modified batch size based on staging testing results

## Rollback Plan
Script runs in transaction. If verification fails, manual rollback from backup.
```

**Note that it's AI-generated, but also note that YOU verified it.**

**Standard 4: Understand before executing**

```
Good verification conversation:

You: "Explain what this script does, step by step"
AI: [Explains each section]
You: "What happens if the database connection fails mid-script?"
AI: [Explains error handling]
You: "What's the worst case if something goes wrong?"
AI: [Explains failure modes]

Now you understand it well enough to run it safely.
```

### Real Example: Production Incident Avoided

**Scenario**: AI generates a cleanup script

**Blind trust approach**:
```bash
You: "Generate a script to delete old logs"
AI: [Generates script]
You: ./cleanup.sh
Result: Deletes production logs including last 24 hours
Incident: Lost crucial debugging data
```

**Verification approach**:
```bash
You: "Generate a script to delete logs older than 30 days, include dry-run"
AI: [Generates script with --dry-run flag]

You: [Reads script carefully]
You: "Wait, this uses 'mtime' which is modification time, not creation time"
You: "If logs were rotated recently, they'd be deleted even if they're new"

You: "Update script to use creation time, not modification time"
AI: [Updates script]

You: ./cleanup.sh --dry-run
Output: "Would delete: /var/log/app-2024-10-15.log"
You: "That's only 3 weeks old, not 30 days. Let me check the logic..."

You: [Finds bug in date calculation]
You: "Fix the date calculation"
AI: [Fixes bug]

You: ./cleanup.sh --dry-run  # Try again
Output: "Would delete: /var/log/app-2024-08-10.log"
You: "That's correct, more than 30 days"

You: [Runs in dev first]
You: [Verifies results]
You: [Then runs in production]
Result: Safely cleaned up old logs, kept recent ones
```

**Your verification caught two bugs before production.**

### Pattern: Verification Checklist

For AI-generated code headed to production:

```
□ I have read and understand all the code
□ I can explain what it does to a teammate
□ I have tested it in a non-production environment
□ I have verified error handling
□ I have checked for security issues
□ I have reviewed for our coding standards
□ It has passed peer review (or will before deploy)
□ I have a rollback plan
□ I know what to monitor after deployment
□ I am confident this is safe to run
```

**If you can't check all boxes, don't run it in production.**

### Anti-Pattern: Confidence Without Understanding

```
Wrong: "AI is really good, so this is probably fine"
Right: "AI is really good at generation, so I should verify carefully"

Wrong: "I don't understand this part, but AI wouldn't write bad code"
Right: "I don't understand this part, so I need AI to explain it"

Wrong: "This looks complicated, but AI knows what it's doing"
Right: "This looks complicated, I need to understand it before running it"
```

### The Trust Paradox

**The more you trust AI's ability to generate code, the more carefully you should verify it.**

Why? Because AI can confidently generate code that looks correct but has subtle bugs.

**Trust the capability, verify the output.**

> ⚠️ **Accountability**: You are responsible for everything that runs in production, regardless of who or what wrote it. "AI wrote it" is never an excuse for production incidents. If you don't understand the code well enough to explain and defend it, don't run it.

### Key Takeaways

1. **AI is a powerful tool, not a replacement for your judgment**
2. **Same review standards apply: human-written or AI-written**
3. **Understanding is mandatory: If you can't explain it, don't run it**
4. **Verification is your job: AI generates, you verify**
5. **You are accountable: Your name, your responsibility**

**Blind trust in AI is professional negligence.**

---

## Pitfall 16: Skipping Verification

### What It Looks Like

**Scenario 1**: Testing in prod first (or not testing at all)
```
AI: "Here's a script to update all user roles in the database"
You: [Runs in production immediately]
Result: Updates wrong users, security incident
```

**Scenario 2**: No dry-run testing
```
AI: "Here's a cleanup script for old resources"
You: [Runs script]
Script: [Deletes critical resources]
You: "Wait, I didn't mean THOSE resources!"
Too late.
```

**Scenario 3**: Assuming AI is always correct
```
AI: "This Terraform will create the infrastructure"
You: terraform apply -auto-approve  # No review, no plan check
Terraform: [Creates resources in wrong region]
You: "Why is everything in us-west-1 instead of us-east-1?"
```

**Scenario 4**: Running scripts without reading them
```
You: "Generate a deployment script"
AI: [Generates script]
You: chmod +x deploy.sh && ./deploy.sh
Script: [Has bug, deploys to wrong environment]
Result: Production outage
```

### Why It Fails

**1. Speed without safety is reckless**

```
Time saved by skipping verification: 10 minutes
Time spent on incident response: 4 hours
Time spent on post-mortem: 2 hours
Time spent rebuilding trust: Weeks

Net result: Not a time saver
```

**2. AI can't know your environment's edge cases**

AI doesn't know:
- That "old" resources include your monitoring stack
- That the database has non-standard column names
- That your production environment is actually called "prd" not "prod"
- That service-account-1 is critical, service-account-2 is test

**You know these things. Verification is where you catch AI's blind spots.**

**3. Errors compound in automation**

Manual process: You notice issues as you go, stop when something looks wrong

Automated script: Executes all steps, compounds errors

```
Manual cleanup:
You: [Looks at resource list]
You: "Wait, that's the production load balancer, skip that one"

Scripted cleanup without verification:
Script: Deleting load-balancer-prod...
Script: Deleting database-prod...
Script: Deleting storage-prod...
You: "STOP! OH NO!"
Script: Done. Deleted 15 resources.
```

### The Fix

**Implement the verification workflow from Module 6**

**Layer 1: Dry-Run Testing**

```bash
# Every operational script should have dry-run mode

You: "Generate a script to scale down non-prod resources. Include dry-run mode."

AI: [Generates script with --dry-run flag]

You: ./scale-down.sh --dry-run

Output:
"DRY RUN MODE
Would scale down:
- dev-cluster: 10 nodes → 2 nodes
- staging-cluster: 8 nodes → 2 nodes
- prod-cluster: 20 nodes → 20 nodes (skipping - production)

Run without --dry-run to execute"

You: [Reviews list]
You: "Good, it's not touching production. Safe to run."

You: ./scale-down.sh

Result: Safe, verified operation
```

**From Module 6 Dry-Run Pattern:**
> Dry-run is crucial for safety, learning, verification, and communication. **Running scripts in production without first testing with dry-run is negligent.**

**Layer 2: Progressive Verification (Dev → Review → Prod)**

From Module 6 Progressive Verification Workflow:

```
Phase 1: Development Environment
- Learn the task manually (if unfamiliar)
- Have AI generate automation with dry-run
- Test with dry-run first
- Run actual automation in dev
- Verify results thoroughly
- Fix any issues discovered

Phase 2: Review/Staging Environment
- Run same automation in review environment
- Verify it works in environment closer to prod
- Test with realistic data volumes
- Identify environment-specific issues

Phase 3: Production Environment
- Run automation in production
- Monitor closely
- Have rollback plan ready
```

**Never skip directly to production for high-risk changes.**

**Layer 3: Code Review for Generated Scripts**

```
When AI generates a script for production:

You: [Read every line]
You: [Understand the logic]
You: [Look for issues]
You: "Explain what happens if the API call fails"
AI: [Explains error handling]
You: "Add error handling for network timeouts"
AI: [Updates script]

You: [Test in dev with --dry-run]
You: [Test in dev with actual execution]
You: [Verify results]

You: [Create PR for peer review]
Teammate: [Reviews script]
Teammate: "Why are you using 'rm -rf' here?"
You: "Good catch, that's too aggressive"
You: [Update script to be safer]

You: [Merge after approval]
You: [Test in staging]
You: [Execute in prod with monitoring]

Result: Multiple verification layers caught issues
```

**Layer 4: Verification Checklist**

Before running AI-generated automation in production:

```
□ I have run this with --dry-run
□ I understand what each step does
□ I have tested in dev environment
□ I have tested in staging environment
□ Error handling is appropriate
□ Rollback procedure is documented
□ Monitoring is in place to detect issues
□ Team has been notified of change
□ Rollback plan is ready
□ I know what success looks like
```

**If any box is unchecked, you're not ready for production.**

### Real Example: The Database Migration

**Wrong approach (skipping verification)**:
```
You: "Generate a SQL migration to add user preferences table"
AI: [Generates migration SQL]
You: psql prod -f migration.sql
Migration: [Runs]
Application: [Starts failing]
You: "What happened?"
[Investigation reveals migration broke foreign key constraints]
You: [Emergency rollback]
You: [Incident post-mortem]
```

**Right approach (progressive verification)**:
```
You: "Generate a SQL migration to add user preferences table. Include
rollback script and verification queries."

AI: [Generates migration, rollback, and verification SQL]

You: [Reads all SQL carefully]
You: "I see you're adding a foreign key to users table. Show me the
exact constraint."
AI: [Shows constraint]
You: "What happens if there are orphaned records?"
AI: [Explains, adds validation query to check first]

# Phase 1: Dev
You: [Runs migration in dev with transaction + rollback to test]
You: [Verifies rollback works]
You: [Runs migration for real in dev]
You: [Tests application against new schema]
You: "Application works in dev. Good."

# Phase 2: Staging
You: [Runs migration in staging]
You: [Verifies with production-like data volume]
You: [Runs automated test suite]
You: [Monitors for 24 hours]
You: "No issues in staging after 24 hours. Ready for prod."

# Phase 3: Production
You: [Schedules maintenance window]
You: [Notifies team]
You: [Runs verification query to check for orphaned records]
Query: "0 orphaned records found"
You: [Runs migration]
You: [Runs verification queries]
You: [Tests application]
You: [Monitors closely]
You: "Migration successful, application healthy"

Result: Safe, verified deployment
```

**The verification workflow caught potential issues at every stage.**

### Common Excuses (and Rebuttals)

❌ **"But verification takes time, and I need to move fast"**

```
Fast without verification:
- 5 minutes to execute
- 4 hours to fix incident
- Total: 4 hours 5 minutes

Slow with verification:
- 30 minutes to verify and test
- 5 minutes to execute
- 0 hours fixing incidents
- Total: 35 minutes

Which is actually faster?
```

✅ **Professional speed includes verification**

---

❌ **"This is a simple change, doesn't need testing"**

Famous last words before production incidents:

```
"It's just a config change" → Broke authentication
"It's just updating a timeout" → Caused cascading failures
"It's just a minor version bump" → Introduced breaking changes
"It's just a cleanup script" → Deleted production data
```

✅ **Simple changes can have complex consequences. Verify anyway.**

---

❌ **"I'll test it in production and rollback if there's an issue"**

```
Problems with "test in prod":
- Some changes can't be easily rolled back (data deletion, schema changes)
- Users experience failures during testing
- Incidents affect SLAs and customer trust
- On-call engineer gets paged
- Team loses confidence in your changes
```

✅ **Testing happens in non-prod. Deploying happens in prod.**

---

❌ **"AI is really good now, I can trust it"**

```
AI is good at generation. You are good at verification.

AI + You without verification = Risky
AI + You with verification = Powerful

Verification is not distrust of AI.
Verification is professional due diligence.
```

✅ **Trust the capability, verify the output. Always.**

### Integration with Other Patterns

**Verification + Learning While Working** (Module 6):
```
1. Learn task manually (understand what should happen)
2. Have AI generate automation (fast generation)
3. Verify automation (you recognize the steps)
4. Test progressively (dev → staging → prod)

Understanding + Verification = Safety
```

**Verification + Read vs Execute Pattern** (Module 6):
```
AI reads from production (safe)
AI generates solution (safe)
You verify solution (your responsibility)
You test in non-prod (safety layer)
You execute in production (accountable)
```

### Verification Workflow Template

Save this checklist for production changes:

```markdown
## Pre-Deployment Verification

### Code Review
- [ ] I have read and understood all generated code
- [ ] Code follows our team standards
- [ ] Error handling is appropriate
- [ ] Security review complete

### Testing
- [ ] Dry-run executed successfully
- [ ] Tested in dev environment
- [ ] Tested in staging environment
- [ ] Test results match expectations
- [ ] No unexpected side effects observed

### Production Readiness
- [ ] Rollback procedure documented
- [ ] Monitoring configured
- [ ] Team notified of change
- [ ] Maintenance window scheduled (if needed)
- [ ] Success criteria defined

### Post-Deployment
- [ ] Monitor for [TIME PERIOD]
- [ ] Verify success metrics
- [ ] Document any issues encountered
```

> ⚠️ **Accountability**: Skipping verification for high-risk changes is professional negligence. Each verification stage exists to catch issues before production. Progressive verification (Dev → Review → Prod) is mandatory, not optional. Dry-run testing is mandatory, not optional. If you skip verification and cause an incident, that's on you.

### Key Takeaways

1. **Verification is not optional** - It's professional due diligence
2. **Dry-run first** - Every time, no exceptions
3. **Progressive verification** - Dev → Staging → Prod for high-risk changes
4. **Trust but verify** - AI generates well, you verify thoroughly
5. **Speed through safety** - Verification prevents incidents, incidents waste time
6. **You are accountable** - Verification is your responsibility

**Fast execution without verification is not engineering. It's gambling.**

---

## Pitfall 17: Not Testing Agent Output

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

## Pitfall 18: Ignoring Tool Output

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

## Pitfall 19: Mixing Read and Write Operations Carelessly

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
4. Command-style communication
5. Blind trust in AI outputs

Master these five first, then worry about advanced pitfalls.

---

**[← Back to Practical Patterns](06-practical-patterns.md)** | **[Quick Reference →](quick-reference.md)**
