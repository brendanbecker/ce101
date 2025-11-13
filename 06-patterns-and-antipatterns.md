# Module 6: Patterns and Anti-Patterns

Real-world workflows and critical mistakes to avoid when working with AI assistants.

---

## Part 1: Core Safety Patterns

Before diving into specific workflows, let's establish the foundational patterns that make AI-assisted work both powerful and safe.

### The Creation vs Verification Advantage

**The fundamental insight**: Creation is time-consuming. Verification is faster.

Many SRE tasks are hard to create but easier to verify. AI excels at generation, turning hours of writing into minutes. You still verify carefully - that part doesn't change - but you've eliminated the time-consuming creation step.

#### Real Examples with Time Comparisons

**Example 1: Terraform Module**

Task: Write a Terraform module to provision a VPC with public/private subnets, NAT gateways, and route tables.

**Without AI**:
- Create: 2-4 hours of writing, looking up syntax, debugging
- Verify: 30 minutes of testing and review
- **Total: 2.5-4.5 hours**

**With AI**:
- Create: 5 minutes (AI generates code)
- Verify: Still 30 minutes of review and testing
- **Total: 35 minutes**

**Time saved**: 2-4 hours
**Safety preserved**: Same verification process
**Your productivity**: 4-7x increase

**Example 2: Database Migration Script**

**Without AI**: 3.5-4.5 hours total (research, write, test, debug)
**With AI**: 1 hour 40 minutes total (describe requirements, AI generates, review, test)

**Time saved**: 2-3 hours
**Learning bonus**: AI explains patterns you can reuse

#### Why This Works

Verification doesn't require perfect knowledge. You're checking:
- Does this logic make sense?
- Are there obvious security issues?
- Does it handle edge cases?
- Does it work when tested?

These are easier questions than "How do I build this from scratch?"

> ⚠️ **Accountability**: You are responsible for understanding and verifying AI-generated code before deploying it to production. Fast generation doesn't mean fast deployment - maintain your testing and review standards.

---

### The Dry-Run Pattern

**Principle**: Every operational script should have a dry-run mode. This is not optional.

Dry-run is crucial for:
- **Safety**: See what would happen without doing it
- **Learning**: Understand the actions without risk
- **Verification**: Confirm it does what you expect

#### Requesting Dry-Run From AI

✅ **Effective request**:
```
Generate a script that [does the task]. Include:
- A dry-run mode that shows what would happen without making changes
- Verbose output explaining each step
- Comments describing what each section does
```

#### Example: Cleanup Script with Dry-Run

```bash
#!/bin/bash
# Delete old completed pods in staging namespace
# Usage: ./cleanup-pods.sh [--dry-run]

NAMESPACE="staging"
DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "DRY RUN MODE - No pods will be deleted"
fi

# Get completed pods older than 30 days
PODS=$(kubectl get pods -n "$NAMESPACE" \
  --field-selector status.phase=Succeeded \
  -o json | \
  jq -r --arg date "$(date -d '30 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.items[] | select(.status.containerStatuses[0].state.terminated.finishedAt < $date) | .metadata.name')

if [ -z "$PODS" ]; then
  echo "No old completed pods found"
  exit 0
fi

echo "Found pods to delete:"
echo "$PODS"

if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN: Would delete $(echo "$PODS" | wc -l) pods"
  exit 0
fi

# Actually delete pods
for pod in $PODS; do
  echo "Deleting pod: $pod"
  kubectl delete pod "$pod" -n "$NAMESPACE"
done
```

> ⚠️ **Accountability**: Dry-run testing is part of due diligence. Running scripts in production without first testing with dry-run is negligent.

---

### Progressive Verification Workflow

**Pattern**: Dev → Review → Prod

This is how you safely promote new automation through environments, building confidence at each stage.

#### The Three Stages

**Phase 1: Development Environment**
- Learn the task manually
- Have AI generate automation with dry-run
- Test in dev with dry-run first
- Run actual automation in dev
- Verify results thoroughly
- Fix any issues discovered

**Phase 2: Review/Staging Environment**
- Run same automation in review environment
- Verify it works in environment closer to prod
- Test with realistic data volumes
- Refine automation if needed

**Phase 3: Production Environment**
- Run automation in production
- Monitor closely
- Have rollback plan ready
- Document what you learned

> ⚠️ **Accountability**: Skipping progressive verification for high-risk changes is professional negligence. Each stage exists to catch issues before production.

---

### Read vs Execute Pattern

**Safe pattern for production:**

✅ AI can READ from production
✅ AI can GENERATE scripts for production
❌ AI should NOT EXECUTE against production (you execute after review)

#### The Principle: AI Prepares, You Execute

**AI helps you prepare the action. You decide to execute it.**

**The workflow**:
1. AI reads production to understand current state
2. AI generates script/commands to solve the problem
3. You review the generated solution
4. You test in non-prod
5. You execute in production
6. You verify the results

You maintain control and accountability at every step.

> ⚠️ **Accountability**: The boundary between reading and executing is your safety line. AI reads and generates, you review and execute. This pattern keeps you accountable and in control.

---

## Part 2: Practical Patterns

Now let's look at specific workflows for common SRE tasks. These workflows combine the principles above into real-world scenarios.

### Pattern 1: Emergency Rollback

**Use case**: Fast rollback with documentation for post-mortem.

#### Setup

```
Tab 1 (Red): Execute rollback
  - Immediate action
  - Rolling back helm deployment

Tab 2 (Yellow): Document actions
  - Parallel documentation
  - Captures each step taken

Tab 3 (Blue): Investigation
  - Why did we need to rollback?
  - What broke?
```

#### Tab 1: Execution

```
URGENT: Need to rollback user-api deployment

Current version: 2.1.0 (deployed 10 minutes ago)
Previous version: 2.0.3 (stable)
Location: /company/SRE/helm/charts/user-api/

Execute rollback to 2.0.3 now.
Show me each command before running.
```

#### Tab 2: Concurrent Documentation

```
Document rollback in progress:

Time: [timestamp]
Service: user-api
Reason: [paste error messages]
Action: Rolling back 2.1.0 → 2.0.3
Executed by: [your name]

[Keep updating as rollback progresses]
```

#### Tab 3: Post-Rollback Analysis

```
Load the diff between versions 2.0.3 and 2.1.0

Analyze what changed and what likely caused the issue
Look for: configuration changes, dependency updates, code changes in critical paths
```

**Why separate tabs**: Rollback happens urgently in Tab 1. Documentation happens in parallel in Tab 2. Investigation can start immediately in Tab 3 without waiting for rollback completion.

---

### Pattern 2: Parallel Updates with Coordination

**Use case**: Making related changes across multiple repositories or components.

#### Setup: Blue-Green Cluster Swap

**Task breakdown**:
- Update helm chart A
- Update helm chart B (same repo as A)
- Update cluster sync script
- Document all changes

#### Tab Layout

```
Tab 1 (Green):  Helm Chart A
  Location: /company/SRE/helm/charts/
  Task: Update chart A for new cluster

Tab 2 (Green):  Helm Chart B
  Location: /company/SRE/helm/charts/
  Task: Update chart B for new cluster

Tab 3 (Blue):   Sync Script
  Location: /company/SRE/scripts/
  Task: Update cluster-sync.sh to handle helm changes

Tab 4 (Green):  Master Coordination
  Location: /company/SRE/
  Task: Aggregate results and create documentation
```

#### Coordination Workflow

**Step 1**: Work happens in parallel (Tabs 1-3)

**Step 2**: Aggregate in master tab (Tab 4)

```
I've completed these changes:

Chart A: [paste summary from Tab 1]
Chart B: [paste summary from Tab 2]
Sync Script: [paste summary from Tab 3]

Please:
1. Create a comprehensive wiki document for these changes
2. Generate a deployment checklist
3. Identify any dependencies I may have missed
```

**Why it works**: Each tab maintains focused context. Manual aggregation ensures you review all changes before creating final documentation.

---

### Pattern 3: Multi-Repo Investigation

**Use case**: Tracking down issues that span multiple repositories.

#### Scenario

Database connection errors in production. Could be:
- Application code (Dev repo)
- Kubernetes configuration (SRE helm charts)
- Terraform infrastructure (SRE terraform)
- Network policies (SRE ansible)

#### Approach: Fan-Out Investigation

```
Tab 1: Application code
  Location: /company/Dev/user-api/
  Task: Check database connection config and retry logic

Tab 2: Kubernetes config
  Location: /company/SRE/helm/charts/user-api/
  Task: Verify secrets, connection strings, and network policies

Tab 3: Infrastructure
  Location: /company/SRE/terraform/azure-infrastructure/
  Task: Check database firewall rules and network configuration

Tab 4: Network policies
  Location: /company/SRE/ansible/
  Task: Review any recent network policy changes

Tab 5: Aggregation
  Location: /company/SRE/
  Task: Collect findings and determine root cause
```

**Each tab** investigates independently, then reports findings to Tab 5 for synthesis.

---

### Pattern 4: Configuration Validator

**Use case**: Validate changes across all environments before deploying.

#### Setup

```
/company/SRE/helm/charts/my-service/
├── values.yaml (defaults)
├── values/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
```

#### Validation Workflow

```
I'm about to change the resource limits in the my-service helm chart.

Please:
1. Show current resource limits in all environment value files
2. After I make changes, validate that:
   - All environments have consistent structure
   - Production has higher limits than staging
   - No environment is missing required fields
   - All syntax is valid YAML
3. Generate helm template output for each environment to catch any issues
```

**Catches**: Syntax errors, missing overrides, environment inconsistencies

---

### Pattern 5: Visual Troubleshooting

**Use case**: Analyzing complex visual information (dashboards, errors, architectures) using multimodal AI.

#### When Screenshots Beat Text

Your AI assistant can analyze screenshots directly. This is often faster and more accurate than describing visual information in text.

**Common SRE use cases:**
- Grafana/Datadog dashboard analysis
- Kubernetes error messages with formatting
- Cloud console state (Azure Portal, AWS Console)
- PagerDuty incident details
- Architecture diagrams from whiteboards
- Terraform plan output (colored diff)
- Log files with color-coded output

#### The Basic Pattern

**Instead of this:**
```
The dashboard shows the blue line going up from 50 to 200 while the green
line dropped from 100 to 30, and there's a red spike at 14:23...
```

**Do this:**
```
[Paste screenshot of Grafana dashboard]

This dashboard started looking weird 20 minutes ago. I'm not sure what's
normal vs abnormal here. Can you:

1. Identify which metrics look problematic
2. Suggest what correlation I should investigate
3. Point me to which services to check first
```

**Why it works:**
- Faster than describing complex visual relationships
- Preserves visual relationships AI can interpret
- Captures formatting/color/layout that text loses
- Natural for dashboard and error analysis

**Important:** Always combine screenshots with textual context. For example, include what changed recently, which environment, and what you've already tried. A screenshot alone is less effective than screenshot + relevant details.

#### Multi-Tab Visual Workflow Example

Use screenshots across multiple tabs to investigate, fix, and document issues efficiently:

**Tab 1 (Blue): Screenshot Analysis**
```
[Paste screenshot of monitoring dashboard]

Analyze this dashboard. Error rate spiked 30 minutes ago.
What services should I investigate?
```

**Tab 2 (Blue): Deep Investigation**
```
Based on Tab 1, investigating user-api service.
[Screenshot of user-api logs]

These are the logs. What's the root cause?
```

**Tab 3 (Green): Implementation**
```
Implementing fix from Tab 2 investigation.
Update /company/SRE/helm/charts/user-api/values.yaml...
```

**Tab 4 (Yellow): Documentation**
```
Create incident report with embedded screenshots from Tabs 1-2.
Include timeline and visual evidence for post-mortem.
```

**Why this works:** Screenshots flow through the investigation → fix → documentation pipeline. Each tab specializes while building on visual evidence from previous tabs.

#### When NOT to Use Screenshots

**Use text instead when:**
- Copying exact values (IDs, resource names, configuration)
- Security-sensitive information (redact from screenshots or use text)
- Large amounts of structured data (JSON, YAML better as text)
- You need AI to edit the content directly

**Use screenshots when:**
- Visual relationships matter (dashboards, diagrams)
- Formatting is significant (error messages, kubectl output)
- Color-coding conveys meaning (terraform plan, log levels)
- Describing in text would be tedious

#### Security Note

**Be careful with screenshots containing:**
- API keys or tokens
- Internal IP addresses or hostnames (if sensitive)
- Customer data
- Database credentials

Redact sensitive information before pasting or use text-based descriptions instead.

---

> ⚠️ **Accountability**: Screenshots provide visual context for faster analysis, but AI's interpretation is still just a suggestion. You verify the diagnosis and implement fixes following normal safety patterns (dry-run, test in staging, peer review).

---

### Pattern 6: The Handoff Chain

**Use case**: Long-running work that exceeds context window capacity.

#### Handoff Workflow

**Step 1**: When context is getting full, prepare to handoff

```
Give me a handoff prompt I can copy into a new session to continue this work.
```

**Step 2**: Agent generates comprehensive handoff

```
We're migrating the user-api service to the new Kubernetes cluster.

Location: /company/SRE/helm/charts/user-api/
Current branch: feature/cluster-migration

Completed:
- Updated Chart.yaml to version 2.1.0
- Modified values.yaml for new cluster endpoints
- Updated ingress configuration for new domain
- Tested template rendering with helm template

Remaining tasks:
- Update production values override (values/production.yaml)
- Test deployment in staging environment
- Update monitoring dashboards for new cluster
- Document changes in wiki

Key decisions made:
- Using ClusterIP service instead of LoadBalancer (cost optimization)
- Maintaining existing resource limits (no changes needed)

Known issues:
- Staging namespace doesn't exist yet (needs to be created first)

Next immediate action: Create staging namespace, then test deployment.
```

**Step 3**: Copy entire handoff into new session
**Step 4**: Continue work in fresh context

**Why it works**: Agent knows its own context better than you do. It generates comprehensive handoffs automatically.

---

## Part 3: Critical Anti-Patterns

Learn from these mistakes so you don't have to make them yourself.

### Anti-Pattern 1: Vague File References

#### What It Looks Like

```
"Check the config file"
"Update the deployment"
"Look at the logs"
"Fix the terraform"
```

#### Why It Fails

- Agent doesn't know which file you mean
- May find wrong file or guess incorrectly
- Wastes time clarifying
- Results may be for wrong component

#### The Fix

**Always use absolute paths**

```
"Check /company/SRE/terraform/azure-infrastructure/main.tf"
"Update /company/SRE/helm/charts/my-service/values/production.yaml"
"Look at /var/log/my-service/error.log"
```

**Pro Tip**: Use tab completion in terminal, copy the full path, paste into prompt.

---

### Anti-Pattern 2: The Everything Tab

#### What It Looks Like

One terminal tab trying to handle:
- Investigation of production issue
- Implementing the fix
- Testing the fix
- Updating documentation
- Creating work item updates
- Writing post-mortem

#### Why It Fails

- Context becomes cluttered with mixed concerns
- Hard to track what's been done vs. what's remaining
- When you need to handoff, the summary is overwhelming
- Can't parallelize independent work
- Easy to lose focus

#### The Fix

**Use isolation strategy**: One tab per concern

```
Tab 1 (Blue):  Investigation - stays focused on root cause
Tab 2 (Green): Implementation - isolated fix work
Tab 3 (Green): Documentation - aggregates from tabs 1-2
```

**Real Example**:
- Tab 1: "Investigate crashloop in production"
- Tab 2: "Update helm chart based on findings from investigation"
- Tab 3: "Create runbook from investigation and fix"
- Tab 4: "Update work item with details from all above"

---

### Anti-Pattern 3: Blind Trust in AI Outputs

#### What It Looks Like

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
```

#### Why It Fails

**1. AI makes mistakes**
- Can misunderstand requirements
- May miss edge cases
- Sometimes hallucinates functions that don't exist
- Can introduce security vulnerabilities

**2. You're accountable, not the AI**
- "AI wrote the code" is not an acceptable excuse
- Your name is on the commit
- You executed the change
- You are responsible

**3. You miss learning opportunities**
- Blind trust: Copy, deploy, learn nothing
- Understanding: Read, learn, can maintain and modify

#### The Fix

**Apply the same standards as human-written code**

**Verification Checklist**:
```
□ I have read and understand all the code
□ I can explain what it does to a teammate
□ I have tested it in a non-production environment
□ I have verified error handling
□ I have checked for security issues
□ It has passed peer review
□ I have a rollback plan
□ I am confident this is safe to run
```

**If you can't check all boxes, don't run it in production.**

> ⚠️ **Accountability**: You are responsible for everything that runs in production, regardless of who or what wrote it. "AI wrote it" is never an excuse for production incidents.

---

### Anti-Pattern 4: Over-Installing MCP Servers

#### What It Looks Like

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
    "slack": {...}
  }
}
```

You installed them "just to try" or "might need someday."

#### Why It Fails

**1. Context pollution**

Every MCP server consumes context tokens:
- Tool schemas are loaded at session start
- 10 servers with 10 tools each = 100 tool schemas in your context
- That's 20k-30k tokens before you type a single word
- Less room for your actual work

**2. The "might need it someday" trap**

```
You install an AWS MCP server with 50 tools (EC2, S3, RDS, Lambda, VPC).

Reality check:
- You actually use: S3 bucket listing (1 tool)
- Context cost: 50 tool schemas, every session
- Efficiency: Terrible

Or worse:
- Installed a weather API "just in case"
- Last used: During initial testing
- Context cost: Every. Single. Session.
- Actual value: Zero
```

#### The Fix

**Pattern 1: Consider AI Skills first**

Before installing an MCP server, ask: "Could I build a skill instead?"

**AI Skills advantages:**
- **Zero context cost until loaded** - Progressive disclosure vs. MCP's constant overhead
- **Team-specific** - Codify your standards, not generic APIs
- **Version-controlled** - Git tracks changes, no external dependencies
- **Works offline** - No API credentials or network needed

**When to use Skills vs. MCP:**

| Use Case | Solution | Why |
|----------|----------|-----|
| Team troubleshooting process | AI Skill | Zero context cost, captures tribal knowledge |
| Live PagerDuty queries | MCP Server | Real-time external data needed |
| Production readiness checklist | AI Skill | Team standards, occasional use |
| Daily GitHub PR reviews | MCP Server | Frequent external API calls |
| Terraform drift detection | AI Skill | Script + standards, periodic use |
| Continuous Jira updates | MCP Server | Frequent external writes |

**Rule of thumb**: If it's team knowledge or periodic tasks, build a skill. If it's frequent live external data, use MCP.

**Example**: Kubernetes troubleshooting
- ❌ Install k8s MCP server (50+ tools, 15k context tokens, always loaded)
- ✅ Create k8s-troubleshooting skill (0 tokens until used, contains your team's runbook)

**Pattern 2: Intentional installation**

Before installing an MCP server, answer these questions:

1. What specific, recurring task will this solve?
   ❌ "Might be useful"
   ✅ "I check PagerDuty 15+ times during on-call weeks"

2. How often will I actually use it?
   ❌ "Occasionally"
   ✅ "Daily during incident response"

3. Can I accomplish this another way?
   ✅ Build an AI skill instead (Module 4)
   ✅ Check if built-in tools work
   ✅ Consider local data store (Module 3)
   ✅ Evaluate if CLI + AI works instead

**Pattern 3: Monthly audit ritual**

```bash
# First Monday of each month
# List installed servers
cat ~/.claude-code/config.json | jq '.mcpServers | keys'

# For each server, ask:
1. When did I last use this?
   - This week: Keep
   - Can't remember: Remove immediately

2. What specific task required it?
   - Can name tasks: Good sign
   - Can't remember: Remove
```

> ⚠️ **Accountability**: Every MCP server you install consumes context in every session. If you can't justify the context cost with specific, frequent usage, you're wasting resources. Consider AI skills for team knowledge and periodic tasks—they have zero context cost until loaded. Audit monthly. Be ruthless about removal.

**See Module 3: MCP Servers for evaluation framework and Module 4: AI Skills for the zero-context alternative**

---

### Anti-Pattern 5: No Handoff Strategy

#### What It Looks Like

You work in a session until it crashes or becomes unusable. When you start fresh, you lose all context and have to re-explain everything.

#### Why It Fails

- Context window eventually fills
- No way to continue work seamlessly
- Knowledge is lost
- Have to rebuild context from scratch

#### The Fix

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

### Anti-Pattern 6: Starting in Wrong Directory

#### What It Looks Like

```bash
cd /
# Start AI session here

"Update the helm chart"
```

Agent now has to search your entire filesystem to find helm charts.

#### Why It Fails

- Agent lacks context about what you're working on
- Has to guess or ask clarifying questions
- May find wrong files
- Slower and less accurate

#### The Fix

**Navigate first, then start session**

```bash
cd /company/SRE/helm/charts/my-service/
# Start AI session here

"Update resource limits in this helm chart"
```

Agent immediately knows context: SRE work, helm chart, specific service.

---

## Part 4: Key Takeaways and Next Steps

### Most Common Mistakes for Beginners

Master these five first:
1. Vague file references (use absolute paths)
2. Starting in wrong directory (navigate first)
3. Blind trust in AI outputs (verify everything)
4. The everything tab (one tab, one job)
5. No dry-run testing (always dry-run first)

### Next Steps

**This week**:
- Try one practical pattern with a real task
- Implement dry-run in one operational script
- Audit your MCP server installations

**This month**:
- Practice progressive verification on a real deployment
- Build handoff habits when context climbs
- Color-code your tabs for better organization

**Long term**:
- Make verification checklists standard practice
- Build a library of proven patterns
- Share learnings with your team

### Remember

**Context Engineering is about making the agent's job easy.**

If the agent is struggling, confused, or giving poor results - you probably didn't give it enough context. Fix it with more specificity, more file paths, more explanation.

**You are accountable for what runs in production.** AI is a powerful tool for generation, but you own verification, testing, and execution.

---

**[← Back to Multi-Tab Orchestration](05-multi-tab-orchestration.md)** | **[Quick Reference →](quick-reference.md)**
