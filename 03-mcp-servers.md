# Module 3: MCP Servers - When and Why

## Learning Objectives

- Understand what MCP servers are and how they work at a technical level
- Recognize when an MCP server adds real productivity value
- Identify when an MCP server is context overhead without benefit
- Make informed decisions about installing and using MCP servers
- Audit and manage your MCP server installations effectively

## What is an MCP Server?

MCP (Model Context Protocol) servers extend AI assistants with additional capabilities—think of them as plugins for your AI:

- **External API access**: Query Jira, GitHub, cloud providers
- **Custom tools**: Specialized operations not built into the AI
- **Specialized data**: Company databases, internal APIs
- **Third-party integrations**: Connect to tools your team uses

**The promise**: Direct access to external systems from within AI conversations.

**The trade-off**: Servers add tools to your context. This isn't a big deal, but forgotten servers accumulate.

## How MCP Servers Work

MCP servers run as **separate processes** that communicate with your AI via a standardized protocol:

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│   AI Assistant  │ ◄─────► │  MCP Server  │ ◄─────► │ External System │
│  (Claude Code)  │   MCP   │  (Process)   │   API   │ (Jira, GitHub)  │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

**What happens at session start**:
1. AI loads all configured MCP servers
2. Each server announces its available tools
3. Tool schemas appear in your context

**Context impact**: A few servers (10-30 tools) might use 5-10k tokens. Ten servers (50+ tools) might use 20-30k tokens. Not catastrophic with 200k token windows, but worth being aware of.

**Configuration is global**: All configured servers load in every session.

**Key implications for SREs**:
- **Performance**: Server startup latency, IPC overhead, API call latency
- **Security**: Servers have credentials, AI can invoke tools automatically
- **Debugging**: Server logs separate from AI logs, failures may not surface clearly

## When to Use MCP Servers

**Key principle**: Install when they solve a real, recurring problem. Remove when they don't.

The real issue isn't context cost (tokens are cheap). The real issue is accumulating forgotten servers you installed months ago and never use.

### Good Use Cases

**1. Frequent, repetitive tasks requiring external system access**

PagerDuty queries during on-call: 3-4 min manual → 30 sec with MCP, 15x/day = 45 min saved
- **Verdict**: Worth it for 10+ daily uses

**2. Complex multi-step integrations**

Deployment status across 3 clusters: 10-15 min SSH/kubectl workflow → 1 min single query
- **Verdict**: Worth it when manual alternative is tedious

**3. Specialized data the AI can't otherwise access**

Internal service catalog: 5-10 min wiki search → immediate with dependency reasoning
- **Verdict**: Worth it when it enables new capabilities

### Poor Use Cases

**1. One-off tasks**: Format conversion server for single file → Just paste in AI (30 sec)

**2. Redundant capabilities**: File-reading MCP when Read tool exists → Wasted context

**3. Rarely-used "nice to haves"**: Weather API you thought you'd use → Forgot it was installed, monthly use at best

**4. Simple scripts work fine**: Server monitoring MCP → 5-line `./check-disk.sh` is simpler

**5. Local data stores better**: CMDB MCP (live queries) → Quarterly JSON export (fast, offline) when freshness isn't critical

## Evaluation Framework

Before installing, ask:

**Does it solve a real problem?**: Specific recurring task vs "might be useful someday"

**Frequency**: Daily = great | Weekly = fine | Monthly = maybe not | "Someday" = no

**Alternatives**: Built-in tools? | CLI? | Local data? | Simple script?

**Trial it**: Install → Use for 2 weeks → Keep or remove based on actual usage

You're not making a permanent commitment. Just try it and see if it helps.

## Managing MCP Servers

### Installation Pattern

1. Have a specific use case in mind
2. Check if simpler alternatives exist
3. Install and try it for 2 weeks
4. **Clean up periodically—remove what you don't use**

### Periodic Cleanup

```bash
# List servers (look for [mcpServers] section)
grep -A 20 '\[mcpServers\]' ~/.codex/config.toml
```

**Quick audit**:
- Using it regularly? → Keep
- Haven't used it in a month? → Remove
- Can't remember why you installed it? → Remove

You can always reinstall later if you need it again.

### Task-Specific Installation

Install for specific projects/on-call, then remove:

- **On-call rotation**: Install PagerDuty MCP during on-call week → Remove after
- **Project work**: Install AWS MCP during Terraform migration → Remove when done
- **Benefits**: Only have servers installed when you need them

## Local Data vs MCP Servers

For read-only data, consider whether you need live data or if periodic exports work:

| Data Type | Freshness Need | Best Approach |
|-----------|---------------|---------------|
| Service catalog, docs, contact info | Weekly/monthly | Local store |
| Incident history, cloud resources | Daily | Local store |
| Current alerts, active incidents | Real-time | MCP server |

**Local store**: Export to JSON periodically → Fast searches, works offline

**MCP server**: Live queries → Always current

Both are valid. Choose based on whether you need real-time data.

## Red Flags

**1. "Just trying it"**: Installed to explore, forgot about it → **Fix**: One-week trial, default to remove

**2. "Might need someday"**: Installed "just in case" → **Fix**: Just-in-time installation when actually needed

**3. "50 tools, use 1"**: AWS MCP (50 tools) but only S3 listing → **Fix**: Use `aws s3 ls` CLI instead

**4. "Forgot it was installed"**: Notion MCP wasting context for 6 months → **Fix**: Monthly audit ritual

**5. "AI keeps suggesting unwanted tools"**: Friction in workflow → **Fix**: Remove the server

## Best Practices

**1. Start minimal**: Zero servers by default → Learn built-in tools → Install when friction emerges

**2. Measure usage**: Track how often you actually use each server → Data beats intuition

**3. Regular audits**: Monthly review → Remove forgotten/low-use servers → Document decisions

**4. Document purpose**: If you can't remember why it's installed, you don't need it

**5. Alternatives first**: Built-in tools? → CLI? → Local data? → Script? → Only then MCP

## Decision Tree

```
Task → Built-in tools? → Frequent? → Real-time data? → Tool count & usage
         ↓ Yes              ↓ No        ↓ No              ↓ Need most?
    Use built-in      Manual/script   Local store         ↓ Yes
                                                      MCP might work
                                                      → Trial → Audit
```

**Example**: GitHub PR status (daily, 10+ times, 15 tools, use 8) → Install, 2-week trial → Keep
**Example**: Service inventory (weekly, static data) → Export to JSON instead → Fast and offline

## Key Takeaways

1. **MCP servers are plugins for your AI**: They add capabilities by connecting to external systems
2. **Try them when you have a use case**: Daily/weekly tasks that save time → Install and test
3. **Clean up forgotten servers**: The real problem is accumulation, not context cost
4. **Consider alternatives first**: Sometimes built-in tools, CLI, or local data work fine
5. **Task-specific installation works well**: Install for projects/on-call → Remove when done
6. **Not a permanent commitment**: Try it, keep what helps, remove what doesn't

**Don't overthink it. Install, try, clean up periodically.**

---

## Exercises

### Exercise 1: Audit Your Current Setup

List installed servers → For each: last used? frequency? tools used vs provided? → Decision: Keep (high value) | Trial (2 weeks) | Remove (low/no use) → Take action

### Exercise 2: Alternative Analysis

Pick one server → Identify one task → Research alternatives (built-in, CLI, local data, script) → Compare context cost, time, complexity → Decide: keep, switch, or use both contextually

### Exercise 3: Decision Practice

**Scenario**: Cloud provider MCP (30 tools, requires credentials, you use CLI currently)

Apply framework: Frequency? Alternatives with CLI + AI? Time saved? Need all 30 tools? → Make decision with justification → If installing: define trial period and metrics

---

## Next Steps

**Try it**: Find an MCP server that might help with a recurring task → Install → Use for 2 weeks → Keep or remove

**Clean up**: Audit installations periodically → Remove forgotten servers

**Further reading**: [Module 5: Multi-Tab Orchestration](05-multi-tab-orchestration.md) | [Module 6: Patterns and Anti-Patterns](06-patterns-and-antipatterns.md)

---

**Remember**: MCP servers are tools to experiment with. Install what might help, keep what does help, remove what doesn't. Don't overthink it.
