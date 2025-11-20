# Context Engineering 101
## Stop Writing Prompts, Start Engineering Context

A practical guide for SREs and DevOps engineers

---

# What is Context Engineering?

**The practice of providing AI assistants with the right information, in the right format**

- Not about writing clever prompts
  - Focus on structure and organization, not prompt tricks
  - Make the AI's job easy by providing clear context
- About building systems that give AI what it needs
  - Reduce ambiguity through intentional structure
  - Let the environment tell the story
  - Create searchable ground truth for consistent answers

**Context engineering is about making the agent's job easy**

---

# Course Overview

**Five focused modules for production engineering teams**

1. **Core Concepts** - Four context strategies and key principles
2. **Filesystem Organization** - Structure as context architecture
3. **MCP Servers** - When and why to use Model Context Protocol
4. **Multi-Tab Orchestration** - Managing multiple specialized agents
5. **Patterns and Anti-Patterns** - Real workflows and critical mistakes

**Duration**: 40 minutes with practical examples throughout

---

# Module 1: Core Concepts

The Four Context Strategies and Key Principles

---

# The Four Context Strategies

**Different ways to provide information to AI**

1. **Inline Context** - Information in the conversation
   - Direct prompts, file contents, code snippets
   - Best for: Specific tasks requiring focused information

2. **Filesystem Context** - Directory structure and organization
   - Logical hierarchy conveys purpose and relationships
   - Best for: Navigating codebases and understanding architecture

3. **Environment Context** - Where you start the session
   - Working directory provides immediate scope
   - Best for: Automatic scoping without explanation

4. **External Context** - APIs and live data sources
   - MCP servers, databases, cloud inventories
   - Best for: Tasks requiring current state or live information

---

# Key Principle: Space Jam Theory

**"If you can dream it, you can do it"**

- Don't self-limit based on perceived complexity
  - Complex tasks are collections of smaller problems
  - AI excels at breaking down and automating parts
- Express uncertainty - it triggers better explanations
  - "I've never used Terraform before, but I need to..."
  - "I'm not sure how Kubernetes secrets work, but..."
- You bring domain knowledge, AI brings generation
  - Together you tackle problems that would take too long manually
  - Amplify your expertise, don't replace it

**Empowerment through AI-assisted exploration**

---

# Key Principle: Accountability

**You are responsible for what runs in production**

- AI generates, you verify
  - Read and understand every change
  - No shortcuts on code review
  - Same rigor as hand-written code
- "AI wrote it" is never an excuse
  - You own what runs under your credentials
  - Maintain your professional standards
  - If you don't understand it, don't run it

**AI can read production. You execute against production.**

---

# Key Principle: Natural Language

**Talk like you're explaining to a knowledgeable colleague**

Be conversational and comprehensive. **Include these elements:**

- **What you're trying to accomplish** - The goal and why
- **What you know and what you're unsure about** - Current understanding
- **What you've already tried** - Eliminate dead ends
- **Where relevant information is located** - Files, directories, docs
- **What success looks like** - Clear exit criteria

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
- Clear hierarchy shows relationships
  - Depth indicates specificity, breadth shows scope
  - Structure teaches without explanation

**The directory path is free, high-quality context**

---

# Example: Poor vs Good Organization

**❌ Poor organization - no context:**
```
/company/
  stuff/
    file1.yaml
    script.sh
    thing.tf
    backup-old.yaml
    test.py
```

**Problems**: No context, unclear relationships, can't tell production from test

**✅ Good organization - clear context:**
```
/company/SRE/
  helm/charts/user-api/
  terraform/azure-infrastructure/
  scripts/backups/
  docs/runbooks/
```

**Benefits**: Clear purpose, easy navigation, implicit context from location

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

**Working directory sets scope automatically**

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

**Monthly audit ritual**: Remove servers unused in 2+ weeks

---

# Module 5: Multi-Tab Orchestration

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

1. **Orchestrator tab** - One tab coordinates overall work
   - Defines tasks for worker tabs
   - Aggregates results and findings
   - Makes final decisions

2. **Worker tabs** - Other tabs do focused, isolated tasks
   - Each handles one specific investigation
   - Work independently without cross-contamination

3. **Summary handoffs** - Workers report back when complete
   - "Here's what I found in the database config"
   - "The Terraform state shows X"

**No mid-work handoffs needed** - Each tab completes its focus area

---

# Module 6: Patterns and Anti-Patterns

Real-world workflows and critical mistakes

---

# Core Safety Pattern: Creation vs Verification

**The fundamental productivity insight**

- **Without AI:** You write (hours) + You verify (minutes) = **Hours total**
- **With AI:** AI writes (minutes) + You verify (same minutes) = **Minutes total**

**Result: 4-7x productivity boost with identical safety**

**Example: Terraform Module**
- Without AI: 2-4 hours creation + 30 min verification = 2.5-4.5 hours
- With AI: 5 min creation + 30 min verification = 35 minutes
- **Time saved: 2-4 hours, safety preserved**

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

---

# Anti-Pattern: The Everything Tab

**One tab trying to do everything at once**

❌ **Anti-pattern**: Single tab handling:
- Investigation + Implementation + Testing + Documentation
- Monitoring + Fixing + Reporting
- Wiki updates + Runbook creation

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
- **MCP audit monthly** - Remove unused servers, reclaim context

**Context engineering is about making the AI's job easy**

---

# Next Steps

**This week - Start small:**
- Try one practical pattern with a real work task
- Implement dry-run flag in one operational script
- Audit your MCP server installations (remove unused)
- Start one session in the correct directory

**This month - Build habits:**
- Practice creation vs verification workflow
- Color-code your tabs consistently
- Use absolute paths in all AI requests
- Build handoff habits for long tasks

**Share learnings with your team**

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
