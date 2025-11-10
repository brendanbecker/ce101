# Context Engineering 101
## Stop Writing Prompts, Start Engineering Context

A practical guide for SREs and DevOps engineers

---

# What is Context Engineering?

**The practice of providing AI assistants with the right information, in the right format**

- Not about writing clever prompts
- About building systems that give AI what it needs
- Focus on structure and organization over prompt engineering tricks
- Make the AI's job easy by providing clear, organized context
- Reduce ambiguity through intentional structure
- Let the environment tell the story

---

# Course Overview

**5 modules designed for SRE teams**

1. **Core Concepts** - Foundational principles and four context strategies
2. **Filesystem Organization** - Structure as context architecture
3. **MCP Servers** - When and why to use Model Context Protocol
4. **Multi-Tab Orchestration** - Managing multiple specialized agents
5. **Patterns and Anti-Patterns** - Real workflows and critical mistakes

---

# Module 1: Core Concepts

The Four Context Strategies

---

# The Four Context Strategies

**Different ways to provide information to AI**

1. **Inline Context** - Information in the conversation
   - Direct prompts, file contents, code snippets

2. **Filesystem Context** - Directory structure and organization
   - Logical hierarchy conveys purpose and relationships

3. **Environment Context** - Where you start the session
   - Working directory provides immediate scope

4. **External Context** - APIs and live data sources
   - MCP servers, databases, cloud inventories

---

# Inline Context

**Information you provide directly in the conversation**

- Prompts and questions you ask
- File contents you share or paste
- Code snippets and error messages
- Documentation excerpts
- Stack traces and log entries
- Configuration values

**Best for**: Specific tasks requiring focused, immediate information

---

# Filesystem Context

**Your directory structure tells a story without words**

- Logical organization creates implicit context
  - Related files grouped together teach relationships
  - Naming patterns establish conventions
- Start sessions in the right place
  - Working directory sets scope automatically
- File names and paths convey meaning
  - `backup-postgres-prod.sh` vs `script.sh`
- Grouping shows relationships
  - `/helm/charts/api/` vs `/random-stuff/`

**Best for**: Navigating large codebases and understanding system architecture

---

# Environment Context

**Where you start matters more than you think**

**Starting in `/company/SRE/helm/charts/my-service/`:**
- AI immediately knows: SRE work, Helm deployment, specific service
- No need to explain what you're working on
- Context is free and automatic
- Questions are scoped to relevant files

**Starting in `/`:**
- AI has no context about your intent
- Has to search entire filesystem to understand scope
- More ambiguity, slower responses
- Higher chance of irrelevant results

---

# External Context

**Live data and runtime information from external sources**

- MCP servers for APIs
  - GitHub repositories and pull requests
  - Jira tickets and Azure DevOps work items
  - Cloud resources (Azure, AWS, GCP)
- Database queries for current state
- Kubernetes cluster resources and status
- Cloud resource inventories and configurations
- Monitoring and observability data

**Best for**: Tasks requiring current state or live system information

**Trade-off**: Higher context cost for persistent availability

---

# Key Principle: Space Jam Theory

**"If you can dream it, you can do it"**

- Don't self-limit based on perceived complexity
  - Unfamiliar tool? AI can guide you through it
  - New language? Learn while building
- AI can help with unfamiliar tools and languages
  - You learn while accomplishing the task
  - Parallel learning and doing
- Express uncertainty - it triggers better explanations
  - "I've never used Terraform before, but I need to..."
  - "I'm not sure how Kubernetes secrets work, but..."

**Empowerment through AI-assisted exploration**

---

# Key Principle: Accountability

**You are responsible for what runs in production**

- AI generates, you verify
  - Read and understand every change
  - No shortcuts on code review
- "AI wrote it" is never an excuse
  - You own what runs under your credentials
  - Maintain your professional standards
- Maintain your testing standards
  - Same rigor as hand-written code
  - No reduced expectations
- Understand before executing
  - If you don't understand it, don't run it

**AI can read production. You execute against production.**

---

# Key Principle: Natural Language

**Talk like you're explaining to a knowledgeable colleague**

Be conversational and comprehensive. **Include these elements:**

- What you're trying to accomplish (the goal)
- What you know and what you're unsure about (your current understanding)
- What you've already tried (eliminate dead ends)
- Where relevant information is located (files, directories, documentation)
- What success looks like (clear exit criteria)

**Uncertainty is valuable** - Saying "I'm not sure about X" triggers explanations

---

# Key Principle: Meeseeks Theory

**"Oooohh! Can Do!" - AI does exactly what you ask**

- The real problem isn't hallucination
  - AI will enthusiastically do precisely what you requested
  - Even if that's not what you actually wanted
- Vague requests get literal (but useless) results
  - "Fix the config" → Which config? How? What's broken?
  - "Update the script" → Which script? Update to do what?
- This is why context engineering matters
  - Clear context = Useful results
  - Vague context = Technically correct but unhelpful

**Be specific about what you want, not just that you want something**

---

# Module 2: Filesystem Organization

Using structure as context architecture

---

# Your Filesystem IS Your Context

**Organize for humans AND AI comprehension**

- Logical grouping by purpose
  - Features together, infrastructure together
  - Clear separation of concerns
- Consistent naming conventions
  - Patterns that AI can recognize
  - Predictable locations for common files
- Clear hierarchy
  - Depth indicates specificity
  - Breadth shows scope
- Separation of concerns
  - Production vs development vs testing

**The structure teaches without explanation**

---

# Example: Poor Organization

```
/company/
  stuff/
    file1.yaml
    script.sh
    thing.tf
    backup-old.yaml
    test.py
```

**Problems:**
- No context about purpose or relationships
- No meaningful organization or hierarchy
- Unclear what's current vs deprecated
- Can't tell production from test
- Forces AI to read every file to understand anything

---

# Example: Good Organization

```
/company/SRE/
  helm/charts/user-api/
  terraform/azure-infrastructure/
  scripts/backups/
  docs/runbooks/
```

**Benefits:**
- Clear purpose from directory names
- Easy navigation and discovery
- Implicit context from location

---

# Starting Location Matters

**Navigate first, then start AI session**

❌ **Anti-pattern**: Start in `/` then ask "update the helm chart"
- AI searches entire filesystem
- Multiple helm charts found - which one?
- Wastes time and context tokens
- Ambiguous intent

✅ **Best practice**: `cd /company/SRE/helm/charts/user-api/` then ask "update resource limits"
- AI knows exactly which chart
- Scoped to relevant files only
- Fast, accurate responses
- Clear intent

**The directory path is free, high-quality context**

---

# File Naming Best Practices

**Be descriptive and consistent - names are documentation**

**Scripts:**
- ✅ `backup-postgres-production.sh` - Clear purpose and target
- ❌ `script.sh` - No information conveyed

**Kubernetes manifests:**
- ✅ `user-api-deployment.yaml` - Service and resource type
- ❌ `deploy.yaml` - Ambiguous

**Infrastructure:**
- ✅ `azure-prod-networking.tf` - Cloud, environment, component
- ❌ `main.tf` - Generic and unhelpful

**Good names prevent questions before they're asked**

---

# Module 3: MCP Servers

When and why to use Model Context Protocol servers

---

# What Are MCP Servers?

**Connections to external systems and APIs**

- GitHub integration
  - Repository access, PR management, issue tracking
- Cloud provider APIs
  - Azure resources, AWS infrastructure, GCP services
- Issue tracking systems
  - Jira tickets, Azure DevOps work items, GitHub Issues
- Databases and data sources
  - Live queries, schema inspection, data analysis

**They extend AI capabilities beyond local files**

**Key consideration**: Every MCP server has a context cost

---

# When to Use MCP Servers

**Install when you have specific, recurring needs**

✅ **Good reasons to install:**
- "I check PagerDuty 15+ times during on-call shifts"
- "I query Azure resources daily for cost analysis"
- "I update Jira tickets constantly throughout my workflow"
- "I review GitHub PRs multiple times per day"

❌ **Bad reasons to install:**
- "Might be useful someday" (then never use it)
- "Want to try it out" (then leave it installed forever)
- "Everyone else has it installed"
- "The demo looked cool"

**Intentional installation beats exploratory accumulation**

---

# The Context Cost

**Every MCP server consumes context tokens at session start**

- Tool schemas loaded before you type anything
  - Each tool has JSON schema describing parameters
  - Multiplies quickly across servers
- 10 servers × 10 tools each = 100 tool schemas
  - That's 20-30k tokens before your first prompt
  - Every single session pays this cost
- Less room for your actual work
  - Fewer tokens for code, documentation, analysis
  - Reduced conversation depth

**Tokens are valuable - don't waste them on unused tools**

**Rule of thumb**: If you haven't used it in 2 weeks, uninstall it

---

# The Audit Pattern

**Monthly review of installed MCP servers**

**For each server, ask yourself:**

1. **When did I last use this?**
   - If more than 2 weeks ago, consider removal
   - One-time use doesn't justify permanent install

2. **What specific task required it?**
   - Can that task be done another way?
   - Is the convenience worth the context cost?

3. **How many tools do I actually use vs. total provided?**
   - Using 2 tools from a 15-tool server?
   - High overhead for low utilization

**Be ruthless about removal** - You can always reinstall later

---

# Alternatives to MCP Servers

**Consider these options before installing MCP servers**

1. **Built-in CLI tools + AI**
   - `kubectl get pods | claude-code "analyze failures"`
   - `az vm list | claude-code "find oversized VMs"`
   - Cheaper context, same result

2. **Local data stores and inventories**
   - Create searchable JSON files of cloud resources
   - Query locally instead of live API calls
   - Update periodically (hourly, daily, weekly)

3. **Manual query + copy/paste**
   - Run query in separate terminal
   - Copy results into AI session
   - Zero persistent context cost

**Often simpler and cheaper than MCP integration**

---

# Module 4: Multi-Tab Orchestration

Managing multiple specialized agents

---

# One Tab, One Job

**Core principle of multi-tab orchestration**

- Each tab has a single, focused purpose
  - Investigation vs implementation vs documentation
  - Read-only analysis vs active changes
- Prevents context clutter
  - No mixing concerns in one conversation
  - Cleaner history for each task
- Enables parallel work
  - Multiple repositories simultaneously
  - Different phases of same project
- Makes handoffs easier
  - Clear task boundaries
  - Simpler context summaries

**Isolation creates clarity and efficiency**

---

# Color Coding System

**Visual identification for quick navigation**

- 🟢 **Green** - Active work, making changes
  - Implementation, editing, building
  - Production changes (after verification)

- 🔵 **Blue** - Read-only investigation and reference
  - Code exploration, log analysis
  - Documentation review, research

- 🟡 **Yellow** - Long-running reference tabs
  - Documentation you refer to repeatedly
  - Standards, patterns, team conventions

- 🔴 **Red** - Urgent, time-sensitive work
  - Incident response, emergency rollbacks
  - Production outages

**One glance tells you the tab's purpose and priority**

---

# The Orchestrator-Worker Pattern

**How to coordinate multiple tabs effectively**

1. **Orchestrator tab** - One tab coordinates the overall work
   - Defines tasks for worker tabs
   - Aggregates results and findings
   - Makes final decisions

2. **Worker tabs** - Other tabs do focused, isolated tasks
   - Each handles one specific investigation or implementation
   - Work independently without cross-contamination

3. **Summary handoffs** - Workers report back when complete
   - "Here's what I found in the database config"
   - "The Terraform state shows X"

4. **Result coordination** - Orchestrator synthesizes insights
   - Combines findings from all workers
   - Determines root cause or next steps

**No mid-work handoffs needed** - Each tab completes its focus area

---

# Example: Multi-Repo Investigation

**Scenario: Database connection errors in production**

```
Tab 1 (Blue): Application code repository
  → Check connection string configuration
  → Review connection pool settings

Tab 2 (Blue): Kubernetes manifests
  → Verify database secrets are current
  → Check network policies for database access

Tab 3 (Blue): Terraform infrastructure
  → Check database firewall rules
  → Verify NSG allows application subnet

Tab 4 (Blue): Network policy repository
  → Review recent policy changes
  → Check for overly restrictive rules

Tab 5 (Green): Orchestrator - Root cause analysis
  → Aggregate findings from all tabs
  → Determine fix and coordinate implementation
```

---

# Natural Language for Workers

**Provide rich context when starting worker tabs**

**Essential elements to include:**

- **Task description**: "Investigate why connections to Postgres are failing"
- **Starting location/directory**: `/company/SRE/kubernetes/api-service/`
- **Relevant files**: "Focus on secrets.yaml and deployment.yaml"
- **What you're trying to accomplish**: "Determine if credentials or network config changed"
- **Success criteria**: "Find connection string or confirm it hasn't changed in 2 weeks"

**Give workers everything they need upfront**

**Why this matters**: Workers can complete tasks autonomously without back-and-forth

---

# Git Worktrees for Parallel Work

**Work on same repository in multiple tabs simultaneously**

```bash
# Main repository location
cd /company/SRE/helm/charts/

# Create worktrees for parallel work
git worktree add ../charts-worktree-feature-a feature-a
git worktree add ../charts-worktree-feature-b feature-b

# Now you have:
# Tab 1: /company/SRE/helm/charts/ (main)
# Tab 2: /company/SRE/helm/charts-worktree-feature-a/
# Tab 3: /company/SRE/helm/charts-worktree-feature-b/

# Each tab can work independently without conflicts
```

**Clean up when done:**
```bash
git worktree remove ../charts-worktree-feature-a
```

---

# Session Resume

**Preserve context across days or weeks**

- Session history is valuable
  - Contains your discoveries and decisions
  - Documents the reasoning behind changes
  - Preserves investigative dead-ends (saves re-exploring)

- Resume when you need to continue work
  - Pick up multi-day projects seamlessly
  - Maintain context for related follow-up tasks

- Don't resume when you need a fresh start
  - New, unrelated task
  - Context is polluted with irrelevant history
  - Starting over is cleaner

**Session history serves both AI memory and human documentation**

---

# Module 5: Patterns and Anti-Patterns

Real-world workflows and critical mistakes

---

# Core Safety Pattern: Creation vs Verification

**The fundamental productivity insight**

- **Without AI:** You write (hours) + You verify (minutes) = **Hours total**
- **With AI:** AI writes (minutes) + You verify (same minutes) = **Minutes total**

**Result: 4-7x productivity boost with identical safety**

**The key insight**: Verification time is constant regardless of who creates. AI eliminates the creation bottleneck while you maintain quality control.

**You shift from**: Manual creator → Expert verifier

---

# Core Safety Pattern: Dry-Run Everything

**Mandatory for operational scripts**

**Every operational script must have:**
- `--dry-run` flag that's easy to use
- Clear output showing what WOULD happen
  - "Would delete 47 log files older than 30 days"
  - "Would restart 3 pods: api-1, api-2, api-3"
- Same code path as real execution
  - Dry-run uses identical logic, just skips execution
  - Catches bugs before production impact

**Example:**
```bash
./cleanup-old-logs.sh --dry-run
./restart-pods.sh --dry-run --namespace=production
```

**Running production scripts without dry-run testing is professional negligence**

---

# Core Safety Pattern: Progressive Verification

**Dev → Staging → Production deployment pipeline**

**Phase 1: Development environment**
- Learn the task requirements
- Generate automation with AI
- Verify with dry-run
- Fix issues in safe environment
- Iterate until confident

**Phase 2: Staging environment**
- Test in production-like conditions
- Realistic data volumes and configurations
- Identify environment-specific issues
- Final dry-run verification

**Phase 3: Production execution**
- One more dry-run with production context
- Monitor closely during execution
- Rollback plan ready and tested
- Document what happened

---

# Core Safety Pattern: Read vs Execute

**Safe boundaries for production access**

✅ **AI can READ from production**
- Log files, configurations, resource state
- No risk to running systems
- Accelerates troubleshooting

✅ **AI can GENERATE scripts and changes**
- Automation, fixes, configurations
- You review before execution
- Maintains accountability

❌ **AI should NOT EXECUTE against production**
- You execute after thorough review
- You understand what's happening
- You're accountable for the outcome

**AI prepares, you verify and execute**

---

# Practical Pattern: Emergency Rollback

**Fast rollback with parallel documentation**

```
Tab 1 (Red): Execute rollback
  → Immediate action to restore service
  → Run verified rollback procedure
  → Monitor recovery metrics

Tab 2 (Yellow): Document actions in real-time
  → Timestamp every action
  → Capture commands executed
  → Note any unexpected behavior

Tab 3 (Blue): Root cause investigation
  → What triggered the need for rollback?
  → Analyze logs and recent changes
  → Prepare incident report data
```

**Separate concerns enable parallel work during incidents**

**Post-incident**: Tab 2 provides timeline for postmortem

---

# Practical Pattern: Configuration Validator

**Validate consistency across all environments**

**Before deploying configuration changes:**

1. Show current values in all environments (dev, staging, prod)
2. Validate consistent structure across environments
3. Check production has higher resource limits than staging
4. Verify no missing required fields
5. Generate helm template output for each environment
6. Diff outputs to confirm only intended changes

**Example:**
```bash
# AI generates this validation script
./validate-config.sh --env=all --show-diff
```

**Catches configuration drift and errors before they reach production**

---

# Practical Pattern: The Handoff Chain

**Continue work seamlessly in fresh context**

**When context fills up (typically 40-60% full):**

1. Ask: "Give me a handoff prompt for a new session"
2. AI generates comprehensive summary including:
   - What you've accomplished so far
   - Current state and decisions made
   - What still needs to be done
   - Relevant file locations and context
3. Copy handoff prompt to new session
4. Continue seamlessly with fresh token budget

**Why this works**: The AI understands its own context better than you do

**Pro tip**: Don't wait until 100% - handoff early for smoother transitions

---

# Anti-Pattern: Vague File References

**Always use absolute paths in requests**

❌ **Vague references (ambiguous, slow):**
- "Check the config file" - Which one?
- "Update the deployment" - Which deployment?
- "Look at the logs" - Where are they?

✅ **Absolute paths (precise, fast):**
- "Check `/company/SRE/terraform/azure/main.tf`"
- "Update `/company/SRE/helm/charts/api/values/prod.yaml`"
- "Look at `/var/log/api-service/error.log`"

**Benefits:**
- Zero ambiguity about which file
- AI doesn't waste time searching
- Faster, more accurate responses
- No back-and-forth clarification

---

# Anti-Pattern: The Everything Tab

**One tab trying to do everything at once**

❌ **Anti-pattern**: Single tab handling:
- Investigation + Implementation
- Testing + Documentation
- Wiki updates + Runbook creation
- Monitoring + Fixing + Reporting

**Problems:**
- Context pollution - unrelated history mixed together
- Can't resume specific tasks cleanly
- Hard to handoff parts to colleagues
- Difficult to track what's done vs in-progress

✅ **Best practice - Separate tabs:**
- Tab 1 (Blue): Investigation and analysis
- Tab 2 (Green): Implementation and fixes
- Tab 3 (Blue): Documentation and runbooks

**One tab, one job - always**

---

# Anti-Pattern: Blind Trust

**AI is powerful but not infallible**

❌ **Dangerous trust approaches:**
- Run scripts without reading them
- Skip peer review because "AI wrote it"
- Deploy without testing in non-prod
- "AI wrote it so it must be fine"

✅ **Professional verification approaches:**
- Read and understand all generated code
  - If you don't understand it, don't run it
- Test in non-prod environments first
  - Same rigor as hand-written code
- Maintain normal code review standards
  - AI-generated code gets reviewed like any other
- You own what runs in production
  - "AI wrote it" is never an excuse

**Your expertise validates AI output, not replaces your judgment**

---

# Anti-Pattern: Over-Installing MCP Servers

**Context pollution from unused tools**

❌ **Anti-pattern**: Installing "just to try" then forgetting
- Accumulate 10+ servers over time
- Use 2-3 regularly, 7+ never
- Pay 30k token cost every session
- Reduced space for actual work

✅ **Intentional installation strategy:**
- Specific, recurring task identified first
  - "I need to query Azure daily"
- Actually used weekly (minimum)
  - If not, it doesn't justify the cost
- Context cost explicitly considered
  - Is convenience worth permanent token tax?

**Monthly audit ritual**: Remove servers unused in 2+ weeks

**Remember**: Uninstalling is easy, context waste is permanent

---

# Anti-Pattern: No Handoff Strategy

**Context fills up, lose all work progress**

❌ **Anti-pattern**: Work until context crashes
- Session hits 100% context limit
- Forced to start completely from scratch
- Lose investigation history and decisions
- Repeat work unnecessarily

✅ **Proactive handoff at 40-60% context:**
- Generate handoff prompt before crisis
- Start fresh session with full context
- Seamless continuation with room to work
- Preserve all decisions and discoveries

**Handoff prompts are better than human summaries**
- AI knows exactly what's relevant
- Includes file paths and specific details
- Captures reasoning and dead-ends explored

---

# Anti-Pattern: Starting in Wrong Directory

**Location provides free, high-quality context**

❌ **Anti-pattern**: Start in `/` then ask "update helm chart"
- AI must search entire filesystem
  - Thousands of files to consider
- Likely finds multiple helm charts
  - Which one do you mean?
- Slower responses, more ambiguity
  - Extra clarification rounds needed
- Wastes context tokens on search

✅ **Best practice**: Navigate first, then ask
```bash
cd /company/SRE/helm/charts/user-api/
# NOW start AI session and ask:
# "update resource limits to match new instance size"
```
- AI knows exactly which chart
- Scoped to relevant files immediately
- Fast, precise responses
- Context tokens used for work, not search

---

# The Productivity Multiplier

**When you combine these core patterns**

**Creation vs Verification** (4-7x faster creation)
+
**Dry-Run Everything** (catch errors before production)
+
**Progressive Verification** (dev → staging → prod safety)
+
**Read vs Execute** (AI prepares, you control execution)

= **4-7x productivity without sacrificing safety**

**The critical insight**: Verification time is constant

**What changes**: AI eliminates creation bottleneck while you maintain quality control

**You shift from**: Manual creator → Expert verifier

---

# Most Common Mistakes for Beginners

**Master these five first - highest impact fixes**

1. **Vague file references**
   - Use absolute paths always

2. **Starting in wrong directory**
   - Navigate before starting session

3. **Blind trust in AI outputs**
   - Verify everything, maintain review standards

4. **The everything tab**
   - One tab, one job - always

5. **No dry-run testing**
   - Mandatory for operational scripts

**Fix these five, see immediate productivity gains**

---

# Key Takeaways

**Stop writing prompts, start engineering context**

- **One agent, one job** - Use multiple tabs for complex work
- **Filesystem is context** - Organize logically, start in the right place
- **Tokens are cheap, clarity is expensive** - Use isolation over compression
- **You are accountable** - AI generates, you verify and execute
- **Dry-run everything** - Safety is mandatory, not optional
- **Progressive verification** - Dev → Staging → Production always

**Context engineering is about making the AI's job easy**

---

# Next Steps

**This week - Start small:**
- Try one practical pattern with a real work task
- Implement dry-run flag in one operational script
- Audit your MCP server installations (remove unused)
- Start one session in the correct directory

**This month - Build habits:**
- Practice progressive verification (dev → staging → prod)
- Build handoff habits (don't wait for 100% context)
- Color-code your tabs consistently
- Use absolute paths in all AI requests

**Share learnings with your team**

---

# Additional Resources

**Course materials available:**
- **Quick Reference Card** - One-page cheat sheet for daily use
- **Workshop Exercises** - Hands-on practice activities
- **Example Prompts** - Copy-paste starting points for common tasks

**Best way to learn: Practice on real work**
- Start with small, low-risk tasks
- Build habits incrementally
- Share patterns that work with teammates
- Iterate and refine your approach

**Context engineering is a practice, not a destination**

---

# Remember

**Context Engineering is about making the agent's job easy**

**If the agent is struggling or giving poor results:**
- You probably didn't provide enough context
- Add more specificity, more file paths, more explanation
- Describe what you know AND what you're unsure about
- Show examples of what you want

**Like managing humans: clear communication = good results**

**Unlike managing humans: AI never gets tired of detailed context**

---

# Questions?

Thank you for attending Context Engineering 101

**Ready to get started?**

Apply these principles to your work this week

Start engineering context, not writing prompts
