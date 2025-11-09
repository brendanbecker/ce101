# Module 8: MCP Servers - When and Why

## Learning Objectives

- Understand what MCP servers are and how they work at a technical level
- Recognize when an MCP server adds real productivity value
- Identify when an MCP server is context overhead without benefit
- Make informed decisions about installing and using MCP servers
- Audit and manage your MCP server installations effectively

## What is an MCP Server?

MCP (Model Context Protocol) servers are tools that extend AI assistants with additional capabilities. They act as bridges between the AI and external systems, providing:

- **Access to external APIs and services**: Query Jira, GitHub, cloud providers
- **Custom tools and functions**: Specialized operations not built into the AI
- **Specialized data sources**: Company-specific databases, internal APIs
- **Integration with third-party platforms**: Connect to tools your team uses

Think of them as plugins or extensions for your AI assistant—similar to how browser extensions add capabilities to your web browser.

**The promise**: Install an MCP server and suddenly your AI can directly query your incident management system, update tickets, check deployment status, or access internal documentation.

**The cost**: Every active MCP server consumes context tokens, whether you're using it or not.

## How MCP Servers Work

### Architecture and Protocol

MCP servers operate as **separate processes** that communicate with your AI assistant through a standardized protocol. Here's the technical breakdown:

**Client-Server Model**:
```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│   AI Assistant  │ ◄─────► │  MCP Server  │ ◄─────► │ External System │
│  (Claude Code)  │   MCP   │  (Process)   │   API   │ (Jira, GitHub)  │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

**Communication Flow**:
1. **Startup**: AI assistant starts MCP server process on initialization
2. **Handshake**: Server announces available tools via protocol
3. **Tool Discovery**: AI receives tool schemas and adds them to context
4. **Tool Invocation**: When AI needs to use a tool, it sends request to server
5. **Execution**: Server executes the request against external system
6. **Response**: Server returns results to AI for processing

**Protocol Basics**:
- **JSON-RPC 2.0 based**: Request/response format over stdio or HTTP
- **Standardized methods**: `tools/list`, `tools/call`, `resources/list`, etc.
- **Bidirectional**: Server can request information from client if needed
- **Stateful sessions**: Server maintains state across multiple tool calls

**Tool Schema Format**:
Each tool the server provides is described in context:
```json
{
  "name": "jira_search_issues",
  "description": "Search for Jira issues using JQL query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "jql": {
        "type": "string",
        "description": "JQL query string"
      },
      "maxResults": {
        "type": "number",
        "description": "Maximum number of results to return"
      }
    },
    "required": ["jql"]
  }
}
```

**This entire schema lives in your context window for every conversation.**

### Context Consumption Model

Here's what happens when you have MCP servers installed:

**At Session Start**:
1. AI loads all connected MCP servers
2. Each server announces its available tools
3. Tool schemas are injected into context
4. **Context is consumed before you type a word**

**During Conversation**:
- AI considers all available tools for every response
- Tool descriptions inform AI's decision-making
- Unused tools still consume context
- Multiple servers compound the cost

**Token Cost Example**:

**No MCP servers**:
- Available context: 200k tokens
- Your prompt + files: 20k tokens
- Remaining for conversation: 180k tokens

**With 3 MCP servers (10 tools each)**:
- Tool schemas: ~5k-10k tokens (varies by complexity)
- Your prompt + files: 20k tokens
- Remaining for conversation: 170k-175k tokens

**With 10 MCP servers (50+ tools total)**:
- Tool schemas: ~20k-30k tokens
- Your prompt + files: 20k tokens
- Remaining for conversation: 150k-160k tokens

**Critical insight**: You're paying the context cost for tools you might not use, in every single conversation.

### Server Lifecycle

**Installation**:
- Add server to AI assistant configuration
- Server executable is downloaded or referenced
- Configuration includes: server location, startup arguments, environment variables

**Runtime**:
- Server process starts when AI assistant initializes
- Runs in background throughout session
- Communicates via stdio or local HTTP
- Terminated when AI session ends

**Configuration Example** (Claude Desktop):
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-jira"],
      "env": {
        "JIRA_URL": "https://company.atlassian.net",
        "JIRA_TOKEN": "${JIRA_API_TOKEN}"
      }
    }
  }
}
```

**What this means**:
- Every session spawns these processes
- Configuration is global (all tabs, all sessions)
- You can't easily disable one server for one task
- The tools are always there, always in context

### Technical Implications for SREs

Understanding the architecture helps you make informed decisions:

**Performance considerations**:
- Server startup adds latency to session initialization
- Each tool call involves IPC (inter-process communication)
- Network calls to external APIs add latency
- Multiple servers = multiple processes = more overhead

**Security considerations**:
- Servers have access to credentials (API tokens, etc.)
- AI can invoke tools automatically
- External APIs are called with your credentials
- Audit logs depend on server implementation

**Debugging**:
- Server logs are separate from AI logs
- Tool call failures may not surface clearly
- Network issues can cause mysterious failures
- Credential problems may be hard to diagnose

**This is why intentional installation matters**: You're not just adding a feature, you're adding technical complexity, security surface area, and context overhead.

## The Context Cost Problem

**Every active MCP server consumes context.**

When you have an MCP server connected:
- Its available tools are described in the context
- Tool schemas and parameters take up tokens
- The AI considers these tools for every response
- Multiple servers compound the context usage

**Critical question**: Is the productivity gain worth the context cost?

### Understanding the Trade-off

**Context is finite**:
- Large context windows feel infinite (200k tokens!)
- But complex tasks consume context quickly
- Multiple files, large codebases, long conversations add up
- Tool schemas reduce space for your actual work

**Example scenario**:

You're debugging a complex Kubernetes issue:
- Need to read 10 YAML manifests (~15k tokens)
- Include recent deployment logs (~10k tokens)
- Reference architecture doc (~20k tokens)
- Iterative troubleshooting conversation (~30k tokens)

**Total needed**: ~75k tokens

**With 5 MCP servers installed**: You've lost ~10k-15k tokens to tool schemas you're not using for this task.

**Could that matter?** Yes, if you hit context limits and need to start a new session, losing the troubleshooting context.

### The Compound Effect

One MCP server: Minimal impact
Three MCP servers: Noticeable
Ten MCP servers: Significant context pollution

**Real example**:
- MCP server for Jira: 8 tools
- MCP server for GitHub: 15 tools
- MCP server for AWS: 30+ tools
- MCP server for PagerDuty: 10 tools
- MCP server for database queries: 12 tools

**Total**: 75+ tool schemas in every conversation

**Even if you only use 3 of them regularly.**

### The Decision Framework

**High-value use case**:
```
Context cost: 2k tokens for server with 5 tools
Usage frequency: Daily, 10+ times
Time saved: 5 minutes per use = 50 minutes/day
Alternative: Manual API calls or web UI navigation

Verdict: Worth it
```

**Low-value use case**:
```
Context cost: 3k tokens for server with 10 tools
Usage frequency: Once a month
Time saved: 2 minutes per use
Alternative: Quick web search or single CLI command

Verdict: Not worth it
```

**The principle**: Context is precious. Spend it on tools you use intentionally and frequently.

> ⚠️ **Accountability**: Installing MCP servers without considering context cost is like running services without resource limits—eventually you'll hit constraints and wonder why. Audit your installations and measure actual usage.

## When to Use MCP Servers

### Good Use Cases

**1. Frequent, Repetitive Tasks**

If you're doing something daily that requires external system access:

**Example: Querying your incident management system**
```
Without MCP:
- Open browser
- Navigate to PagerDuty
- Search for incidents
- Copy relevant data
- Paste into AI conversation
- Time: 3-4 minutes per query

With MCP:
- Natural language query in AI
- Results appear automatically
- Time: 30 seconds per query

Usage: 15 times per day during on-call week
Time saved: ~45 minutes per day
Context cost: Acceptable for this frequency
```

**Worth it**: You use this 10+ times per day

---

**2. Complex Integrations You'd Otherwise Manual**

When the alternative is tedious manual work:

**Example: Deployment status across multiple environments**
```
Without MCP:
- SSH to dev cluster
- Run kubectl get deployments -A
- SSH to staging cluster
- Run kubectl get deployments -A
- SSH to prod cluster
- Run kubectl get deployments -A
- Compile results manually
- Time: 10-15 minutes

With MCP:
- Single query: "What's the deployment status across all environments?"
- AI queries each cluster via MCP
- Formatted results in seconds
- Time: 1 minute

Usage: Multiple times daily
Time saved: 10-15 minutes per check
```

**Worth it**: Saves significant time, used frequently

---

**3. Specialized Data Access**

When you need domain-specific data the AI can't access otherwise:

**Example: Internal service catalog or CMDB**
```
Without MCP:
- Open internal wiki
- Search for service information
- Copy details manually
- Paste into AI for analysis
- Repeat for related services
- Time: 5-10 minutes

With MCP:
- AI queries service catalog directly
- Can reason about service dependencies
- Cross-references information automatically
- Time: Immediate

Usage: Daily during planning and troubleshooting
Benefit: Enables AI to answer questions it otherwise couldn't
```

**Worth it**: Enables capabilities that don't exist otherwise

---

### Poor Use Cases

**1. One-Off Tasks**

If you're only using it once or rarely:

**Example: Converting a JSON file to YAML**
```
You could:
- Install format-conversion MCP server
- Convert one file
- Server sits unused for months

Don't need:
- Just paste JSON in AI
- Ask "convert this to YAML"
- Done in 30 seconds

Context cost: Not worth it for single use
Better alternative: Use AI's built-in capabilities
```

**Not worth it**: Context cost exceeds single-use benefit

---

**2. Tasks AI Can Already Do**

When the capability already exists:

**Example: Reading local files**
```
AI can already:
- Use built-in Read tool
- Access any file you point to
- Search file contents
- No additional setup needed

Don't need:
- MCP server that reads files
- Redundant capability
- Wastes context on duplicate functionality

Context cost: Pure waste
Better alternative: Use built-in tools
```

**Not worth it**: Redundant capability, wasted context

---

**3. Rarely-Used "Nice to Haves"**

Features you thought you'd use but don't:

**Example: Weather service integration for on-call planning**
```
Initial thought:
- "I'll check weather during on-call planning"
- "Know if I need to prep for severe weather incidents"

Reality:
- You check weather manually anyway
- Using it maybe once a month
- Forgot it was even installed

Context cost: Every conversation
Usage frequency: Essentially never
```

**Not worth it**: Context cost every conversation for minimal use

---

**4. When Built-in Tools or Scripts Work Fine**

**Example: Checking disk space on servers**

```
MCP server approach:
- Install server-monitoring MCP
- Add authentication configuration
- Tools consume context constantly
- Time saved: Minimal

Shell script approach:
- Write 5-line script with SSH
- Run when needed: ./check-disk.sh
- AI can help write/modify script
- No context overhead

Better choice: Shell script
```

**Not worth it**: Simpler solutions exist

---

**5. When Local Data Stores Work Better**

**Example: Looking up service information**

```
MCP server approach:
- Install CMDB MCP server
- Context cost: 5k tokens
- Live queries every time
- Network dependency

Local data store approach: (See Module 4)
- Export CMDB to JSON quarterly
- Fast local searches
- No context cost
- Works offline

Better choice: Local data store
When live data not critical
```

**Not worth it**: Local alternative is more efficient

## Evaluation Framework

Before installing an MCP server, ask yourself these questions:

### Frequency Questions

- [ ] **Will I use this daily? Weekly? Monthly?**
  - Daily: Strong candidate
  - Weekly: Maybe, depends on time saved
  - Monthly: Probably not worth it
  - "Someday": Definitely not worth it

- [ ] **Is this solving a recurring pain point?**
  - If yes: Quantify how often it hurts
  - If no: Don't install it

- [ ] **Can I quantify how often I'll actually use this?**
  - "All the time" is not a number
  - Track your actual workflow for a week
  - Be honest about usage patterns

### Alternative Questions

- [ ] **Can the AI already do this with built-in tools?**
  - Check Read, Write, Bash, WebFetch capabilities first
  - Many tasks don't need external servers

- [ ] **Is there a simpler CLI tool I could use instead?**
  - `gh` for GitHub
  - `kubectl` for Kubernetes
  - `az` for Azure
  - AI can help you use these tools

- [ ] **Could I create a local data store instead?** (See Module 4)
  - Export data periodically
  - Fast local searches
  - No context cost
  - Better for read-heavy workflows

- [ ] **Could a simple script solve this?**
  - 20-line Python script vs complex MCP server
  - Script is easier to maintain
  - No context overhead

### Value Questions

- [ ] **How much time does this save per use?**
  - 30 seconds: Not significant
  - 5 minutes: Moderate value
  - 15+ minutes: High value
  - Multiply by usage frequency

- [ ] **Does this enable new capabilities or just convenience?**
  - New capabilities: Higher value
  - Convenience: Weigh against context cost
  - Duplication of existing features: Zero value

- [ ] **Am I using this intentionally or just because it's installed?**
  - Intentional use: Good sign
  - "It's there, might as well": Warning sign
  - Can't remember last use: Red flag

### Context Questions

- [ ] **How many tools does this server expose?**
  - 1-5 tools: Reasonable
  - 10-20 tools: Significant cost
  - 30+ tools: Very expensive
  - Question: Do I need ALL of them?

- [ ] **Are the tool descriptions concise or verbose?**
  - Verbose descriptions = more tokens
  - Check tool schemas if possible
  - Some servers are more efficient than others

- [ ] **Do I need ALL the tools it provides, or just some?**
  - If just 1-2 tools from a 20-tool server: Wasteful
  - Consider requesting a minimal server
  - Or using alternative approaches for specific tasks

### The Smell Test

**Rule of thumb**: If you can't immediately justify how this server will improve your daily workflow with specific examples, don't install it.

**Good justification**:
```
"I'm on-call weekly and check PagerDuty 20+ times per shift. The MCP server
will save me 5 minutes per check by eliminating tab switching and copying data.
That's 100+ minutes saved per on-call week."
```

**Bad justification**:
```
"This looks cool and might be useful someday."
```

> ⚠️ **Accountability**: If you can't articulate the specific recurring task this server will improve, you're adding technical debt. Context pollution is real, and it compounds across sessions.

## Managing MCP Servers

### Intentional Use Pattern

**Install when you have a specific, recurring need:**

**Step-by-step process**:

1. **Identify the pain point**
   - What task is tedious or time-consuming?
   - How often does it happen?
   - What's the current manual process?

2. **Verify no built-in solution exists**
   - Can AI already do this?
   - Is there a CLI tool + AI approach?
   - Would a local data store work better?

3. **Install the MCP server**
   - Add to configuration
   - Set up credentials securely
   - Test that it works

4. **Use it intentionally for that purpose**
   - Don't let it become invisible background noise
   - Track whether it's actually saving time
   - Notice if you stop using it

5. **Audit monthly: Still using it? Remove if not.**
   - Regular review of installed servers
   - Be ruthless about removal
   - Context is too valuable to waste

### Audit Your Servers

**Monthly review process**:

```bash
# List installed MCP servers (Claude Desktop example)
cat ~/.claude-code/config.json | jq '.mcpServers | keys'

# Expected output:
# [
#   "jira",
#   "github",
#   "pagerduty",
#   "aws"
# ]
```

**For each server, ask**:

1. **When did I last use this?**
   - This week: Keep
   - This month: Consider usage frequency
   - Can't remember: Remove it

2. **What specific task required it?**
   - Can name specific tasks: Good sign
   - "General purpose": Warning sign
   - Can't remember: Remove it

3. **Could I accomplish this another way now?**
   - Built-in tools improved?
   - Learned better CLI approaches?
   - Local data store would work?

4. **How many of its tools do I actually use?**
   - All of them: Efficient
   - Half of them: Acceptable
   - 1-2 tools: Consider alternatives

**Removal is not failure**:
- You learned the server isn't valuable for your workflow
- Removing it reclaims context
- You can reinstall if needs change

**If you can't remember the last time you used it, uninstall it.**

### Auditing Commands for Different Platforms

**Claude Desktop**:
```bash
# List all MCP servers
cat ~/.config/Claude/claude_desktop_config.json | \
  jq '.mcpServers | keys[]'

# Show full configuration for a server
cat ~/.config/Claude/claude_desktop_config.json | \
  jq '.mcpServers.jira'

# Count total servers
cat ~/.config/Claude/claude_desktop_config.json | \
  jq '.mcpServers | keys | length'
```

**Claude Code CLI**:
```bash
# Check configuration location
ls -la ~/.claude-code/

# Review installed servers
cat ~/.claude-code/config.json | jq '.mcpServers'

# Validate configuration syntax
cat ~/.claude-code/config.json | jq . > /dev/null && \
  echo "Valid JSON" || echo "Invalid JSON"
```

**Server Usage Logging** (if you want to track usage):
```bash
# Create simple logging wrapper
cat > ~/.claude-code/mcp-audit.sh << 'EOF'
#!/bin/bash
# Log MCP server invocations
echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> ~/.claude-code/mcp-usage.log
EOF

# Review usage patterns
cat ~/.claude-code/mcp-usage.log | \
  awk '{print $4}' | sort | uniq -c | sort -rn

# Output shows which servers you actually use:
#  145 jira
#   23 github
#    2 pagerduty
#    0 aws
```

### Task-Specific Installation

**Pattern: Install for specific projects or on-call rotations, then remove**

**On-call week example**:
```bash
# Starting on-call rotation
# Install incident management MCP
echo "Installing PagerDuty MCP for on-call week"
# [Add to config]

# During on-call week
# Use server 20+ times for incident queries
# High value during this period

# End of on-call rotation
# Remove PagerDuty MCP
echo "Removing PagerDuty MCP - on-call rotation complete"
# [Remove from config]
```

**Project work example**:
```bash
# Starting Kubernetes migration project
# Install deployment status MCP
echo "Installing k8s-status MCP for migration project"

# During migration
# Use server frequently to check deployment status across clusters

# Project complete
# Remove deployment status MCP
echo "Removing k8s-status MCP - migration complete"
```

**This keeps context clean when you don't need those capabilities.**

**Benefits**:
- Zero context cost when not needed
- Intentional installation for specific purpose
- Forces re-evaluation of value
- Prevents "forgotten server" problem

## Common Patterns

### Pattern: Task-Specific Servers

Install servers for specific projects or on-call rotations, then remove them:

**On-call rotation**:
```
Week 1 (On-call): Install PagerDuty MCP
- Heavy usage during incidents
- Frequent alert queries
- Team coordination via incident tools

Week 2 (Not on-call): Remove PagerDuty MCP
- Not using incident tools actively
- Context freed for other work
```

**Project-based**:
```
During Terraform migration: Install AWS MCP
- Querying current infrastructure constantly
- Comparing resources across accounts
- High value for specific project

After migration: Remove AWS MCP
- Can use 'aws' CLI with AI help
- Infrequent queries handled manually
- Context better used elsewhere
```

**Security audit**:
```
During security review: Install vulnerability scanner MCP
- Scanning repositories
- Checking dependency versions
- Tracking CVEs

After audit: Remove scanner MCP
- Return to normal development
- Security scans via CI/CD
- No need for constant access
```

This keeps context clean when you don't need those capabilities.

### Pattern: Local Data Instead

Before installing an MCP server for read-only data access, consider creating a local data store (Module 4):

**MCP Server approach:**
```
Pros:
- Live, real-time data
- Always up-to-date
- Direct API access

Cons:
- Context cost every conversation
- Requires server to be running
- Network/API dependency
- Latency on queries
```

**Local data store approach:**
```
Pros:
- No context cost (data read as needed)
- No runtime dependencies
- Works offline
- Fast searches
- You control update frequency

Cons:
- Data may be slightly stale
- Requires periodic refresh
- Storage space (usually minimal)
```

**Decision matrix**:

| Data Type | Refresh Frequency | Best Approach |
|-----------|------------------|---------------|
| Service catalog | Weekly | Local store |
| Incident history | Daily | Local store |
| Current alerts | Real-time | MCP server |
| Deployment status | Real-time | MCP server |
| Team contact info | Monthly | Local store |
| Architecture docs | Weekly | Local store |
| Cloud resources | Daily | Local store |
| Active incidents | Real-time | MCP server |

**Hybrid approach**:
```bash
# Weekly: Export service catalog to local JSON
./export-services.sh > /notes/inventory/services.json

# Daily work: Fast local searches
"Search services.json for all services owned by team-platform"

# When needed: Install MCP for real-time queries
# On-call week: Install PagerDuty MCP for active incidents
```

**Trade-off**: MCP gives you live data, local store gives you context efficiency.

Choose based on whether you need real-time information or can work with periodic snapshots.

> ⚠️ **Accountability**: Don't default to MCP servers because they seem more "complete". Local data stores are often better for your workflow and your context budget. Choose the right tool for the job.

## Red Flags

Warning signs you're misusing MCP servers:

### 1. "I installed this just to try it"

**The scenario**:
```
You: "This MCP server looks interesting!"
You: [Installs server]
You: [Uses it once to try it out]
You: [Forgets about it]
Server: [Consumes context forever]
```

**Why it's a problem**:
- Exploration is fine, but don't leave it installed
- "Just trying it" becomes "permanently installed"
- You forget what's even running

**Fix**: Trial period pattern
```
1. Install server
2. Use it for one week
3. At end of week: Keep or remove
4. Default to remove unless clear value
```

---

### 2. "I might need this someday"

**The scenario**:
```
You: "This weather API MCP could be useful for on-call planning"
You: "I'll install it just in case"
You: [Never actually uses it]
Server: [Wastes context for months]
```

**Why it's a problem**:
- "Might need" = "probably won't need"
- Speculative installation wastes resources
- You can install it when you actually need it

**Fix**: Just-in-time installation
```
When you actually need weather data:
1. Install the server then
2. Use it for specific task
3. Remove when done

Don't pre-install for hypothetical future use
```

---

### 3. "It came with 50 tools but I only use one"

**The scenario**:
```
AWS MCP server provides:
- EC2 tools (15 tools)
- S3 tools (12 tools)
- RDS tools (10 tools)
- Lambda tools (8 tools)
- VPC tools (5 tools)

You only use: S3 bucket listing

Context cost: 50 tool schemas
Value: 1 tool's worth
```

**Why it's a problem**:
- Paying context cost for 49 unused tools
- Inefficient use of context budget
- Alternative approaches likely better

**Fix**: Use targeted alternatives
```
For S3 bucket listing:
- Use 'aws s3 ls' CLI command
- AI can help you format output
- No context overhead
- Same result

Only install full server if you use many tools
```

---

### 4. "I forgot this was even installed"

**The scenario**:
```
You: [Running audit]
You: "Wait, when did I install a Notion MCP server?"
You: "I don't even use Notion anymore"
Server: [Has been wasting context for 6 months]
```

**Why it's a problem**:
- Invisible waste
- Forgotten servers accumulate
- Death by a thousand tool schemas

**Fix**: Monthly audit ritual
```
First Monday of each month:
1. List installed servers
2. Review when last used
3. Remove forgotten servers
4. Keep audit log
```

---

### 5. "The AI keeps suggesting tools I don't want to use"

**The scenario**:
```
You: "Help me investigate this production issue"
AI: "I could use the PagerDuty MCP to create an incident..."
You: "No, I'll do that manually"
AI: "I could use the GitHub MCP to search for similar issues..."
You: "No, just look at the logs I gave you"
```

**Why it's a problem**:
- MCP server tools pollute AI's decision space
- AI considers tools even when not appropriate
- Creates friction in workflow

**Fix**: Remove servers that cause this
```
If AI frequently suggests tools you don't want:
- That server probably isn't valuable to you
- Your workflow doesn't match the tool
- Remove it to reduce noise
```

## Best Practices

### 1. Start Minimal

**Principle**: Install nothing by default

```
New AI assistant setup:
- Don't install MCP servers "just in case"
- Start with zero servers
- Learn the built-in capabilities first
- Discover what you actually need through use
```

**Discovery process**:
```
Week 1-2: No MCP servers
- Learn AI's built-in tools
- Identify friction points
- Note repetitive manual tasks

Week 3: Install first server
- Choose most painful friction point
- Install targeted solution
- Track actual usage

Week 4+: Evaluate and iterate
- Did server solve the problem?
- Using it as expected?
- Keep or remove
```

---

### 2. Measure Usage

**Principle**: Data beats intuition

**Usage tracking approaches**:

**Simple: Mental notes**
```
For each installed server:
- How many times did I use it this week?
- Be honest
- Remove if usage is low
```

**Better: Usage log**
```bash
# Create a simple usage tracker
cat > ~/bin/mcp-log << 'EOF'
#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> ~/.mcp-usage.log
EOF

# When you use a server feature, log it
# This could be manual or automated

# Monthly review
cat ~/.mcp-usage.log | awk '{print $4}' | sort | uniq -c
```

**Best: Automated metrics** (if platform supports)
```
If your MCP server platform has metrics:
- Track tool invocation counts
- Measure latency
- Identify most-used tools
- Data-driven decisions
```

---

### 3. Regular Audits

**Principle**: Installed servers decay in value over time

**Monthly audit checklist**:

```
□ List all installed MCP servers
□ For each server:
  □ When did I last use it?
  □ How many times used this month?
  □ Is it still solving a real problem?
  □ Could I accomplish this another way now?
  □ Does it still justify context cost?
□ Remove unused servers
□ Document removals and reasons
```

**Quarterly deep audit**:
```
□ Review all servers as a portfolio
□ What percentage of tools do I actually use?
□ Are there patterns in what I use vs don't use?
□ Should I consolidate or split servers?
□ Have my needs changed since installation?
```

---

### 4. Document Purpose

**Principle**: If you can't remember why it's installed, you probably don't need it

**Server documentation template**:
```yaml
# ~/.claude-code/mcp-servers.md

## PagerDuty MCP
Installed: 2024-11-01
Purpose: Query incidents during on-call rotations
Usage: Weekly during on-call shifts
Value: Saves 30+ minutes per on-call week
Decision: Keep during on-call rotation, remove otherwise

## GitHub MCP
Installed: 2024-10-15
Purpose: Search issues across all repos
Usage: Daily for cross-repo issue tracking
Value: Enables queries I can't do with 'gh' CLI alone
Decision: Keep - high daily value

## Jira MCP
Installed: 2024-09-10
Purpose: Thought I'd use for ticket queries
Usage: Actually never used it (use web UI instead)
Value: Zero
Decision: REMOVE
```

**Review this document monthly**

---

### 5. Consider Alternatives First

**Decision flowchart**:

```
Need to accomplish task
  |
  ├─> Can AI do with built-in tools?
  |     Yes → Use built-in tools
  |     No → Continue
  |
  ├─> Can I use CLI + AI assistance?
  |     Yes → Use CLI approach
  |     No → Continue
  |
  ├─> Would local data store work?
  |     Yes → Build local inventory
  |     No → Continue
  |
  ├─> Is this high-frequency task?
  |     No → Use manual approach
  |     Yes → Continue
  |
  └─> MCP server might make sense
        └─> Trial period → Evaluate → Keep or remove
```

**Always exhaust simpler options first**

## Example Decision Tree

Visual decision framework for evaluating MCP server installation:

```
┌─────────────────────────────────────┐
│ Need to accomplish task             │
└─────────────┬───────────────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │ Can AI do this with     │ ──Yes──> Use built-in tools
    │ built-in tools?         │          (Read, Write, Bash,
    └─────────┬───────────────┘           WebFetch, etc.)
              │ No
              ▼
    ┌─────────────────────────┐
    │ Will I do this task     │ ──No───> Use one-off solution
    │ frequently?             │          (Manual, script, etc.)
    │ (daily/weekly)          │
    └─────────┬───────────────┘
              │ Yes
              ▼
    ┌─────────────────────────┐
    │ Does this need live/    │ ──No───> Consider local data
    │ real-time data?         │          store (Module 4)
    └─────────┬───────────────┘
              │ Yes
              ▼
    ┌─────────────────────────┐
    │ How many tools does     │
    │ server provide?         │
    └─────────┬───────────────┘
              │
         ┌────┴────┐
         │         │
    1-5 tools  10+ tools
         │         │
         │         ▼
         │    ┌─────────────────────────┐
         │    │ Do I need MOST of       │ ──No───> Find more focused
         │    │ these tools?            │          alternative or use
         │    └─────────┬───────────────┘          CLI approaches
         │              │ Yes
         │              ▼
         └──────────────┤
                        ▼
         ┌──────────────────────────────┐
         │ MCP server probably makes    │
         │ sense                        │
         └──────────────┬───────────────┘
                        │
                        ▼
         ┌──────────────────────────────┐
         │ Install for specific purpose │
         │ Track usage for 2 weeks      │
         │ Audit monthly                │
         └──────────────────────────────┘
```

**Key decision points**:

1. **Built-in capabilities**: Always check first
2. **Frequency**: Daily/weekly = good candidate, monthly = probably not
3. **Real-time requirement**: Determines if local data works
4. **Tool count**: More tools = higher context cost = higher usage bar
5. **Trial period**: Install, measure, decide

**Example walkthrough**:

```
Task: Check GitHub PR status

Built-in tools? No direct GitHub integration
Frequency? Daily, 10+ times
Real-time data? Yes, need current PR status
Tool count? GitHub server has 15 tools
Need most? Yes, use PR status, review, merge, search

Decision: Install GitHub MCP
Trial: 2 weeks
Review: Actually using 8 of 15 tools daily
Verdict: Keep - high value
```

vs.

```
Task: Check service inventory

Built-in tools? No direct access to CMDB
Frequency? Weekly
Real-time data? No, doesn't change often
Alternative? Export CMDB to JSON once a week

Decision: Create local data store instead
Result: Fast searches, no context cost
```

## Key Takeaways

1. **MCP servers are powerful but come with context cost**
   - Every tool schema consumes tokens
   - Multiple servers compound the cost
   - Context is finite, even with large windows

2. **Only install servers you'll use intentionally and frequently**
   - Daily usage: Strong candidate
   - Weekly usage: Maybe
   - Monthly usage: Probably not worth it
   - "Someday": Definitely not

3. **Audit regularly and remove unused servers**
   - Monthly reviews minimum
   - Be ruthless about removal
   - Removal is not failure, it's optimization

4. **Consider alternatives: built-in tools, scripts, local data stores**
   - Many tasks don't need MCP servers
   - CLI + AI is often sufficient
   - Local data stores work great for read-heavy use

5. **Context is precious - spend it wisely**
   - You're budgeting tokens across your workflow
   - Every MCP server is a budget allocation
   - Maximize value per token spent

6. **Task-specific installation keeps context clean**
   - Install for projects or on-call rotations
   - Remove when done
   - Prevents forgotten server accumulation

7. **Measure actual usage, not theoretical benefit**
   - Track how often you actually use servers
   - Data beats intuition
   - Optimize based on reality

**Remember**: Just because you CAN install an MCP server doesn't mean you SHOULD. Be deliberate about what you add to your AI's context.

**The question isn't "Would this be useful?"**

**The question is "Is this useful enough to justify permanent context cost?"**

---

## Exercises

### Exercise 1: Audit Your Current Setup

**Task**: Inventory and evaluate your installed MCP servers

**Steps**:
1. List your currently installed MCP servers
   ```bash
   # Use platform-specific command from "Managing MCP Servers" section
   ```

2. For each server, document:
   - Installation date (if you remember)
   - Original purpose
   - Last time you used it
   - Frequency of use (daily/weekly/monthly/never)
   - Number of tools it provides
   - Number of tools you actually use

3. Decision for each server:
   - **Keep**: High value, frequent use, justifies context cost
   - **Trial**: Keep for 2 weeks, track usage, then decide
   - **Remove**: Low/no usage, context cost not justified

4. Take action:
   - Remove servers marked for removal
   - Set calendar reminder for 2-week trial period reviews
   - Document decisions for future reference

**Expected outcome**: Leaner MCP configuration, reclaimed context

---

### Exercise 2: Alternative Analysis

**Task**: For one task you use an MCP server for, explore alternatives

**Steps**:
1. Pick one MCP server you currently use
2. Identify one specific task you use it for
3. Research alternatives:
   - **Built-in tools**: Can AI do this another way?
   - **CLI approach**: Could you use a CLI tool + AI assistance?
   - **Local data store**: Would periodic export work?
   - **Simple script**: Could a script solve this?

4. Compare approaches:
   ```
   Current MCP approach:
   - Context cost: [tokens]
   - Time per use: [seconds]
   - Setup complexity: [low/medium/high]
   - Maintenance: [ongoing/minimal]

   Alternative approach:
   - Context cost: [tokens]
   - Time per use: [seconds]
   - Setup complexity: [low/medium/high]
   - Maintenance: [ongoing/minimal]
   ```

5. Decision:
   - Keep MCP server? Why?
   - Switch to alternative? Why?
   - Use both? When to use each?

**Expected outcome**: Informed decision about tool choice

---

### Exercise 3: Decision Practice

**Scenario**: You're considering installing an MCP server that integrates with your cloud provider's API.

**Server details**:
- Provides 30 tools
- Covers: compute, storage, networking, databases, monitoring
- Requires API credentials
- You currently use cloud provider CLI (`aws`, `az`, `gcloud`) manually

**Your task**:

1. Walk through the evaluation framework:
   - **Frequency**: How often would you use this?
   - **Alternatives**: What can you already do with CLI + AI?
   - **Value**: How much time would this save?
   - **Context**: 30 tools is significant - need them all?

2. Answer these questions:
   - What specific tasks would benefit from this server?
   - How often do you do those tasks currently?
   - What's your current workflow for those tasks?
   - How much time does current workflow take?
   - Would MCP server save significant time?
   - Which of the 30 tools would you actually use?
   - Is there a more focused alternative?

3. Make a decision:
   - Install: Justify with specific use cases and frequency
   - Don't install: Explain why alternatives are better
   - Conditional: Under what circumstances would you install?

4. If you decided to install:
   - Define trial period duration
   - Set evaluation criteria
   - Plan what metrics you'll track

**Expected outcome**: Practice applying decision framework

---

## Next Steps

**Immediate actions**:
1. Audit your current MCP server installations today
2. Remove at least one unused server
3. Document purpose for remaining servers

**Ongoing practices**:
1. Set monthly calendar reminder for MCP audit
2. Track usage for 2 weeks when installing new servers
3. Default to "no" for new installations until proven necessary

**Further reading**:
- **[Module 4: Local Data Stores](04-local-data-stores.md)** - Alternative to MCP for read-heavy workflows
- **[Module 5: Integration Patterns](05-integration-patterns.md)** - When to use live queries vs local data
- **[Module 7: Common Pitfalls](07-common-pitfalls.md)** - Avoiding MCP-related anti-patterns

---

**Questions or experiences to share?** Bring them to the workshop or add to the discussion thread.

**Remember**: Context engineering is about making intentional choices. MCP servers are powerful tools—use them intentionally.
