# Context Engineering Quick Reference

One-page cheat sheet for working with AI coding assistants.

---

## The Four Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **SELECT** | Point to relevant info | "Check /terraform/main.tf for AKS config" |
| **WRITE** | Save for later | Build local work item inventory |
| **ISOLATE** | Separate concerns | One tab per helm chart update |
| **COMPRESS** | Context limit approaching | Generate handoff prompt at 50% |

---

## Starting a Session Right

```
✅ DO THIS:

cd /company/SRE/helm/charts/my-service/  # Navigate first

I need to update resource limits for my-service.

Context:
- Current chart in this directory
- Production values at values/production.yaml
- Recent OOM incidents logged in /notes/incidents/2024-11.md

Task: Increase memory limit from 512Mi to 1Gi
```

```
❌ NOT THIS:

"Update the memory limits"
```

---

## Multi-Tab Decision Tree

```
Independent tasks?           → Separate tabs
Tasks share context?         → Same tab
Long investigation?          → Dedicated tab
Quick one-off?              → Master tab is fine
Context approaching 50%?    → Generate handoff, new tab
```

---

## Tab Color Coding

- 🟢 **Green**: Active work, changes in progress
- 🔵 **Blue**: Investigation, read-only
- 🟡 **Yellow**: Reference, stays open
- 🔴 **Red**: Urgent/emergency work

---

## File Path Rules

❌ Vague: "Check the config"  
✅ Specific: "Check /company/SRE/terraform/main.tf"

❌ Relative: "Look in the logs"  
✅ Absolute: "Check /var/log/app/error.log"

❌ Assumed: "The helm chart"  
✅ Named: "The ingress-nginx helm chart at /company/SRE/helm/charts/ingress-nginx/"

---

## Handoff Prompt Technique

**When**: Context usage crosses 50%

**How**: 
```
Give me a handoff prompt I can copy into a new Codex session to continue this work.
```

**Result**: Agent generates comprehensive summary with:
- Location and files
- Work completed
- Work remaining  
- Key decisions made
- Next immediate action

---

## Data Store Formats

| Format | Use For | Example |
|--------|---------|---------|
| **Markdown** | Docs, runbooks, notes | Incident reports, procedures |
| **JSON** | Structured data | Azure inventories, work items |
| **CSV** | Simple tables | Quick resource lists |

---

## Live vs. Local Decision

| Use Live Queries | Use Local Stores |
|-----------------|------------------|
| Current state needed | Historical data |
| Making changes | Reference information |
| Fast-changing data | Large datasets |
| Small queries | Repeated searches |

**Example**:
- Live: "What's current CPU usage?" (Azure MCP)
- Local: "Has this error happened before?" (Search incident logs)

---

## Common Prompts

### Start Investigation
```
Context: [describe issue]
Location: [directory path]
Available info: [logs, configs, etc.]
Task: Investigate root cause
```

### Update Configuration
```
I need to update [specific config]
File: [exact path]
Current value: [what it is now]
Desired value: [what it should be]
Reason: [why changing]
```

### Search for Information
```
Search [directory/file/data store] for [specific pattern or keywords]
Context: [why I need this]
```

### Generate Documentation
```
Based on our work above, create [type of doc]
Include: [specific sections]
Save to: [exact path]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent seems confused | Provide more specific file paths |
| Losing track of work | Use handoff prompts more frequently |
| Context filling up fast | Split into multiple tabs earlier |
| Wrong information | Check if data stores are up to date |
| Too many tabs | Close finished ones, keep reference tabs |

---

## Red Flags

🚩 Prompts without file paths  
🚩 Mixing 3+ different tasks in one tab  
🚩 Data stores not updated in months  
🚩 Starting sessions in root directory  
🚩 No handoffs despite many messages  
🚩 Asking agent to "remember" from previous sessions

---

## The Three-Step Check

Before hitting enter on a prompt:

1. **SELECT**: Did I point to the right files?
2. **CONTEXT**: Did I explain what and why?
3. **CLARITY**: Will this make sense to someone with no prior knowledge?

---

## Emergency Quick Start

**New to this? Start here:**

1. Navigate to your working directory
2. Tell the agent what you're doing
3. Point to relevant files
4. Ask specific questions

**Example**:
```bash
cd /company/SRE/helm/charts/my-service/

"I need to update this service's resource limits. 
Current config in values.yaml. 
Show me the current limits first."
```

---

## Remember

- **Tokens are cheap** - Don't over-optimize, provide good context
- **Isolation beats compression** - Use multiple tabs before compressing
- **Be specific** - File paths, not descriptions
- **Let the agent navigate** - It can find files, you guide the search
- **One agent, one job** - Separate tabs for separate concerns

---

## Learn More

- Full course materials in training repo
- Practice exercises in `workshop-exercises.md`
- Real-world patterns in `06-practical-patterns.md`

---

**Print this page and keep it handy!**
