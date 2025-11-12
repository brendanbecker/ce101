# User API Service

A tier-1 HTTP API service for user management.

## Overview

This service provides REST API endpoints for user CRUD operations. It is customer-facing and classified as tier-1 (critical).

## Architecture

- **Type**: HTTP REST API
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: OAuth 2.0 with JWT

## Endpoints

- `GET /api/v1/users` - List users
- `GET /api/v1/users/{id}` - Get user details
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Configuration

Environment variables:
- `DATABASE_URL` - PostgreSQL connection string (from secret)
- `REDIS_URL` - Redis connection string (from secret)
- `JWT_SECRET` - JWT signing secret (from secret)
- `LOG_LEVEL` - Logging level (default: INFO)

## Monitoring

- Prometheus metrics exposed at `/metrics`
- ServiceMonitor configured for automatic scraping
- Grafana dashboard: "User API Overview"
- Alerts configured for:
  - High error rate (>1%)
  - High latency (p99 >500ms)
  - Low availability (<99.9%)

## Deployment

Deployed via Helm chart in `production` namespace.

Replicas: 3 (tier-1 requirement)

Resource limits:
- CPU: 500m request, 1000m limit
- Memory: 512Mi request, 1Gi limit

## On-Call

Primary on-call: Platform Team
Escalation: Engineering Manager → CTO

Runbook: See RUNBOOK.md for troubleshooting procedures.
