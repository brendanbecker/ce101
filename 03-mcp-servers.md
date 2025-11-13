# Module 3: MCP Servers - When and Why

## Learning Objectives

- Understand what MCP servers are and how they work at a technical level
- Recognize when an MCP server adds real productivity value
- Identify when an MCP server is context overhead without benefit
- Make informed decisions about installing and using MCP servers
- Audit and manage your MCP server installations effectively

## What is an MCP Server and How Does it Work?

MCP (Model Context Protocol) servers extend AI assistants with additional capabilities—think of them as plugins for your AI:

- **External API access**: Query Jira, GitHub, cloud providers
- **Custom tools**: Specialized operations not built into the AI
- **Specialized data**: Company databases, internal APIs
- **Third-party integrations**: Connect to tools your team uses

**How they work**: MCP servers run as **separate processes** that communicate with your AI via a standardized protocol:

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│   AI Assistant  │ ◄─────► │  MCP Server  │ ◄─────► │ External System │
│  (Claude Code)  │   MCP   │  (Process)   │   API   │ (Jira, GitHub)  │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

**At session start**: AI loads all configured servers → Each announces its tools → Tool schemas appear in your context

**Context impact**: Tokens are cheap with 200k windows, but forgotten servers accumulate. A few servers (10-30 tools) use 5-10k tokens. Ten servers (50+ tools) might use 20-30k tokens.

**Configuration is global**: All configured servers load in every session.

**Key implications for SREs**:
- **Performance**: Server startup latency, IPC overhead, API call latency
- **Security**: Servers have credentials, AI can invoke tools automatically
- **Debugging**: Server logs separate from AI logs, failures may not surface clearly

## When to Use MCP Servers

**Key principle**: Install when they solve a real, recurring problem. Remove when they don't.

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

### When NOT to Use MCP Servers

**One-off tasks**: Format conversion server for single file → Just paste in AI (30 sec)

**Redundant capabilities**: File-reading MCP when Read tool exists → Wasted context

**Rarely-used "nice to haves"**: Weather API you thought you'd use → Forgot it was installed, monthly use at best

**Simple scripts work fine**: Server monitoring MCP → 5-line `./check-disk.sh` is simpler

**Installing AWS MCP but only using S3**: 50 tools in context, you use 1 → Just use `aws s3 ls` with AI instead

**"Just in case" installations**: Notion/Confluence MCP you never actually use → Wasting context for months

**Can't remember why you installed it**: No clear use case, accumulated cruft → Remove immediately, reinstall if need emerges

---

## SRE-Relevant MCP Servers (2025)

These are MCP servers commonly used by SREs. Evaluate each using the framework above - don't install just because they're listed here.

### High-value for daily use

**Incident management:**
- `pagerduty-mcp` - Query incidents, on-call schedules during rotations
  - **When**: You're on-call weekly or more
  - **Alternative**: PagerDuty web UI + screenshots to AI

**Source control:**
- `github-mcp` or `gitlab-mcp` - PR reviews, issue tracking, repository queries
  - **When**: Managing many repos, frequent PR workflows
  - **Alternative**: `gh` or `glab` CLI + AI (often better)

### Evaluate carefully (high tool count)

**Cloud providers:**
- `aws-mcp`, `azure-mcp`, `gcp-mcp` - 30-50 tools each for cloud resource management
  - **When MCP wins**: Cross-account queries, complex IAM analysis, resource discovery
  - **Alternative**: `aws`, `az`, `gcloud` CLI + AI (usually simpler)
  - **Watch for**: Using 1-2 tools from a 50-tool server → Just use CLI instead

**Kubernetes:**
- `kubernetes-mcp` - Direct cluster queries if managing many clusters
  - **When**: Multi-cluster management, complex queries across namespaces
  - **Alternative**: `kubectl` + AI (faster for single cluster work)

### Specialized/occasional use

**Infrastructure:**
- `terraform-registry-mcp` - Finding and evaluating Terraform modules
  - **When**: Weekly module research, complex dependency analysis
  - **Alternative**: registry.terraform.io + AI analysis

**Monitoring:**
- `grafana-tempo-mcp`, `prometheus-mcp` - Querying metrics and traces
  - **When**: Complex metric analysis, correlation queries
  - **Alternative**: Dashboard screenshots + AI analysis (Pattern 5: Visual Troubleshooting)

**Secrets management:**
- `vault-mcp` - HashiCorp Vault queries
  - **When**: Frequent secret rotation, complex policy management
  - **Alternative**: `vault` CLI + AI

**Browser automation:**
- `playwright-mcp` - Automate web UIs for systems without APIs
  - **When**: Vendor portals, legacy systems, automated screenshot capture
  - **Alternative**: Manual clicking + screenshot to AI for analysis
  - **Install if**: You automate web workflows weekly or more

---

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

**Further reading**: [Module 5: Multi-Tab Orchestration](05-multi-tab-orchestration.md) | [Module 6: Patterns and Anti-Patterns](06-patterns-and-antipatterns.md)
