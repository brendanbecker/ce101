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
