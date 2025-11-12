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
