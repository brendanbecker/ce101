# Module 4: AI Skills

Package team expertise as discoverable, composable capabilities that AI assistants can load on-demand.

---

## The Problem

Your team has expertise, but it's scattered:

- **In people's heads** - Not accessible to everyone
- **In stale documentation** - Wiki pages from 2 years ago
- **In scripts that can't explain** - They execute but don't teach
- **Not enforced** - Just "tribal knowledge"

**What you need**: A way to package team standards that is discoverable, self-documenting, composable, executable, versioned, and loads progressively.

---

## What Are AI Skills?

### Defining a Skill

A **skill** is a filesystem-based package containing:
- **Metadata**: What the skill does (YAML frontmatter in SKILL.md)
- **Instructions**: How the AI should use it (SKILL.md content)
- **Standards**: Team conventions, schemas, checklists (YAML/JSON files)
- **Automation**: Optional executable scripts (Python, Bash, etc.)
- **Examples**: Reference implementations

**Structure**:
```
.ai-skills/skill-name/
├── SKILL.md                # Metadata + AI instructions
├── standards.yaml          # Team requirements/templates
├── check-script.py        # Optional automation
└── examples/              # Success/failure cases
```

### Progressive Disclosure

**The insight**: AI assistants have unlimited potential context but limited actual tokens.

**How skills solve this**:
```
1. AI reads metadata (50 tokens): "production-readiness-review - Validates services"
2. User asks about production readiness
3. AI loads full skill (5000 tokens): Complete checklist, automation, examples
4. AI applies skill to user's service
```

**Result**: Zero tokens most of the time, full context when relevant.

### The Value Triangle

```
         Scripts
      (Deterministic)
            /\
           /  \
          /    \
         /      \
        /________\
    AI           Team Standards
(Flexible)       (Versioned)
```

**Skills combine all three**:
- Scripts provide deterministic validation
- AI provides flexible reasoning and explanation
- Standards provide versioned team knowledge

---

## Example Skill Ideas

### Production Readiness Review

Validates services meet production launch requirements.

**Contains**:
- `prr-requirements.yaml`: Team's checklist organized by category (monitoring, security, reliability, docs, observability)
- `check-prr.py`: Automated validation of Kubernetes resources, required files, security contexts
- Instructions for AI on interpreting results in context (tier-based requirements, service-type exceptions)

**AI adds value**: Explains what failures mean, suggests remediation, identifies when exceptions are reasonable.

---

### Kubernetes Pod Troubleshooting

Systematic pod failure diagnosis following team runbook patterns.

**Real-world problem:** Every SRE troubleshoots pods differently. Codify your team's diagnostic approach so AI can apply it consistently.

**Skill structure:**
```
.ai-skills/k8s-troubleshooting/
├── SKILL.md              # Metadata + AI instructions
├── diagnostic-tree.yaml  # Decision tree for common failures
├── check-pod.sh         # Automated diagnostic gathering
└── examples/
    ├── crashloop.md
    ├── oomkilled.md
    └── imagepullbackoff.md
```

**diagnostic-tree.yaml example:**
```yaml
symptoms:
  CrashLoopBackOff:
    checks:
      - name: Application error in logs
        command: kubectl logs {pod} --previous
        look_for: "Exception|Error|panic|Fatal"
        rationale: "Previous container logs show why it crashed"

      - name: Liveness probe failing
        command: kubectl describe pod {pod}
        look_for: "Liveness probe failed"
        rationale: "App running but health check endpoint failing"

      - name: Missing dependencies
        look_for: "connection refused|timeout|ECONNREFUSED"
        rationale: "App can't reach database or other service"

  OOMKilled:
    checks:
      - name: Memory limits too low
        command: kubectl describe pod {pod}
        look_for: "OOMKilled"
        rationale: "Container exceeded memory limit"

      - name: Memory leak pattern
        guidance: "Check if restarts correlate with pod uptime"
        rationale: "Leak causes gradual memory growth until OOM"

      - name: Actual memory usage
        command: kubectl top pod {pod}
        rationale: "Compare actual usage to limits"

  ImagePullBackOff:
    checks:
      - name: Image exists
        command: kubectl describe pod {pod}
        look_for: "Failed to pull image|manifest unknown"
        rationale: "Image name typo or doesn't exist in registry"

      - name: Registry authentication
        look_for: "unauthorized|authentication required"
        rationale: "Image pull secret missing or invalid"
```

**SKILL.md includes:**
```markdown
## AI Instructions

When troubleshooting a pod:
1. Identify the symptom (CrashLoopBackOff, OOMKilled, etc.)
2. Load the appropriate section from diagnostic-tree.yaml
3. Run checks in order, explaining what each check reveals
4. Stop when root cause is identified
5. Suggest fix with rationale from the tree
6. Reference relevant example from examples/ directory

Always explain WHY each check matters, not just WHAT it shows.
```

**Example usage:**
```
"Use the k8s-troubleshooting skill to diagnose auth-service crashlooping"

AI walks through diagnostic tree:
1. Checks previous logs → finds ECONNREFUSED to postgres:5432
2. Verifies database service → postgres endpoints are empty
3. Identifies root cause: Database pods are down
4. Suggests remediation from team's decision tree
```

---

### Terraform State Drift Detection

Detect and explain infrastructure drift between Terraform state and actual cloud resources.

**Real-world problem:** Manual changes to cloud resources cause Terraform state drift, leading to mysterious failures on next apply.

**Skill structure:**
```
.ai-skills/terraform-drift/
├── SKILL.md
├── drift-checks.yaml     # What to check for each resource type
├── detect-drift.py      # Automated state comparison
└── remediation-guide.md  # How to fix common drift scenarios
```

**drift-checks.yaml example:**
```yaml
resource_types:
  azurerm_kubernetes_cluster:
    critical_fields:
      - kubernetes_version
      - default_node_pool.0.node_count
      - default_node_pool.0.vm_size
    warning_fields:
      - tags
    rationale: "Version/size drift breaks infrastructure assumptions"
    common_causes:
      - "Manual upgrade through Azure Portal"
      - "Auto-scaling changed node count"

  azurerm_storage_account:
    critical_fields:
      - account_tier
      - account_replication_type
      - min_tls_version
    warning_fields:
      - tags
    sensitive: true  # May contain connection strings
    rationale: "Storage tier affects cost and performance guarantees"

  azurerm_postgresql_server:
    critical_fields:
      - sku_name
      - storage_mb
      - ssl_enforcement_enabled
    warning_fields:
      - backup_retention_days
    rationale: "Database config affects availability and data safety"
    common_causes:
      - "DBA made emergency changes during incident"
      - "Auto-scaling adjusted storage"
```

**detect-drift.py features:**
- Compares `terraform show` output to `terraform plan`
- Categorizes drift: critical, warning, cosmetic
- Outputs structured report for AI to interpret

**AI interprets results:** Explains drift in business context, prioritizes by impact, suggests remediation from team's guide.

---

### Helm Values Validator

Validates Helm values files against team conventions.

**Skill structure:**
```
.ai-skills/helm-validator/
├── SKILL.md
├── conventions.yaml      # Team standards
├── validate-values.py   # Automated checks
└── examples/
    ├── good-values.yaml
    └── bad-values.yaml
```

**conventions.yaml example:**
```yaml
required_fields:
  - replicaCount
  - image.repository
  - image.tag
  - resources.requests.cpu
  - resources.requests.memory
  - resources.limits.cpu
  - resources.limits.memory

naming_conventions:
  image_tag:
    pattern: "^v?[0-9]+\\.[0-9]+\\.[0-9]+$"
    rationale: "Semantic versioning only, no 'latest'"

resource_limits:
  memory_ratio:
    rule: "limits.memory >= 1.2 * requests.memory"
    rationale: "Buffer for memory spikes"
  cpu_ratio:
    rule: "limits.cpu >= requests.cpu"
    rationale: "Allow burst capacity"

security_checks:
  - name: No plaintext secrets
    check: "No 'password' or 'secret' keys in values files"
    rationale: "Use sealed-secrets or external-secrets"

  - name: Security context required
    check: "securityContext.runAsNonRoot = true"
    rationale: "Containers should not run as root"

environment_consistency:
  - name: Production has higher limits
    check: "prod limits >= staging limits >= dev limits"
    rationale: "Prevent resource contention in production"
```

**AI adds value**:
- Explains conventions and why they exist
- Suggests fixes that comply with team standards
- Handles edge cases ("service-mesh sidecar exempt from memory limits")
- Validates across all environment value files

---

### Dockerfile Security Scanner

Checks Dockerfiles for security issues and best practices.

**Checks**: No `latest` tag, non-root user, no secrets in ENV, multi-stage builds, health checks, minimal base images.

**AI adds value**: Explains security implications, suggests refactoring, provides secure pattern examples from team standards.

---

### Incident Postmortem Generator

Creates postmortem documents from incident notes.

**Creates**: Timeline, root cause analysis, impact assessment, action items, lessons learned.

**AI adds value**: Structures messy notes, identifies root causes, generates actionable remediation.

---

## When to Use Skills

### Skills vs. Scripts

| Scenario | Use |
|----------|-----|
| One-time automation | Script |
| Repeated process with edge cases | Skill |
| Pure deterministic check | Script |
| Needs context and explanation | Skill |

### Skills vs. MCP Servers

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| Context cost | Zero until loaded | Constant |
| Best for | Team processes | Live external data |
| Versioning | Git | External system |

**Rule**: If you explain the same team standards repeatedly, codify them as a skill.

---

## Building Your Own Skills

### Quick Guide

**1. Identify the need**
- You repeatedly explain team standards
- Script exists but needs context to interpret
- Process is partially automated, partially judgment

*Keep skills focused*: "production-readiness-review" not "infrastructure-automation". One job per skill.

**2. Create structure**
```bash
mkdir -p .ai-skills/skill-name/{examples,scripts}
```

**3. Write SKILL.md**
```markdown
---
name: skill-name
description: One-line description
version: 1.0.0
category: operations
tags: [relevant, keywords]
---

## Purpose
Why this exists

## When to Use
Specific scenarios

## AI Instructions
How AI should use this skill
```

**4. Add standards file**
```yaml
standards:
  - id: STD-001
    name: Standard name
    description: What it requires
    rationale: Why it matters  # Critical - enables AI to explain
    severity: blocker|required|recommended
```

*Always include rationale* so AI can explain the "why", not just check compliance.

**5. Test with AI**
```
Ask AI: "Use the <skill-name> skill to check this"
Verify AI loads, runs, interprets correctly
Iterate until it works
```

**6. Version and commit**
```bash
git add .ai-skills/skill-name/
git commit -m "Add skill-name skill v1.0.0"
git tag skill-skill-name-v1.0.0
```

*Version properly*: Use semantic versioning. Update version in SKILL.md metadata when you make changes.

---

## Key Takeaways

1. **Progressive disclosure** - Load context only when needed
2. **Value triangle** - Scripts + AI + Standards
3. **Composability** - Skills work together naturally
4. **Platform agnostic** - Works with any AI that reads files
5. **Document rationale** - Enable AI to teach, not just check

---

**[← Back to MCP Servers](03-mcp-servers.md)** | **[Multi-Tab Orchestration →](05-multi-tab-orchestration.md)**
