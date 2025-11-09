# Module 8: MCP Servers - When and Why

## Learning Objectives

- Understand what MCP servers are and how they work
- Recognize when an MCP server adds real productivity value
- Identify when an MCP server is context overhead without benefit
- Make informed decisions about installing and using MCP servers

## What is an MCP Server?

MCP (Model Context Protocol) servers are tools that extend AI assistants with additional capabilities. They act as bridges between the AI and external systems, providing:

- Access to external APIs and services
- Custom tools and functions
- Specialized data sources
- Integration with third-party platforms

Think of them as plugins or extensions for your AI assistant.

## How MCP Servers Work

[TODO: Add technical overview - how they connect, what protocol they use, basic architecture]

Key points:
- They run as separate processes
- Communicate with AI via standardized protocol
- Can be local or remote
- Consume context tokens when active

## The Context Cost Problem

**Every active MCP server consumes context.**

When you have an MCP server connected:
- Its available tools are described in the context
- Tool schemas and parameters take up tokens
- The AI considers these tools for every response
- Multiple servers compound the context usage

**Critical question**: Is the productivity gain worth the context cost?

## When to Use MCP Servers

### Good Use Cases

**1. Frequent, Repetitive Tasks**
If you're doing something daily that requires external system access:
```
Example: Querying your incident management system
- Without MCP: Copy/paste API calls, manual formatting
- With MCP: Natural language queries, structured responses
- Worth it: You use this 10+ times per day
```

**2. Complex Integrations You'd Otherwise Manual**
When the alternative is tedious manual work:
```
Example: Deployment status across multiple environments
- Without MCP: SSH to each env, run commands, compile results
- With MCP: Single query gets all environment status
- Worth it: Saves 15+ minutes every time
```

**3. Specialized Data Access**
When you need domain-specific data the AI can't access otherwise:
```
Example: Internal service catalog or CMDB
- Without MCP: You manually look up and paste information
- With MCP: AI can query and reason about your infrastructure
- Worth it: Enables AI to answer questions it otherwise couldn't
```

### Poor Use Cases

**1. One-Off Tasks**
If you're only using it once or rarely:
```
Example: Converting a JSON file to YAML
- You can: Just paste the JSON and ask AI to convert
- Don't need: Special MCP server for format conversion
- Not worth it: Context cost exceeds single-use benefit
```

**2. Tasks AI Can Already Do**
When the capability already exists:
```
Example: Reading local files
- AI can: Use built-in Read tool
- Don't need: MCP server that reads files
- Not worth it: Redundant capability, wasted context
```

**3. Rarely-Used "Nice to Haves"**
Features you thought you'd use but don't:
```
Example: Weather service integration for on-call planning
- Reality: You check weather manually anyway
- Using it: Maybe once a month?
- Not worth it: Context cost every conversation for minimal use
```

## Evaluation Framework

Before installing an MCP server, ask:

### Frequency Questions
- [ ] Will I use this daily? Weekly? Monthly?
- [ ] Is this solving a recurring pain point?
- [ ] Can I quantify how often I'll actually use this?

### Alternative Questions
- [ ] Can the AI already do this with built-in tools?
- [ ] Is there a simpler CLI tool I could use instead?
- [ ] Could I create a local data store instead? (See Module 4)

### Value Questions
- [ ] How much time does this save per use?
- [ ] Does this enable new capabilities or just convenience?
- [ ] Am I using this intentionally or just because it's installed?

### Context Questions
- [ ] How many tools does this server expose?
- [ ] Are the tool descriptions concise or verbose?
- [ ] Do I need ALL the tools it provides, or just some?

**Rule of thumb**: If you can't immediately justify how this server will improve your daily workflow, don't install it.

## Managing MCP Servers

### Intentional Use Pattern

**Install when you have a specific, recurring need:**
1. Identify the pain point
2. Verify no built-in solution exists
3. Install the MCP server
4. Use it intentionally for that purpose
5. Audit monthly: Still using it? Remove if not.

### Audit Your Servers

Monthly review:
```bash
# List your installed MCP servers
# [TODO: Add actual command based on MCP implementation]

# For each server, ask:
# - When did I last use this?
# - What specific task required it?
# - Could I accomplish this another way now?
```

**If you can't remember the last time you used it, uninstall it.**

## Common Patterns

### Pattern: Task-Specific Servers

Install servers for specific projects or on-call rotations, then remove them:

```
On-call week: Install incident management MCP
Project work: Install deployment status MCP
Security audit: Install vulnerability scanner MCP
```

This keeps context clean when you don't need those capabilities.

### Pattern: Local Data Instead

Before installing an MCP server for read-only data access, consider creating a local data store (Module 4):

**MCP Server approach:**
- Context cost every conversation
- Requires server to be running
- Network/API dependency

**Local data store approach:**
- No context cost (data is read as needed)
- No runtime dependencies
- Works offline
- You control update frequency

**Trade-off**: MCP gives you live data, local store gives you context efficiency.

Choose based on whether you need real-time information or can work with periodic snapshots.

## Red Flags

Warning signs you're misusing MCP servers:

1. **"I installed this just to try it"**
   - Exploration is fine, but don't leave it installed if unused

2. **"I might need this someday"**
   - Install when you need it, not in anticipation

3. **"It came with 50 tools but I only use one"**
   - Paying context cost for 49 unused tools

4. **"I forgot this was even installed"**
   - Time to uninstall

5. **"The AI keeps suggesting tools I don't want to use"**
   - MCP server tools are polluting the AI's decision space

## Best Practices

1. **Start minimal**: Don't install MCP servers until you need them
2. **Measure usage**: Track whether you're actually using what you install
3. **Regular audits**: Monthly review of installed servers
4. **Document purpose**: Know WHY each server is installed
5. **Consider alternatives**: Could a script, alias, or local data work instead?

## Example Decision Tree

```
Need to accomplish task
  |
  ├─> Can AI do this with built-in tools?
  |   └─> YES: Use built-in tools
  |   └─> NO: Continue
  |
  ├─> Will I do this task frequently (daily/weekly)?
  |   └─> NO: Use one-off solution (manual, script, etc.)
  |   └─> YES: Continue
  |
  ├─> Does this need live/real-time data?
  |   └─> NO: Consider local data store (Module 4)
  |   └─> YES: Continue
  |
  └─> MCP server probably makes sense
      └─> Install for specific purpose
      └─> Audit monthly for continued use
```

## Key Takeaways

- MCP servers are powerful but come with context cost
- Only install servers you'll use intentionally and frequently
- Audit regularly and remove unused servers
- Consider alternatives: built-in tools, scripts, local data stores
- Context is precious - spend it wisely

**Remember**: Just because you CAN install an MCP server doesn't mean you SHOULD. Be deliberate about what you add to your AI's context.

---

**Next**: [Common Pitfalls →](../07-common-pitfalls.md)

## Exercises

1. **Audit Exercise**: List your currently installed MCP servers. For each one, document when you last used it and for what purpose. Uninstall any you can't justify.

2. **Alternative Analysis**: Pick one task you use an MCP server for. Can you accomplish it with:
   - Built-in AI tools?
   - A simple shell script?
   - A local data store?
   - Compare effort and context cost.

3. **Decision Practice**: You're considering installing an MCP server that integrates with your cloud provider's API. Walk through the evaluation framework. What questions would you need to answer?

## Additional Resources

[TODO: Add links to MCP documentation, server examples, etc.]
