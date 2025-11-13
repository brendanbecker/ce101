# Context Engineering Quick Reference

One-page cheat sheet for working with AI coding assistants.

---

## Core Mindset

**Space Jam Theory**: If you can dream it, you can at least start it
- Don't self-limit based on complexity
- AI helps break down big problems into small ones
- You bring expertise, AI brings generation speed

**Accountability Framework**: AI generates, you verify and execute
- You are responsible for everything that runs in prod
- Same standards as human-written code
- Creation is fast, verification is your job
- Empowered but responsible

---

## Natural Language Communication

**Talk like a human, not a command prompt**

✅ **Effective**:
```
I need to update disk space alerts from 80% to 85%. We've been getting
too many false positives. I'm not sure if threshold adjustment or
rate-of-change would be better. Current alert in /monitoring/alerts.yaml.
```

❌ **Ineffective**: "Fix disk space alert threshold to 85%"

**Key patterns**:
- Express uncertainty - triggers better explanations
- Provide context (what, why, where)
- Ask AI to teach while doing
- Natural > formal for explanations
- Structured > natural for specifications

---

## The Four Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **SELECT** | Point to relevant info | "Check /terraform/main.tf for AKS config" |
| **WRITE** | Save for later | Build local work item inventory |
| **ISOLATE** | Separate concerns | One tab per helm chart update |
| **COMPRESS** | Context getting full | Generate handoff prompt when needed |

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
Context getting full?       → Generate handoff, new tab
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

**When**: Context usage is getting high or session feels cluttered

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

## Skills Pattern

**What**: Filesystem-based packages combining automation + standards + AI reasoning

**Structure**:
```
.ai-skills/skill-name/
├── SKILL.md              # Metadata + AI instructions
├── standards.yaml        # Team requirements/templates
├── script.py            # Optional automation
└── examples/            # Success/failure cases
```

**When to Use**:
- ✅ Repeated team processes with edge cases
- ✅ Standards enforcement with context
- ✅ Partially automated, partially judgment
- ❌ One-time tasks (just use script)
- ❌ Pure deterministic checks (no AI needed)
- ❌ Generic knowledge (LLM already knows)

**Key Benefits**:
- **Progressive disclosure**: Zero tokens until loaded
- **Composable**: Skills work together through filesystem
- **Versioned**: Git tracks team standards evolution
- **Platform agnostic**: Works with any AI that reads files

**Example Skills**:
- `production-readiness-review`: Validate service meets launch requirements
- `slo-builder`: Generate SLOs based on tier and type
- `helm-values-validator`: Check values against conventions
- `incident-postmortem-generator`: Create postmortem from notes

**The Value Triangle**:
```
Scripts (deterministic) + AI (flexible) + Standards (versioned) = Skills
```

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

## Safety Patterns

**Dry-Run is Mandatory**:
- Every operational script needs `--dry-run` mode
- Test in non-prod before prod
- Show what WOULD happen without doing it

**Progressive Verification Workflow**:
```
Dev → Review → Prod

Dev:     Learn, test logic, fix issues
Review:  Test with realistic data, verify scale
Prod:    Final dry-run, execute with confidence
```

**Script Generation Pattern**:
- AI generates scripts, you review and execute
- Include verbose comments explaining each step
- Peer review like any other code
- Version control operational scripts

**Read vs Execute Boundaries**:
- ✅ AI can READ from production (safe)
- ✅ AI can GENERATE scripts (safe, you review)
- ❌ AI should NOT EXECUTE in production (you execute after review)

---

## MCP Server Evaluation

**Before installing an MCP server, ask:**

**Frequency**:
- [ ] Will I use this daily? (Good candidate)
- [ ] Weekly? (Maybe)
- [ ] Monthly or less? (Probably not worth it)

**Alternatives**:
- [ ] Can AI's built-in tools do this?
- [ ] Can I use CLI + AI assistance instead?
- [ ] Would a local data store work? (create searchable inventories)

**Context Cost**:
- [ ] How many tools does it expose? (1-5 reasonable, 30+ expensive)
- [ ] Do I need ALL of them or just some?
- [ ] Is context cost justified by usage frequency?

**Rule of thumb**: If you can't quantify daily/weekly usage with specific examples, don't install it.

**Audit monthly**: Remove unused servers. Context is precious.

---

## Red Flags

**Context & Communication**:
🚩 Prompts without file paths
🚩 Command-style instead of natural language
🚩 Hiding uncertainty instead of expressing it

**Organization**:
🚩 Mixing 3+ different tasks in one tab
🚩 Starting sessions in root directory
🚩 No handoffs despite many messages
🚩 Asking agent to "remember" from previous sessions

**Data & Tools**:
🚩 Data stores not updated in months
🚩 MCP servers installed "just in case"
🚩 Can't remember when you last used an installed server

**Safety**:
🚩 Running AI-generated scripts without review
🚩 Testing in prod first (or not at all)
🚩 Skipping dry-run testing
🚩 Blind trust in AI outputs

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

**Core Principles**:
- **If you can dream it, you can start it** - Don't self-limit
- **You are accountable** - AI generates, you verify and execute
- **Talk naturally** - Express uncertainty, provide context
- **Tokens are cheap** - Don't over-optimize, provide good context

**Organization**:
- **Isolation beats compression** - Use multiple tabs before compressing
- **One agent, one job** - Separate tabs for separate concerns
- **Be specific** - File paths, not descriptions

**Safety**:
- **Dry-run everything** - Test before executing
- **Dev → Review → Prod** - Progressive verification
- **AI reads and generates, you execute** - Maintain control

**Tools**:
- **Built-in first** - Check native tools before installing MCP servers
- **Context cost matters** - MCP servers consume tokens every conversation
- **Audit monthly** - Remove unused tools and servers

---

## Learn More

**By Module**:
- **Module 1**: Core Concepts - Space Jam, Accountability, Natural Language
- **Module 3**: MCP Servers - When to use, evaluation framework, context cost
- **Module 4**: AI Skills - Package team expertise as discoverable capabilities
- **Module 5**: Multi-Tab Orchestration - One agent per job, orchestrator-worker pattern
- **Module 6**: Patterns and Anti-Patterns - Dry-run, progressive verification, safety, common mistakes

**Quick Access**:
- Full course materials in training repo
- Practice exercises in `workshop-exercises.md`
- Example prompts in `example-prompts.md`

---

**Print this page and keep it handy!**
