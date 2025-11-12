# Module 6: The Skills Pattern

Package team expertise as discoverable, composable capabilities that AI assistants can load on-demand.

---

## The Problem: Expertise Scattered Everywhere

### Scenario: The New Team Member

A new SRE joins your team. They ask:

"How do I know if a service is ready for production?"

You could answer in three ways:

**Option 1: Verbal explanation** (15 minutes)
- Verbal handoff, inconsistent across team members
- Not documented anywhere
- Forgotten details
- No traceability

**Option 2: Point to documentation** (if it exists)
- "Check the wiki for the PRR checklist"
- Wiki is 8 months out of date
- Doesn't explain *why* each requirement matters
- No automation to help

**Option 3: Share a script** (if it exists)
```bash
./check-production-readiness.sh my-service
```
- Script checks some things automatically
- But can't explain context or handle edge cases
- "Why is this failing?" requires reading code
- Doesn't help you understand the *process*

### The Real Problem

Your team has expertise, but it's not **accessible, consistent, or composable**:

- **Expertise lives in people's heads** - Not in systems
- **Documentation gets stale** - No one maintains it
- **Scripts can't explain** - They execute but don't teach
- **Standards aren't enforced** - Just "tribal knowledge"
- **LLMs have generic knowledge** - Not *your team's* standards

### What We Need

A way to package team expertise that is:
1. **Discoverable** - AI can find it when relevant
2. **Self-documenting** - Explains what it does and why
3. **Composable** - Skills work together naturally
4. **Executable** - Can automate checks when possible
5. **Versioned** - Team standards evolve, skills evolve with them
6. **Progressive** - Load only what's needed, when it's needed

---

## The Skills Pattern

### What is a Skill?

A **skill** is a filesystem-based package containing:
- **Metadata**: What the skill does (YAML frontmatter in SKILL.md)
- **Instructions**: How the AI should use it (SKILL.md content)
- **Standards**: Team conventions, schemas, checklists (YAML/JSON files)
- **Automation**: Optional executable scripts (Python, Bash, etc.)
- **Examples**: Reference implementations showing success/failure cases

### The Key Insight: Progressive Disclosure

AI assistants face a fundamental challenge: **unlimited potential context, limited actual tokens**.

Skills solve this through **progressive disclosure**:

```
1. AI reads metadata (50 tokens): "production-readiness-review - Validates services for production launch"
2. User asks about production readiness
3. AI loads full skill (5000 tokens): Complete checklist, automation, examples
4. AI applies skill to user's service
```

**Without skills**: You'd paste the entire checklist into every conversation about production readiness.

**With skills**: AI loads it only when needed. Zero tokens most of the time, full context when relevant.

### The Value Triangle: Deterministic + Flexible + Versioned

Skills combine three things that individually are insufficient:

```
         Scripts
         (Deterministic)
            /\
           /  \
          /    \
         /      \
    AI           Team Standards
(Flexible)       (Versioned)
```

**Scripts alone**: Execute checks but can't reason about edge cases
**AI alone**: Generic knowledge, not your team's specific standards
**Standards alone**: Static documents that get out of date

**Skills = All three together**:
- Deterministic validation where automation is possible
- Flexible reasoning for context-specific decisions
- Versioned team standards that evolve with your practice

---

## Example 1: Production Readiness Review Skill

Let's build a complete, working skill that validates whether a service is ready for production.

### The Business Need

Before launching any service to production, your team needs to verify:
- Monitoring and alerting configured
- Documentation exists and is complete
- Security best practices followed
- Reliability requirements met
- Operational procedures defined

Currently, this is a manual checklist. Sometimes items get missed. The skill automates what it can and guides the AI to assess the rest.

### Skill Structure

```
.ai-skills/production-readiness-review/
├── SKILL.md                    # Metadata + instructions for AI
├── prr-requirements.yaml       # Team's PRR checklist
├── check-prr.py               # Automated validation script
└── examples/
    ├── passing-service/       # Example of compliant service
    │   ├── README.md
    │   ├── deployment.yaml
    │   └── servicemonitor.yaml
    └── failing-service/       # Example with issues
        ├── README.md
        └── deployment.yaml
```

### File 1: SKILL.md (Metadata + Instructions)

```markdown
---
name: production-readiness-review
description: Validates whether a service meets production launch requirements
version: 2.1.0
category: operations
tags: [production, reliability, compliance]
requires_tools: [kubectl, python3]
---

# Production Readiness Review Skill

## Purpose

This skill helps validate that a service meets your team's production readiness requirements before launch.

## When to Use

Use this skill when:
- Launching a new service to production
- Promoting a service from tier-3 to tier-1
- Conducting quarterly compliance reviews
- Onboarding new services to the platform

## How It Works

### Automated Checks (`check-prr.py`)

The script validates:
- ✅ Required documentation files exist
- ✅ Kubernetes deployment has required labels/annotations
- ✅ Security contexts configured properly
- ✅ Resource limits defined
- ✅ Health checks configured
- ✅ ServiceMonitor exists for Prometheus
- ✅ PrometheusRule exists with alerts

### Manual Assessment (AI-Assisted)

For requirements that can't be automated, guide the AI to:
- Review documentation quality
- Assess runbook completeness
- Evaluate on-call readiness
- Check load test results exist
- Verify backup procedures documented

## AI Instructions

When using this skill:

1. **Run automated checks first**:
   ```bash
   python3 .ai-skills/production-readiness-review/check-prr.py <service-name> <namespace>
   ```

2. **Interpret results with context**:
   - A failing check isn't always a blocker
   - Tier-3 services have relaxed requirements
   - Batch jobs don't need availability metrics
   - Internal tools may not need runbooks

3. **Guide manual assessment**:
   - Ask about service tier and type
   - Review documentation interactively
   - Explain WHY each requirement matters
   - Suggest remediation steps

4. **Provide actionable output**:
   - Clear pass/fail/warning per requirement
   - Specific remediation steps
   - Rationale for each finding
   - Estimated effort to fix

## Service Tiers

**Tier-1** (customer-facing, critical):
- All requirements are blockers
- No production launch without 100% pass

**Tier-2** (important, not critical):
- Most requirements required
- Some warnings acceptable with justification

**Tier-3** (internal, best effort):
- Relaxed requirements
- Focus on basic observability

## Examples

See `examples/` directory:
- `passing-service/`: Complete tier-1 HTTP API
- `failing-service/`: Service with several issues

## Related Skills

- `slo-builder`: Generate SLOs based on tier from PRR metadata
- `helm-values-validator`: Validates Helm configuration
```

### File 2: prr-requirements.yaml

```yaml
# Production Readiness Review Requirements
# Version: 2.1.0
# Last updated: 2024-11-11

requirements:
  # MONITORING & ALERTING
  - id: MON-001
    category: monitoring
    name: Prometheus metrics endpoint
    description: Service exposes /metrics endpoint in Prometheus format
    check: automated
    severity: blocker
    rationale: Without metrics, we can't monitor service health or performance
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
    validation:
      type: kubernetes
      check: deployment_has_port_named_metrics

  - id: MON-002
    category: monitoring
    name: ServiceMonitor configured
    description: ServiceMonitor resource exists to scrape metrics
    check: automated
    severity: blocker
    rationale: Prometheus must be configured to scrape the service
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended
    validation:
      type: kubernetes
      check: servicemonitor_exists

  - id: MON-003
    category: monitoring
    name: Alerting rules defined
    description: PrometheusRule with at least one alert for the service
    check: automated
    severity: blocker
    rationale: Team must be notified when service degrades
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended
    validation:
      type: kubernetes
      check: prometheusrule_exists

  # DOCUMENTATION
  - id: DOC-001
    category: documentation
    name: README exists
    description: README.md in repository root with service description
    check: automated
    severity: blocker
    rationale: Basic documentation is essential for team understanding
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
    validation:
      type: filesystem
      check: file_exists
      path: README.md

  - id: DOC-002
    category: documentation
    name: Runbook exists
    description: Runbook with common failure modes and remediation
    check: automated
    severity: blocker
    rationale: On-call engineers need clear guidance during incidents
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended
    validation:
      type: filesystem
      check: file_exists
      path: RUNBOOK.md

  - id: DOC-003
    category: documentation
    name: Architecture documentation
    description: Architecture diagram and design decisions documented
    check: manual
    severity: required
    rationale: Team needs to understand system design for troubleshooting
    tiers:
      tier-1: required
      tier-2: recommended
      tier-3: optional

  # SECURITY
  - id: SEC-001
    category: security
    name: Security context configured
    description: Pod security context with runAsNonRoot, readOnlyRootFilesystem
    check: automated
    severity: blocker
    rationale: Defense in depth - limit container privileges
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
    validation:
      type: kubernetes
      check: security_context_configured

  - id: SEC-002
    category: security
    name: Secrets management
    description: Secrets stored in Kubernetes Secrets or external vault, not env vars
    check: automated
    severity: blocker
    rationale: Prevent credential exposure in configs or logs
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
    validation:
      type: kubernetes
      check: no_plaintext_secrets

  - id: SEC-003
    category: security
    name: Network policies defined
    description: NetworkPolicy restricting ingress/egress
    check: automated
    severity: required
    rationale: Limit blast radius of compromised pod
    tiers:
      tier-1: required
      tier-2: recommended
      tier-3: optional
    validation:
      type: kubernetes
      check: networkpolicy_exists

  # RELIABILITY
  - id: REL-001
    category: reliability
    name: Multiple replicas
    description: Deployment has replicas >= 2 for tier-1, >= 1 for others
    check: automated
    severity: blocker
    rationale: Single instance is single point of failure
    tiers:
      tier-1: required  # >= 2 replicas
      tier-2: recommended  # >= 2 replicas
      tier-3: optional  # >= 1 replica ok
    validation:
      type: kubernetes
      check: replica_count

  - id: REL-002
    category: reliability
    name: Resource limits defined
    description: CPU and memory requests/limits set
    check: automated
    severity: blocker
    rationale: Prevent resource starvation and cluster instability
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
    validation:
      type: kubernetes
      check: resources_defined

  - id: REL-003
    category: reliability
    name: Liveness probe configured
    description: Liveness probe configured to restart unhealthy pods
    check: automated
    severity: blocker
    rationale: Automatic recovery from hung processes
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended
    validation:
      type: kubernetes
      check: liveness_probe_exists

  - id: REL-004
    category: reliability
    name: Readiness probe configured
    description: Readiness probe to remove pods from load balancing when not ready
    check: automated
    severity: blocker
    rationale: Prevent traffic to pods that can't handle it
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended
    validation:
      type: kubernetes
      check: readiness_probe_exists

  # OBSERVABILITY
  - id: OBS-001
    category: observability
    name: Structured logging
    description: Service logs in JSON format to stdout
    check: manual
    severity: required
    rationale: Enables automated log parsing and analysis
    tiers:
      tier-1: required
      tier-2: required
      tier-3: recommended

  - id: OBS-002
    category: observability
    name: Trace instrumentation
    description: Distributed tracing integrated (Jaeger/OpenTelemetry)
    check: manual
    severity: recommended
    rationale: Essential for debugging distributed systems
    tiers:
      tier-1: required
      tier-2: recommended
      tier-3: optional

  - id: OBS-003
    category: observability
    name: Grafana dashboard
    description: Grafana dashboard for key service metrics
    check: manual
    severity: required
    rationale: Visual monitoring for operators
    tiers:
      tier-1: required
      tier-2: required
      tier-3: optional

  # OPERATIONAL
  - id: OPS-001
    category: operational
    name: On-call rotation defined
    description: Service has assigned on-call rotation
    check: manual
    severity: blocker
    rationale: Someone must be responsible for incidents
    tiers:
      tier-1: required
      tier-2: required
      tier-3: optional

  - id: OPS-002
    category: operational
    name: Escalation policy
    description: Documented escalation path for critical issues
    check: manual
    severity: required
    rationale: Clear path when on-call can't resolve
    tiers:
      tier-1: required
      tier-2: required
      tier-3: optional

  - id: OPS-003
    category: operational
    name: Backup procedures
    description: Backup and restore procedures documented (if stateful)
    check: manual
    severity: required
    rationale: Data loss prevention and recovery
    tiers:
      tier-1: required  # if stateful
      tier-2: required  # if stateful
      tier-3: recommended  # if stateful

  # PERFORMANCE
  - id: PERF-001
    category: performance
    name: Load test results
    description: Load testing completed and results documented
    check: manual
    severity: required
    rationale: Understand capacity limits before production
    tiers:
      tier-1: required
      tier-2: recommended
      tier-3: optional

  - id: PERF-002
    category: performance
    name: Capacity planning
    description: Expected load and scaling plan documented
    check: manual
    severity: required
    rationale: Prevent outages from unexpected traffic
    tiers:
      tier-1: required
      tier-2: recommended
      tier-3: optional
```

### File 3: check-prr.py

```python
#!/usr/bin/env python3
"""
Production Readiness Review Automated Checker
Version: 2.1.0

Validates Kubernetes deployments against PRR requirements.
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

class Colors:
    """ANSI color codes for output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class CheckResult:
    """Result of a single check"""
    def __init__(self, requirement_id: str, name: str, passed: bool,
                 severity: str, message: str, details: Optional[str] = None):
        self.requirement_id = requirement_id
        self.name = name
        self.passed = passed
        self.severity = severity
        self.message = message
        self.details = details

class PRRChecker:
    """Production Readiness Review automated checker"""

    def __init__(self, service_name: str, namespace: str, tier: str = "tier-1"):
        self.service_name = service_name
        self.namespace = namespace
        self.tier = tier
        self.results: List[CheckResult] = []
        self.requirements = self._load_requirements()

    def _load_requirements(self) -> Dict:
        """Load PRR requirements from YAML file"""
        script_dir = Path(__file__).parent
        req_file = script_dir / "prr-requirements.yaml"

        try:
            with open(req_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{Colors.RED}Error loading requirements: {e}{Colors.RESET}")
            sys.exit(1)

    def _run_kubectl(self, args: List[str]) -> Optional[Dict]:
        """Run kubectl command and return JSON output"""
        try:
            cmd = ['kubectl', '-n', self.namespace] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return None
        except subprocess.CalledProcessError:
            return None
        except json.JSONDecodeError as e:
            print(f"{Colors.YELLOW}Warning: Could not parse kubectl output: {e}{Colors.RESET}")
            return None

    def _get_deployment(self) -> Optional[Dict]:
        """Get deployment manifest"""
        return self._run_kubectl([
            'get', 'deployment', self.service_name,
            '-o', 'json'
        ])

    def _get_service(self) -> Optional[Dict]:
        """Get service manifest"""
        return self._run_kubectl([
            'get', 'service', self.service_name,
            '-o', 'json'
        ])

    def _get_servicemonitor(self) -> Optional[Dict]:
        """Get ServiceMonitor manifest"""
        return self._run_kubectl([
            'get', 'servicemonitor', self.service_name,
            '-o', 'json'
        ])

    def _get_prometheusrule(self) -> Optional[Dict]:
        """Get PrometheusRule manifest"""
        return self._run_kubectl([
            'get', 'prometheusrule', f"{self.service_name}-alerts",
            '-o', 'json'
        ])

    def _get_networkpolicy(self) -> Optional[Dict]:
        """Get NetworkPolicy manifest"""
        return self._run_kubectl([
            'get', 'networkpolicy', self.service_name,
            '-o', 'json'
        ])

    def check_deployment_has_metrics_port(self, deployment: Dict) -> CheckResult:
        """MON-001: Check if deployment has metrics port"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            for container in containers:
                if 'ports' in container:
                    for port in container['ports']:
                        if port.get('name') == 'metrics':
                            return CheckResult(
                                req['id'], req['name'], True, req['severity'],
                                f"Metrics port found: {port.get('containerPort')}"
                            )

            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "No port named 'metrics' found in deployment",
                "Add a container port named 'metrics' (typically 8080 or 9090)"
            )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing deployment: {e}"
            )

    def check_servicemonitor_exists(self) -> CheckResult:
        """MON-002: Check if ServiceMonitor exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-002')

        sm = self._get_servicemonitor()
        if sm:
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                "ServiceMonitor configured"
            )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "ServiceMonitor not found",
                f"Create a ServiceMonitor resource for {self.service_name}"
            )

    def check_prometheusrule_exists(self) -> CheckResult:
        """MON-003: Check if PrometheusRule exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'MON-003')

        pr = self._get_prometheusrule()
        if pr:
            try:
                rules = pr['spec']['groups'][0]['rules']
                num_alerts = len([r for r in rules if r.get('alert')])
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"PrometheusRule found with {num_alerts} alert(s)"
                )
            except (KeyError, IndexError):
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "PrometheusRule exists but has no alerts defined"
                )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "PrometheusRule not found",
                f"Create a PrometheusRule resource named {self.service_name}-alerts"
            )

    def check_file_exists(self, filepath: str, req_id: str) -> CheckResult:
        """DOC-001, DOC-002: Check if documentation file exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == req_id)

        # Check in current directory
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size < 100:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"{filepath} exists but appears too short ({file_size} bytes)",
                    "Ensure documentation is comprehensive"
                )
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                f"{filepath} exists ({file_size} bytes)"
            )
        else:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"{filepath} not found",
                f"Create {filepath} with comprehensive documentation"
            )

    def check_security_context(self, deployment: Dict) -> CheckResult:
        """SEC-001: Check if security context is configured"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            spec = deployment['spec']['template']['spec']
            security_context = spec.get('securityContext', {})

            issues = []

            if not security_context.get('runAsNonRoot'):
                issues.append("runAsNonRoot not set to true")

            # Check container security contexts
            containers = spec.get('containers', [])
            for container in containers:
                container_sc = container.get('securityContext', {})
                if not container_sc.get('readOnlyRootFilesystem'):
                    issues.append(f"readOnlyRootFilesystem not set for container {container['name']}")

            if issues:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "Security context issues found",
                    "; ".join(issues)
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "Security context properly configured"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing deployment security context: {e}"
            )

    def check_no_plaintext_secrets(self, deployment: Dict) -> CheckResult:
        """SEC-002: Check for plaintext secrets in env vars"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-002')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            suspicious_vars = []

            for container in containers:
                env_vars = container.get('env', [])
                for env_var in env_vars:
                    # Check if env var has direct value (not from secret/configmap)
                    if 'value' in env_var and not ('valueFrom' in env_var):
                        var_name = env_var['name'].lower()
                        # Check for common secret patterns
                        if any(pattern in var_name for pattern in ['password', 'secret', 'token', 'key', 'api']):
                            suspicious_vars.append(env_var['name'])

            if suspicious_vars:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"Potential plaintext secrets found: {', '.join(suspicious_vars)}",
                    "Use Kubernetes Secrets or valueFrom with secretKeyRef"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "No plaintext secrets detected"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing environment variables: {e}"
            )

    def check_networkpolicy_exists(self) -> CheckResult:
        """SEC-003: Check if NetworkPolicy exists"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'SEC-003')

        # Check if tier requires this
        if req['tiers'][self.tier] == 'optional':
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                f"Optional for {self.tier} - skipped"
            )

        np = self._get_networkpolicy()
        if np:
            return CheckResult(
                req['id'], req['name'], True, req['severity'],
                "NetworkPolicy configured"
            )
        else:
            severity = 'warning' if req['tiers'][self.tier] == 'recommended' else req['severity']
            return CheckResult(
                req['id'], req['name'], False, severity,
                "NetworkPolicy not found",
                f"Create a NetworkPolicy for {self.service_name}"
            )

    def check_replica_count(self, deployment: Dict) -> CheckResult:
        """REL-001: Check replica count"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'REL-001')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            replicas = deployment['spec']['replicas']

            min_replicas = 2 if self.tier == 'tier-1' else 1

            if replicas >= min_replicas:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"Replica count: {replicas} (minimum: {min_replicas})"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    f"Insufficient replicas: {replicas} (minimum: {min_replicas})",
                    f"Increase replicas to at least {min_replicas} for {self.tier}"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing replica count: {e}"
            )

    def check_resources_defined(self, deployment: Dict) -> CheckResult:
        """REL-002: Check if resource requests/limits are defined"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == 'REL-002')

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            issues = []

            for container in containers:
                resources = container.get('resources', {})
                requests = resources.get('requests', {})
                limits = resources.get('limits', {})

                if not requests.get('memory'):
                    issues.append(f"{container['name']}: missing memory request")
                if not requests.get('cpu'):
                    issues.append(f"{container['name']}: missing CPU request")
                if not limits.get('memory'):
                    issues.append(f"{container['name']}: missing memory limit")
                if not limits.get('cpu'):
                    issues.append(f"{container['name']}: missing CPU limit")

            if issues:
                return CheckResult(
                    req['id'], req['name'], False, req['severity'],
                    "Resource issues found",
                    "; ".join(issues)
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    "Resource requests and limits configured"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing resources: {e}"
            )

    def check_probe(self, deployment: Dict, probe_type: str, req_id: str) -> CheckResult:
        """REL-003, REL-004: Check if liveness/readiness probe is configured"""
        req = next(r for r in self.requirements['requirements'] if r['id'] == req_id)

        if not deployment:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                "Deployment not found"
            )

        try:
            containers = deployment['spec']['template']['spec']['containers']
            probe_name = f"{probe_type}Probe"
            missing_containers = []

            for container in containers:
                if probe_name not in container:
                    missing_containers.append(container['name'])

            if missing_containers:
                severity = req['severity'] if req['tiers'][self.tier] == 'required' else 'warning'
                return CheckResult(
                    req['id'], req['name'], False, severity,
                    f"{probe_type.capitalize()} probe missing for: {', '.join(missing_containers)}",
                    f"Add {probe_name} to container spec"
                )
            else:
                return CheckResult(
                    req['id'], req['name'], True, req['severity'],
                    f"{probe_type.capitalize()} probe configured for all containers"
                )
        except KeyError as e:
            return CheckResult(
                req['id'], req['name'], False, req['severity'],
                f"Error parsing {probe_type} probe: {e}"
            )

    def run_checks(self) -> List[CheckResult]:
        """Run all automated checks"""
        print(f"\n{Colors.BOLD}Production Readiness Review{Colors.RESET}")
        print(f"Service: {self.service_name}")
        print(f"Namespace: {self.namespace}")
        print(f"Tier: {self.tier}\n")

        # Fetch resources
        print("Fetching Kubernetes resources...")
        deployment = self._get_deployment()

        # Run all automated checks
        self.results.append(self.check_deployment_has_metrics_port(deployment))
        self.results.append(self.check_servicemonitor_exists())
        self.results.append(self.check_prometheusrule_exists())
        self.results.append(self.check_file_exists('README.md', 'DOC-001'))
        self.results.append(self.check_file_exists('RUNBOOK.md', 'DOC-002'))
        self.results.append(self.check_security_context(deployment))
        self.results.append(self.check_no_plaintext_secrets(deployment))
        self.results.append(self.check_networkpolicy_exists())
        self.results.append(self.check_replica_count(deployment))
        self.results.append(self.check_resources_defined(deployment))
        self.results.append(self.check_probe(deployment, 'liveness', 'REL-003'))
        self.results.append(self.check_probe(deployment, 'readiness', 'REL-004'))

        return self.results

    def print_results(self):
        """Print check results in a formatted way"""
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]

        print(f"\n{Colors.BOLD}Automated Check Results:{Colors.RESET}\n")

        # Print failures first
        if failed:
            print(f"{Colors.RED}{Colors.BOLD}FAILED CHECKS:{Colors.RESET}")
            for result in failed:
                color = Colors.RED if result.severity == 'blocker' else Colors.YELLOW
                print(f"\n{color}✗ [{result.requirement_id}] {result.name}{Colors.RESET}")
                print(f"  {result.message}")
                if result.details:
                    print(f"  → {result.details}")

        # Print successes
        if passed:
            print(f"\n{Colors.GREEN}{Colors.BOLD}PASSED CHECKS:{Colors.RESET}")
            for result in passed:
                print(f"{Colors.GREEN}✓ [{result.requirement_id}] {result.name}{Colors.RESET}")
                print(f"  {result.message}")

        # Summary
        print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
        print(f"Total checks: {len(self.results)}")
        print(f"{Colors.GREEN}Passed: {len(passed)}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {len(failed)}{Colors.RESET}")

        blockers = [r for r in failed if r.severity == 'blocker']
        if blockers:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠ {len(blockers)} blocker(s) must be resolved before production launch{Colors.RESET}")
            return 1
        else:
            print(f"\n{Colors.GREEN}All blockers passed! Review manual checks before launch.{Colors.RESET}")
            return 0

def main():
    parser = argparse.ArgumentParser(
        description='Production Readiness Review automated checker'
    )
    parser.add_argument('service', help='Service name')
    parser.add_argument('namespace', help='Kubernetes namespace')
    parser.add_argument(
        '--tier',
        choices=['tier-1', 'tier-2', 'tier-3'],
        default='tier-1',
        help='Service tier (default: tier-1)'
    )
    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    checker = PRRChecker(args.service, args.namespace, args.tier)
    results = checker.run_checks()

    if args.output == 'json':
        output = {
            'service': args.service,
            'namespace': args.namespace,
            'tier': args.tier,
            'results': [
                {
                    'id': r.requirement_id,
                    'name': r.name,
                    'passed': r.passed,
                    'severity': r.severity,
                    'message': r.message,
                    'details': r.details
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    else:
        sys.exit(checker.print_results())

if __name__ == '__main__':
    main()
```

### How AI Adds Value

The script automates validation, but AI adds intelligence:

1. **Contextual interpretation**: "This is a batch job, so it doesn't need high availability"
2. **Explains rationale**: "Why does this requirement exist for tier-1 services?"
3. **Suggests remediation**: "Here's how to fix the security context issue"
4. **Handles edge cases**: "The metrics port is named 'http-metrics' instead of 'metrics' - that's acceptable"
5. **Assesses manual items**: "Let me review your RUNBOOK.md to see if it's comprehensive"

### Example Usage

```bash
# AI loads the skill and runs the check
$ python3 .ai-skills/production-readiness-review/check-prr.py user-api production --tier tier-1

Production Readiness Review
Service: user-api
Namespace: production
Tier: tier-1

Fetching Kubernetes resources...

FAILED CHECKS:

✗ [MON-003] Alerting rules defined
  PrometheusRule not found
  → Create a PrometheusRule resource named user-api-alerts

✗ [DOC-002] Runbook exists
  RUNBOOK.md not found
  → Create RUNBOOK.md with comprehensive documentation

✗ [REL-001] Multiple replicas
  Insufficient replicas: 1 (minimum: 2)
  → Increase replicas to at least 2 for tier-1

PASSED CHECKS:
✓ [MON-001] Prometheus metrics endpoint
  Metrics port found: 8080
✓ [MON-002] ServiceMonitor configured
  ServiceMonitor configured
... [other passing checks]

Summary:
Total checks: 12
Passed: 9
Failed: 3

⚠ 3 blocker(s) must be resolved before production launch
```

Then AI says:
```
I've run the automated checks. You have 3 blockers to resolve:

1. **Alerting rules** (MON-003): You need a PrometheusRule resource. Based on your
   tier-1 HTTP API service type, you should have alerts for:
   - High error rate (>1% over 5m)
   - High latency (p99 > 500ms)
   - Low availability (<99.9%)

   Would you like me to generate a PrometheusRule based on these standard alerts?

2. **Runbook** (DOC-002): Create RUNBOOK.md with at least:
   - Common failure scenarios
   - Troubleshooting steps
   - Emergency contacts

   I can generate a template based on your service architecture if you'd like.

3. **Replica count** (REL-001): You have 1 replica but tier-1 requires at least 2
   for high availability. Update your deployment.yaml or Helm values to set:

   ```yaml
   replicas: 2
   ```

   This ensures no downtime during rolling updates.

The other 9 checks passed. Once these blockers are resolved, we'll need to do manual
assessment of documentation quality, load testing, and operational readiness.
```

---

## Example 2: SLO Builder Skill

Now let's build a skill that **composes** with the PRR skill - it reads the service tier from PRR and generates appropriate SLOs.

### The Business Need

Service Level Objectives (SLOs) should match the service tier:
- Tier-1 services need strict SLOs (99.9% availability)
- Tier-3 services can have relaxed SLOs (99% availability)
- HTTP APIs need latency SLOs
- Batch jobs need success rate and duration SLOs

Manually creating SLO definitions is time-consuming and error-prone. This skill automates it based on service metadata.

### Skill Structure

```
.ai-skills/slo-builder/
├── SKILL.md                    # Metadata + instructions
├── slo-templates.yaml          # SLO templates by tier and type
├── build-slos.py              # Generates Sloth-format SLOs
└── examples/
    ├── api-service-tier1/
    │   ├── input-deployment.yaml
    │   └── output-slos.yaml
    └── batch-job-tier2/
        ├── input-cronjob.yaml
        └── output-slos.yaml
```

### File 1: SKILL.md

```markdown
---
name: slo-builder
description: Generates Service Level Objectives based on service tier and type
version: 1.0.0
category: operations
tags: [slo, reliability, monitoring]
requires_tools: [python3, kubectl]
composes_with: [production-readiness-review]
---

# SLO Builder Skill

## Purpose

Automatically generate Service Level Objectives (SLOs) in Sloth format based on:
- Service tier (from PRR metadata or explicit specification)
- Service type (HTTP API, gRPC service, batch job, data pipeline)
- Actual metrics available in the deployment

## When to Use

Use this skill when:
- Launching a new service that needs SLOs
- Migrating existing services to formal SLO framework
- Updating SLOs after tier changes
- Standardizing SLOs across the platform

## How It Works

### Composition with PRR

**Best workflow**:
1. Run Production Readiness Review first
2. PRR identifies service tier and type
3. SLO Builder reads that metadata
4. Generates appropriate SLOs without asking again

### Standalone Usage

Can also be used standalone by specifying tier and type explicitly.

## SLO Templates

Templates defined in `slo-templates.yaml` cover:

**By Tier**:
- **Tier-1**: 99.9% availability, strict latency targets
- **Tier-2**: 99.5% availability, moderate latency targets
- **Tier-3**: 99% availability, relaxed targets

**By Service Type**:
- **HTTP API**: Availability, latency (p95, p99), error rate
- **gRPC Service**: Per-method SLOs, different latency targets
- **Batch Job**: Success rate, duration (no latency)
- **Data Pipeline**: Freshness, completeness, accuracy

## AI Instructions

When using this skill:

1. **Check for PRR metadata first**:
   - Look for `.prr-metadata.yaml` in service directory
   - If exists, read tier and service type from there

2. **Determine service type from manifests**:
   - Deployment with HTTP port → HTTP API
   - CronJob → Batch job
   - StatefulSet with database → Data pipeline

3. **Run the builder**:
   ```bash
   python3 .ai-skills/slo-builder/build-slos.py <service-name> <namespace> \
     --tier <tier> --type <type>
   ```

4. **Explain the generated SLOs**:
   - Why these targets for this tier
   - What each SLI measures
   - How error budget works
   - When alerts will fire

5. **Customize if needed**:
   - Adjust targets for service-specific needs
   - Add custom SLIs for unique metrics
   - Explain tradeoffs (stricter SLO = higher cost)

## Output Format

Generates Sloth-format SLO definitions ready to deploy:
- SLO declarations
- SLI queries (PromQL)
- Error budget burn alerts
- Multi-window burn rate alerts (fast/slow)

## Examples

See `examples/` directory:
- `api-service-tier1/`: HTTP API with strict tier-1 SLOs
- `batch-job-tier2/`: Batch job with success rate SLOs

## Related Skills

- `production-readiness-review`: Provides tier metadata
- `prometheus-query-builder`: Helps validate SLI queries exist
```

### File 2: slo-templates.yaml

```yaml
# SLO Templates by Tier and Service Type
# Version: 1.0.0
# Format: Sloth (https://sloth.dev)

templates:
  # HTTP API SERVICE TEMPLATES
  http-api:
    tier-1:
      availability:
        target: 99.9  # 43m downtime/month
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 2h    # Page if burning 1% error budget in 2h
          slow: 24h   # Warn if burning 5% error budget in 24h

      latency_p99:
        target: 99.0  # 99% of requests under threshold
        threshold_ms: 500
        sli_query: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 0.5

      latency_p95:
        target: 99.5  # 99.5% of requests under threshold
        threshold_ms: 200
        sli_query: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 0.2

      error_rate:
        target: 99.9  # < 0.1% errors
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))

    tier-2:
      availability:
        target: 99.5  # 3.6h downtime/month
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 2h
          slow: 24h

      latency_p99:
        target: 99.0
        threshold_ms: 1000
        sli_query: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 1.0

      latency_p95:
        target: 99.5
        threshold_ms: 500
        sli_query: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 0.5

      error_rate:
        target: 99.0  # < 1% errors
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))

    tier-3:
      availability:
        target: 99.0  # 7.2h downtime/month
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 6h
          slow: 72h

      latency_p95:
        target: 95.0
        threshold_ms: 2000
        sli_query: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 2.0

      error_rate:
        target: 95.0  # < 5% errors
        sli_query: |
          sum(rate(http_requests_total{service="{{service}}",code!~"5.."}[{{window}}]))
          /
          sum(rate(http_requests_total{service="{{service}}"}[{{window}}]))

  # BATCH JOB TEMPLATES
  batch-job:
    tier-1:
      success_rate:
        target: 99.9  # 99.9% of jobs succeed
        sli_query: |
          sum(rate(batch_job_completed{service="{{service}}",status="success"}[{{window}}]))
          /
          sum(rate(batch_job_completed{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 2h
          slow: 24h

      duration_p95:
        target: 95.0  # 95% complete within expected time
        threshold_minutes: 30  # Adjust based on job
        sli_query: |
          histogram_quantile(0.95,
            sum(rate(batch_job_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < (30 * 60)  # 30 minutes

    tier-2:
      success_rate:
        target: 99.5
        sli_query: |
          sum(rate(batch_job_completed{service="{{service}}",status="success"}[{{window}}]))
          /
          sum(rate(batch_job_completed{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 6h
          slow: 48h

      duration_p95:
        target: 90.0
        threshold_minutes: 60
        sli_query: |
          histogram_quantile(0.95,
            sum(rate(batch_job_duration_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < (60 * 60)

    tier-3:
      success_rate:
        target: 95.0
        sli_query: |
          sum(rate(batch_job_completed{service="{{service}}",status="success"}[{{window}}]))
          /
          sum(rate(batch_job_completed{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 24h
          slow: 168h  # 1 week

  # GRPC SERVICE TEMPLATES
  grpc-service:
    tier-1:
      availability:
        target: 99.9
        sli_query: |
          sum(rate(grpc_server_handled_total{service="{{service}}",grpc_code!="Unknown",grpc_code!="Unavailable"}[{{window}}]))
          /
          sum(rate(grpc_server_handled_total{service="{{service}}"}[{{window}}]))
        error_budget_burn:
          fast: 2h
          slow: 24h

      latency_p99:
        target: 99.0
        threshold_ms: 100  # gRPC typically faster than HTTP
        sli_query: |
          histogram_quantile(0.99,
            sum(rate(grpc_server_handling_seconds_bucket{service="{{service}}"}[{{window}}])) by (le)
          ) < 0.1

  # DATA PIPELINE TEMPLATES
  data-pipeline:
    tier-1:
      freshness:
        target: 99.9  # Data updated within SLA
        threshold_minutes: 15
        sli_query: |
          (time() - pipeline_last_successful_run_timestamp{service="{{service}}"}) < (15 * 60)

      completeness:
        target: 99.9  # % of expected records processed
        sli_query: |
          sum(rate(pipeline_records_processed{service="{{service}}"}[{{window}}]))
          /
          sum(rate(pipeline_records_expected{service="{{service}}"}[{{window}}]))

      accuracy:
        target: 99.99  # % of records without errors
        sli_query: |
          sum(rate(pipeline_records_valid{service="{{service}}"}[{{window}}]))
          /
          sum(rate(pipeline_records_processed{service="{{service}}"}[{{window}}]))

error_budget_policies:
  tier-1:
    page: "0.1%"  # Page if burning 0.1% of monthly budget in 1h
    warn: "1%"    # Warn if burning 1% of monthly budget in 6h
  tier-2:
    page: "0.5%"
    warn: "2%"
  tier-3:
    page: "2%"
    warn: "5%"

alerting_windows:
  # Multi-window, multi-burn-rate alerts (Google SRE best practice)
  fast_burn:
    lookback: 1h
    errors: 14.4  # 2% error budget burn rate
  slow_burn:
    lookback: 6h
    errors: 6     # 1% error budget burn rate
```

### File 3: build-slos.py

```python
#!/usr/bin/env python3
"""
SLO Builder - Generates Sloth-format SLO definitions
Version: 1.0.0

Generates SLOs based on service tier and type.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import yaml

class SLOBuilder:
    """Builds SLO definitions from templates"""

    def __init__(self, service_name: str, namespace: str, tier: str, service_type: str):
        self.service_name = service_name
        self.namespace = namespace
        self.tier = tier
        self.service_type = service_type
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load SLO templates from YAML"""
        script_dir = Path(__file__).parent
        template_file = script_dir / "slo-templates.yaml"

        try:
            with open(template_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading templates: {e}", file=sys.stderr)
            sys.exit(1)

    def _substitute_variables(self, text: str) -> str:
        """Replace template variables with actual values"""
        return (text
                .replace('{{service}}', self.service_name)
                .replace('{{namespace}}', self.namespace))

    def _generate_slo_spec(self, slo_name: str, slo_config: Dict) -> Dict:
        """Generate a single SLO spec in Sloth format"""
        return {
            'name': f"{self.service_name}-{slo_name}",
            'objective': slo_config['target'],
            'description': f"{slo_name} SLO for {self.service_name}",
            'sli': {
                'events': {
                    'errorQuery': self._substitute_variables(slo_config['sli_query'])
                }
            },
            'alerting': {
                'name': f"{self.service_name}-{slo_name}",
                'labels': {
                    'service': self.service_name,
                    'tier': self.tier,
                    'slo': slo_name
                },
                'annotations': {
                    'summary': f"High error budget burn for {slo_name}"
                },
                'pageAlert': self._generate_burn_rate_alert(slo_config, 'fast'),
                'ticketAlert': self._generate_burn_rate_alert(slo_config, 'slow')
            }
        }

    def _generate_burn_rate_alert(self, slo_config: Dict, speed: str) -> Dict:
        """Generate burn rate alert configuration"""
        if 'error_budget_burn' not in slo_config:
            return None

        burn_config = slo_config['error_budget_burn']
        window = burn_config.get(speed, '1h')

        return {
            'annotations': {
                'description': f"{speed.capitalize()} burn rate alert - {window} window"
            }
        }

    def build(self) -> Dict:
        """Build complete SLO specification"""
        # Get templates for this service type and tier
        try:
            type_templates = self.templates['templates'][self.service_type]
            tier_template = type_templates[self.tier]
        except KeyError as e:
            print(f"Error: No template found for type={self.service_type}, tier={self.tier}",
                  file=sys.stderr)
            print(f"Available types: {list(self.templates['templates'].keys())}",
                  file=sys.stderr)
            sys.exit(1)

        # Generate SLO specs
        slos = []
        for slo_name, slo_config in tier_template.items():
            slos.append(self._generate_slo_spec(slo_name, slo_config))

        # Build Sloth spec
        sloth_spec = {
            'version': 'prometheus/v1',
            'service': self.service_name,
            'labels': {
                'tier': self.tier,
                'namespace': self.namespace,
                'service_type': self.service_type
            },
            'slos': slos
        }

        return sloth_spec

    def explain(self):
        """Print human-readable explanation of generated SLOs"""
        print(f"\nSLO Configuration for {self.service_name}")
        print(f"{'=' * 60}\n")
        print(f"Service Type: {self.service_type}")
        print(f"Tier: {self.tier}")
        print(f"Namespace: {self.namespace}\n")

        try:
            type_templates = self.templates['templates'][self.service_type]
            tier_template = type_templates[self.tier]
        except KeyError:
            return

        for slo_name, slo_config in tier_template.items():
            target = slo_config['target']
            print(f"SLO: {slo_name}")
            print(f"  Target: {target}%")

            if 'threshold_ms' in slo_config:
                print(f"  Threshold: {slo_config['threshold_ms']}ms")
            elif 'threshold_minutes' in slo_config:
                print(f"  Threshold: {slo_config['threshold_minutes']} minutes")

            # Calculate error budget
            error_budget = 100 - target
            if slo_name == 'availability':
                # Convert to downtime
                monthly_minutes = 30 * 24 * 60  # ~43200 minutes
                allowed_downtime = monthly_minutes * (error_budget / 100)
                print(f"  Error Budget: {error_budget}% ({allowed_downtime:.1f} minutes/month)")
            else:
                print(f"  Error Budget: {error_budget}%")

            if 'error_budget_burn' in slo_config:
                burn = slo_config['error_budget_burn']
                print(f"  Alerts:")
                print(f"    Fast burn: Page if burning error budget in {burn['fast']}")
                print(f"    Slow burn: Ticket if burning error budget in {burn['slow']}")

            print()

def main():
    parser = argparse.ArgumentParser(
        description='Generate SLO definitions in Sloth format'
    )
    parser.add_argument('service', help='Service name')
    parser.add_argument('namespace', help='Kubernetes namespace')
    parser.add_argument(
        '--tier',
        choices=['tier-1', 'tier-2', 'tier-3'],
        required=True,
        help='Service tier'
    )
    parser.add_argument(
        '--type',
        choices=['http-api', 'grpc-service', 'batch-job', 'data-pipeline'],
        required=True,
        help='Service type'
    )
    parser.add_argument(
        '--output',
        default='slos.yaml',
        help='Output file (default: slos.yaml)'
    )
    parser.add_argument(
        '--explain',
        action='store_true',
        help='Print human-readable explanation'
    )

    args = parser.parse_args()

    builder = SLOBuilder(args.service, args.namespace, args.tier, args.type)

    if args.explain:
        builder.explain()

    # Generate SLO spec
    slo_spec = builder.build()

    # Write to file
    with open(args.output, 'w') as f:
        yaml.dump(slo_spec, f, default_flow_style=False, sort_keys=False)

    print(f"\n✓ SLO specification written to {args.output}")
    print(f"\nTo deploy:")
    print(f"  kubectl apply -f {args.output}")
    print(f"\nTo generate Prometheus rules:")
    print(f"  sloth generate -i {args.output} -o prometheus-rules.yaml")

if __name__ == '__main__':
    main()
```

### Demonstrating Composition

Here's how the two skills work together:

**Step 1: Run PRR**
```bash
$ python3 .ai-skills/production-readiness-review/check-prr.py user-api production --tier tier-1

# PRR identifies: tier-1 HTTP API service
# Creates metadata file: .prr-metadata.yaml
```

**Step 2: User asks for SLOs**
```
User: "Create SLOs for this service"
```

**Step 3: AI loads SLO builder skill and checks for PRR metadata**
```python
# AI reads .prr-metadata.yaml:
tier: tier-1
service_type: http-api
```

**Step 4: AI generates SLOs without asking**
```bash
$ python3 .ai-skills/slo-builder/build-slos.py user-api production \
  --tier tier-1 --type http-api --output user-api-slos.yaml --explain

SLO Configuration for user-api
============================================================

Service Type: http-api
Tier: tier-1
Namespace: production

SLO: availability
  Target: 99.9%
  Error Budget: 0.1% (43.2 minutes/month)
  Alerts:
    Fast burn: Page if burning error budget in 2h
    Slow burn: Ticket if burning error budget in 24h

SLO: latency_p99
  Target: 99.0%
  Threshold: 500ms
  Error Budget: 1.0%

SLO: latency_p95
  Target: 99.5%
  Threshold: 200ms
  Error Budget: 0.5%

SLO: error_rate
  Target: 99.9%
  Error Budget: 0.1%

✓ SLO specification written to user-api-slos.yaml
```

**Step 5: AI explains the SLOs**
```
I've generated SLOs for your tier-1 HTTP API service. Here's what each means:

**Availability (99.9%)**:
Your service can be down for ~43 minutes per month. This is strict because you're
tier-1. If you experience more downtime, you've exhausted your error budget and
should halt risky deployments until next month.

**Latency p99 (<500ms)**:
99% of requests must complete in under 500ms. This ensures good user experience
even at the tail of the distribution.

**Latency p95 (<200ms)**:
99.5% of requests must complete in under 200ms. Most users experience fast response.

**Error rate (<0.1%)**:
Less than 1 in 1000 requests can return 5xx errors.

**Alerts**:
- **Fast burn (2h)**: You'll get paged if you're burning error budget 14x faster
  than sustainable. This catches severe outages.
- **Slow burn (24h)**: You'll get a ticket if you're burning error budget 6x
  faster than sustainable. This catches slow degradation.

The generated file `user-api-slos.yaml` is in Sloth format. Deploy it with:
  kubectl apply -f user-api-slos.yaml

Then generate Prometheus recording rules with:
  sloth generate -i user-api-slos.yaml -o prometheus-rules.yaml
  kubectl apply -f prometheus-rules.yaml

Would you like me to help adjust any of these targets based on your actual traffic patterns?
```

---

## Skills vs. Other Approaches

### When to Use Skills vs. Scripts

| Use Case | Scripts | Skills | Why |
|----------|---------|--------|-----|
| One-time automation | ✅ | ❌ | Script is simpler |
| Repeated process with edge cases | ❌ | ✅ | AI handles context |
| Team standard enforcement | ❌ | ✅ | Standards evolve, skills version them |
| Pure deterministic check | ✅ | ❌ | No AI needed |
| Needs explanation | ❌ | ✅ | AI explains why, not just what |

### When to Use Skills vs. MCP Servers

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| **Context cost** | Zero until loaded | Constant (tool schemas) |
| **Discovery** | Metadata in filesystem | Registered in config |
| **Versioning** | Git | External system |
| **Team-specific** | Perfect fit | Overkill |
| **Live queries** | Not designed for this | Perfect fit |
| **Best for** | Team processes, standards | External APIs, live data |

**Example scenarios**:

**Use MCP**: "What's the current CPU usage of this pod?" (live query, changes constantly)

**Use Skill**: "Does this service meet production standards?" (team-specific process, standards change slowly)

### When to Use Skills vs. Just Asking the LLM

| Scenario | Just Ask LLM | Use Skill | Why |
|----------|--------------|-----------|-----|
| "How do I write a Dockerfile?" | ✅ | ❌ | Generic knowledge |
| "What's our team's Dockerfile standard?" | ❌ | ✅ | Team-specific |
| "Explain Kubernetes readiness probes" | ✅ | ❌ | Well-known concept |
| "What does our PRR checklist require?" | ❌ | ✅ | Your standards |
| First time doing something | ✅ | ❌ | Learning mode |
| 10th time doing the same thing | ❌ | ✅ | Codify the pattern |

**The pattern**: If you find yourself explaining the same team standards repeatedly, codify them as a skill.

---

## Building Your Own Skills

### Step-by-Step Guide

**Step 1: Identify the Need**

Look for patterns where:
- You repeatedly explain team standards
- A script exists but needs context to interpret
- Process is partially automated, partially judgment
- Different team members do things differently

**Example candidates**:
- Helm values validation against team conventions
- Terraform module scaffolding with standards
- Incident postmortem template generation
- Cost analysis of Kubernetes manifests

**Step 2: Define the Skill Structure**

```bash
mkdir -p .ai-skills/your-skill-name/{examples,schemas,scripts}
```

**Step 3: Write SKILL.md with Metadata**

```markdown
---
name: your-skill-name
description: One-line description of what it does
version: 1.0.0
category: [operations|security|development|compliance]
tags: [relevant, keywords]
requires_tools: [tools needed to run scripts]
composes_with: [other skills that work with this one]
---

# Your Skill Name

## Purpose
[Why this skill exists]

## When to Use
[Specific scenarios]

## How It Works
[Overview of automated + manual parts]

## AI Instructions
[How the AI should use this skill]

## Examples
[Point to examples directory]

## Related Skills
[Skills that compose with this one]
```

**Step 4: Create Team Standards File (YAML/JSON)**

```yaml
# your-standards.yaml
standards:
  - id: STD-001
    name: Clear standard name
    description: What this standard requires
    rationale: Why it matters
    severity: [blocker|required|recommended]
    check: [automated|manual]
    validation:
      type: [kubernetes|filesystem|custom]
      check: script_function_name
```

**Step 5: Write Automation Script (Optional)**

```python
#!/usr/bin/env python3
"""
Your Skill Automated Checker
"""

def check_standard_001():
    """Check STD-001"""
    # Automated validation logic
    pass

def main():
    # Run checks, output results
    pass

if __name__ == '__main__':
    main()
```

**Step 6: Create Examples**

```
examples/
├── passing-example/
│   ├── input-files
│   └── expected-output
└── failing-example/
    ├── input-files
    └── issues-to-fix
```

**Step 7: Test with AI**

```
1. Navigate to directory with test case
2. Ask AI: "Use the <your-skill-name> skill to check this"
3. Verify AI loads metadata, runs script, interprets results
4. Iterate on instructions in SKILL.md until AI uses it correctly
```

**Step 8: Version and Document**

```bash
git add .ai-skills/your-skill-name/
git commit -m "Add <your-skill-name> skill v1.0.0"
git tag skill-your-skill-name-v1.0.0
```

### Skill Structure Conventions

**File naming**:
- `SKILL.md` - Always uppercase, contains metadata
- `*-requirements.yaml` or `*-standards.yaml` - Lowercase, descriptive
- `check-*.py` or `build-*.py` - Lowercase, verb-based
- `examples/` - Always plural

**Metadata fields** (YAML frontmatter in SKILL.md):
- `name`: Lowercase with hyphens (matches directory name)
- `description`: One clear sentence
- `version`: Semantic versioning (1.0.0)
- `category`: Single category for organization
- `tags`: Array of relevant keywords
- `requires_tools`: Tools needed to run (kubectl, python3, jq, etc.)
- `composes_with`: Skills this works well with

**Standards format**:
```yaml
requirements:
  - id: PREFIX-NNN  # Prefix identifies category, NNN is sequential
    category: logical-grouping
    name: Human-readable name
    description: What is required
    check: automated|manual
    severity: blocker|required|recommended
    rationale: Why this matters
    tiers:  # If tier-based
      tier-1: required|recommended|optional
      tier-2: required|recommended|optional
      tier-3: required|recommended|optional
    validation:  # If automated
      type: check-type
      check: function-name
      params: {}  # Optional parameters
```

### Testing and Iteration

**Test checklist**:
```
□ AI can discover the skill from metadata
□ AI loads full skill content when relevant
□ AI runs automation script correctly
□ AI interprets results with proper context
□ AI explains why requirements matter
□ AI handles edge cases appropriately
□ Examples demonstrate success and failure cases
□ Documentation is clear and complete
```

**Iteration workflow**:
1. Create minimal viable skill
2. Test with real scenario
3. Note where AI struggles or makes mistakes
4. Improve SKILL.md instructions
5. Add missing examples
6. Repeat until AI uses skill correctly

---

## Practical Exercises

### Exercise 1: Customize PRR for Your Team

**Objective**: Adapt the Production Readiness Review skill to your organization's standards.

**Tasks**:
1. Copy `.ai-skills/production-readiness-review/` to your project
2. Edit `prr-requirements.yaml`:
   - Add requirements specific to your team
   - Remove requirements that don't apply
   - Adjust tier requirements based on your standards
   - Update rationale to reflect your context
3. Modify `check-prr.py`:
   - Update automated checks for your environment
   - Add checks for custom requirements
   - Adjust validation logic
4. Create examples from your actual services:
   - One passing service
   - One failing service
5. Test the skill with AI on a real service

**Deliverable**: Working PRR skill customized to your team's needs.

---

### Exercise 2: Test PRR on Real Service

**Objective**: Run the PRR skill against an actual service and interpret results.

**Tasks**:
1. Choose a service deployed in Kubernetes
2. Navigate to the service's repository
3. Ask AI: "Use the production-readiness-review skill to check this service"
4. Review the automated check results
5. Work with AI to assess manual checklist items
6. Create a remediation plan for failures
7. Implement fixes and re-run

**Deliverable**: PRR report with pass/fail status and remediation plan.

---

### Exercise 3: Generate SLOs for a Service

**Objective**: Use the SLO builder skill to create SLOs.

**Tasks**:
1. Run PRR on a service first (establishes tier and type)
2. Ask AI: "Create SLOs for this service"
3. Review the generated SLO targets
4. Ask AI to explain each SLO and error budget
5. Adjust targets if defaults don't fit your service
6. Deploy the SLOs to your cluster
7. Generate Prometheus recording rules with Sloth

**Deliverable**: Deployed SLO definitions and Prometheus rules.

---

### Exercise 4: Create a New Skill from Scratch

**Objective**: Build a skill for a team-specific workflow.

**Choose one of these scenarios** (or create your own):

**Option A: Helm Values Validator**
- Validates Helm values files against team conventions
- Checks required fields, naming patterns, resource limits
- Ensures consistency across environments

**Option B: Incident Postmortem Generator**
- Creates postmortem document from incident notes
- Follows team template
- Includes timeline, root cause, action items

**Option C: Terraform Module Scaffolder**
- Generates Terraform module structure
- Includes team-standard files (variables.tf, outputs.tf, README.md)
- Adds provider configuration and testing setup

**Tasks**:
1. Create skill directory structure
2. Write SKILL.md with metadata and instructions
3. Create standards/templates file (YAML or JSON)
4. Write automation script (if applicable)
5. Create 2-3 examples (passing and failing cases)
6. Test with AI on real or sample data
7. Iterate based on AI's usage

**Deliverable**: Working skill ready for team use.

---

### Exercise 5: Compose Multiple Skills

**Objective**: Demonstrate skills working together in a workflow.

**Scenario**: New service launch workflow

**Tasks**:
1. Use PRR skill to validate production readiness
2. Use SLO builder to generate SLOs based on PRR metadata
3. Use Helm values validator to check configuration
4. Ask AI to create comprehensive launch checklist
5. Execute the workflow on a real or test service

**Deliverable**: Complete launch workflow using composed skills.

---

## Common Pitfalls

### Pitfall 1: Skills Too Broad

**What it looks like**:
```
Skill name: "infrastructure-automation"
Description: "Automates all infrastructure tasks"
```

**Why it fails**:
- Too vague to load at the right time
- Tries to do everything, does nothing well
- Huge context cost when loaded
- Hard to maintain

**The fix**:

Make skills **specific and focused**:
```
✅ Good:
  - production-readiness-review
  - slo-builder
  - helm-values-validator
  - docker-security-scanner

❌ Too broad:
  - kubernetes-helper
  - deployment-automation
  - monitoring-setup
```

**Principle**: One skill, one job. Like Unix tools.

---

### Pitfall 2: Over-Engineering (Script When Skill Not Needed)

**What it looks like**:

You have a simple deterministic task:
- Convert CSV to JSON
- Format Kubernetes manifests
- Calculate resource costs

You create a skill with:
- SKILL.md with extensive instructions
- Standards YAML file
- Examples directory
- 500 lines of Python

**Why it fails**:
- Deterministic tasks don't need AI reasoning
- Just script is simpler and faster
- Maintenance overhead for no benefit

**The fix**:

**Use skills when**:
- AI adds value through reasoning
- Edge cases require context
- Team standards need explanation
- Process is partially manual

**Use scripts when**:
- Pure deterministic transformation
- No context needed
- Same every time
- Simple automation

**Example decision tree**:

"Format Kubernetes YAML files" → Script (pure formatting)

"Validate Kubernetes manifests against team standards" → Skill (judgment required)

---

### Pitfall 3: Not Enough Examples in SKILL.md

**What it looks like**:

SKILL.md says:
```markdown
## How to Use

Run the script and interpret the results.
```

No examples of:
- What good output looks like
- What bad output looks like
- How to handle edge cases

**Why it fails**:
- AI doesn't know how to interpret results
- Can't handle edge cases appropriately
- May miss important context

**The fix**:

Include **concrete examples** in SKILL.md:

```markdown
## Example Usage

### Passing Case

```bash
$ python3 check-prr.py user-api production --tier tier-1

✓ All checks passed
```

AI should respond:
"Your service passes all automated checks. Now let's review manual items..."

### Failing Case

```bash
$ python3 check-prr.py batch-job staging --tier tier-3

✗ [REL-001] Multiple replicas
  Insufficient replicas: 1 (minimum: 2)
```

AI should respond:
"The script reports insufficient replicas. However, since this is a tier-3 batch job,
having 1 replica might be acceptable. Let me ask: Is this a scheduled batch job that
runs periodically? If so, high availability isn't critical and we can mark this as
an acceptable exception."

### Edge Case: Batch Job Doesn't Need HA

```bash
✗ [REL-001] Multiple replicas
```

AI should recognize:
- Batch jobs may run once and exit
- HA is not relevant for CronJobs
- Mark as expected failure with explanation
```

**Principle**: Show AI how to handle success, failure, and edge cases.

---

### Pitfall 4: Missing Rationale in Standards

**What it looks like**:

```yaml
requirements:
  - id: SEC-001
    name: Security context configured
    check: automated
    severity: blocker
```

No explanation of *why* it matters.

**Why it fails**:
- AI can't explain to user why requirement exists
- User doesn't understand context
- Harder to determine when exceptions are reasonable

**The fix**:

**Always include rationale**:

```yaml
requirements:
  - id: SEC-001
    name: Security context configured
    description: Pod security context with runAsNonRoot, readOnlyRootFilesystem
    check: automated
    severity: blocker
    rationale: |
      Defense in depth - limit container privileges to reduce blast radius if
      container is compromised. RunAsNonRoot prevents root exploits, and
      readOnlyRootFilesystem prevents malware from persisting changes.
    tiers:
      tier-1: required
      tier-2: required
      tier-3: required
```

Now AI can explain:
```
The security context requirement is failing. This is a blocker because it provides
defense in depth. If an attacker compromises your container, they won't have root
access and can't write to the filesystem, limiting what they can do.

For a tier-1 customer-facing service, this is non-negotiable. Let me show you how
to fix it...
```

**Principle**: Document the "why" so AI can teach, not just check.

---

### Pitfall 5: Skills Not Versioned

**What it looks like**:

Skills are edited in place with no version tracking:
- Standards change without notice
- Script updated but SKILL.md not updated
- No way to know what version was used

**Why it fails**:
- Can't reproduce past results
- Breaking changes surprise users
- Can't rollback problematic updates

**The fix**:

**Version skills properly**:

```yaml
---
name: production-readiness-review
version: 2.1.0  # Semantic versioning
---
```

**Update version when**:
- Major (3.0.0): Breaking changes to standards or outputs
- Minor (2.1.0): New checks added, backward compatible
- Patch (2.0.1): Bug fixes, no functional changes

**Git tagging**:
```bash
git tag skill-production-readiness-review-v2.1.0
git push --tags
```

**Changelog in SKILL.md**:
```markdown
## Changelog

### 2.1.0 (2024-11-11)
- Added network policy check (SEC-003)
- Updated tier-3 replica requirement to be optional

### 2.0.0 (2024-10-15)
- Breaking: Changed prr-requirements.yaml structure
- Added support for service tiers
- Added rationale field to all requirements
```

**Principle**: Skills are code. Version them like code.

---

## Integration with Earlier Modules

### Module 1: Core Concepts - SELECT Strategy

Skills use the **SELECT** strategy:

**Traditional approach**:
```
"Check if this service is production ready"
[You paste entire PRR checklist into conversation]
[4000 tokens consumed]
```

**Skills approach**:
```
"Use the production-readiness-review skill to check this service"
[AI reads metadata: 50 tokens]
[AI loads full skill when relevant: 5000 tokens]
[Zero tokens when skill not used]
```

**Progressive disclosure** = **SELECT at the right time**.

---

### Module 2: Filesystem Organization

Skills leverage **filesystem as context**:

```
.ai-skills/                          ← Discoverable location
├── production-readiness-review/     ← Skill name = directory name
│   ├── SKILL.md                     ← Metadata for discovery
│   ├── prr-requirements.yaml        ← Standards data
│   ├── check-prr.py                 ← Automation
│   └── examples/                    ← Reference implementations
└── slo-builder/
    ├── SKILL.md
    ├── slo-templates.yaml
    └── build-slos.py
```

**Module 2 taught**: Filesystem structure communicates organization

**Skills apply it**: Standard location (`.ai-skills/`) makes skills discoverable

---

### Module 3: MCP Servers

Skills and MCP serve different purposes:

| Use Case | MCP Server | Skill |
|----------|-----------|-------|
| Live external data (GitHub, Jira, AWS) | ✅ | ❌ |
| Team-specific standards and processes | ❌ | ✅ |
| Real-time queries | ✅ | ❌ |
| Versioned team knowledge | ❌ | ✅ |
| Context cost | Constant | Zero until loaded |

**Skills can wrap MCP**:
```yaml
# skill that uses MCP for live data
name: aws-cost-analyzer
description: Analyze AWS costs against budget
requires_tools: [aws-mcp-server]
```

Skill provides the process/standards, MCP provides the live data.

---

### Module 4: Multi-Tab Orchestration

Skills work across tabs:

**Pattern: Investigation + Implementation**

```
Tab 1 (Blue): Investigation
  "Use production-readiness-review skill to audit this service"
  [Generates findings]

Tab 2 (Green): Implementation
  "Fix the issues found in Tab 1"
  [Loads same skill for reference]
  [Implements fixes]

Tab 3 (Green): Verification
  "Re-run production-readiness-review skill"
  [Verifies fixes]
```

Skills maintain consistency across tabs because they're **filesystem-based**, not in-memory.

---

### Module 5: Patterns and Anti-Patterns

Skills embody safety patterns from Module 5:

**Dry-Run Pattern**:
```bash
python3 check-prr.py my-service production --dry-run
# Shows what would be checked without making changes
```

**Progressive Verification**:
```
1. Dev: Test skill on dev service
2. Review: Apply skill to review environment
3. Prod: Use skill for production launch gates
```

**Read vs Execute**:
- Skills **READ** configuration and state
- Skills **GENERATE** recommendations
- **YOU** execute the fixes

**Accountability**:
> ⚠️ **Accountability**: Skills help AI provide better guidance, but you are still responsible for understanding and verifying all recommendations before executing changes.

---

## Other Skill Ideas

Brief descriptions of additional skills you might build:

### helm-values-validator

**Purpose**: Validate Helm values files against team conventions

**What it checks**:
- Required fields present (image.repository, image.tag, resources)
- Naming conventions (services, deployments, configmaps)
- Resource limits within acceptable ranges
- Environment-specific overrides complete
- Values don't contain secrets or sensitive data

**How AI adds value**:
- Explains why conventions exist
- Suggests fixes for violations
- Handles edge cases (dev vs prod differences)

---

### dockerfile-security-scanner

**Purpose**: Check Dockerfiles for security issues and best practices

**What it checks**:
- Base image not using `latest` tag
- Running as non-root user
- No secrets in build args or ENV
- Multi-stage builds for smaller images
- Minimize layers and cache appropriately
- Health check defined

**How AI adds value**:
- Explains security implications
- Suggests refactoring to fix issues
- Recommends base image alternatives

---

### terraform-module-generator

**Purpose**: Scaffold Terraform modules following team conventions

**What it generates**:
- Standard directory structure
- variables.tf with required variables
- outputs.tf with standard outputs
- README.md template with sections
- examples/ directory with usage
- tests/ directory with Terratest setup

**How AI adds value**:
- Customizes template based on module type (VPC, compute, database)
- Fills in sensible defaults
- Explains conventions and best practices

---

### incident-postmortem-generator

**Purpose**: Create incident postmortem document from notes

**What it creates**:
- Timeline of events
- Root cause analysis
- Impact assessment
- Action items with owners and deadlines
- Lessons learned
- Follow-up tasks

**How AI adds value**:
- Structures messy notes into clear narrative
- Identifies root causes from descriptions
- Generates actionable remediation items
- Suggests preventive measures

---

### k8s-cost-analyzer

**Purpose**: Analyze Kubernetes manifests for cost optimization

**What it checks**:
- Resource requests vs actual usage
- Over-provisioned workloads
- Idle deployments (0 replicas)
- Expensive storage classes
- Unused persistent volumes
- Cost per service/namespace

**How AI adds value**:
- Explains cost implications
- Suggests right-sizing
- Prioritizes optimization opportunities by impact

---

### changelog-formatter

**Purpose**: Transform git commits into team changelog format

**What it does**:
- Groups commits by type (feat, fix, chore, docs)
- Formats in team's changelog style
- Generates summary for release notes
- Links to issues/PRs

**How AI adds value**:
- Interprets commit messages
- Writes human-friendly descriptions
- Highlights breaking changes
- Suggests version bump (major/minor/patch)

---

## Summary

### The Skills Pattern Solves

1. **Token budget constraints**: Progressive disclosure loads only when needed
2. **Inconsistent standards**: Version-controlled team knowledge
3. **Scripts can't explain**: AI adds reasoning and context
4. **Generic LLM knowledge**: Skills encode your team's specific practices
5. **Forgotten expertise**: Codified in discoverable, self-documenting packages

### The Value Triangle

```
     Scripts (Deterministic)
            /\
           /  \
          /    \
         /      \
    AI           Team Standards
(Flexible)       (Versioned)
```

Skills combine all three: automated validation + flexible reasoning + versioned standards.

### When to Create a Skill

Create a skill when:
- ✅ You're explaining the same standards repeatedly
- ✅ A script exists but needs context to interpret
- ✅ Process is partially automated, partially judgment
- ✅ Team members do things differently and should be consistent
- ✅ AI can add value through reasoning about edge cases

Don't create a skill when:
- ❌ Task is purely deterministic (just use a script)
- ❌ One-time automation (not repeated)
- ❌ Generic knowledge (LLM already knows this)
- ❌ You're over-engineering a simple task

### Key Takeaways

1. **Progressive disclosure**: Load context only when needed
2. **Composability**: Skills work together naturally through filesystem and metadata
3. **Platform agnostic**: Pattern works with any AI that can read files and run code
4. **Version everything**: Skills are code, treat them as such
5. **Document the why**: Rationale enables AI to teach, not just check

---

**Next Module**: [Patterns and Anti-Patterns →](05-patterns-and-antipatterns.md)

**Related Modules**:
- [Core Concepts](01-core-concepts.md) - SELECT strategy and progressive disclosure
- [Filesystem Organization](02-filesystem-organization.md) - Context through structure
- [MCP Servers](03-mcp-servers.md) - When skills vs MCP
