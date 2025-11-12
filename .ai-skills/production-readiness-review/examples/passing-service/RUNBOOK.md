# User API Runbook

On-call procedures for the User API service.

## Quick Response

### Service is Down (All replicas failing)

1. **Check deployment status**:
   ```bash
   kubectl get pods -n production -l app=user-api
   kubectl describe pod <failing-pod> -n production
   ```

2. **Common causes**:
   - Database connection failure → Check PostgreSQL connectivity
   - Redis unavailable → Check Redis cluster status
   - Recent deployment → Rollback to previous version

3. **Immediate mitigation**:
   ```bash
   # Rollback to previous version
   helm rollback user-api -n production
   ```

4. **Escalation**: If rollback doesn't resolve in 5 minutes, page Engineering Manager

### High Error Rate (>1%)

1. **Check error logs**:
   ```bash
   kubectl logs -n production -l app=user-api --since=10m | grep ERROR
   ```

2. **Common causes**:
   - Database query timeouts
   - Invalid authentication tokens
   - Rate limiting triggered

3. **Investigation**:
   - Check Grafana dashboard for error patterns
   - Review recent code changes
   - Check database slow query log

### High Latency (p99 >500ms)

1. **Check resource utilization**:
   ```bash
   kubectl top pods -n production -l app=user-api
   ```

2. **Common causes**:
   - CPU throttling
   - Database slow queries
   - External API timeouts
   - Redis cache misses

3. **Quick wins**:
   - Scale up replicas: `kubectl scale deployment user-api --replicas=5 -n production`
   - Check database connection pool exhaustion
   - Review Redis hit rate

## Failure Scenarios

### Database Connection Failures

**Symptoms**: 500 errors, logs show "connection refused"

**Root causes**:
- Database pod restarted
- Network policy blocking traffic
- Connection pool exhausted

**Resolution**:
1. Verify database pods are running
2. Check network policies allow traffic from user-api namespace
3. Restart user-api pods to refresh connection pool

### Authentication Failures

**Symptoms**: 401 errors, logs show "invalid token"

**Root causes**:
- JWT secret rotated without updating deployment
- Clock skew between services
- Auth service unavailable

**Resolution**:
1. Verify JWT_SECRET is current in Kubernetes secret
2. Check auth service health
3. Restart pods to pick up new secret

### Memory Leaks

**Symptoms**: Pods restarting frequently, OOMKilled in events

**Root causes**:
- Unclosed database connections
- Large result sets not paginated
- Memory profiling needed

**Resolution**:
1. Reduce replica count temporarily to spread load
2. Increase memory limits as temporary fix
3. Create incident ticket for investigation
4. Schedule profiling session with dev team

## Health Checks

### Liveness Probe
- Endpoint: `GET /health/live`
- Expected: 200 OK
- Failure action: Restart pod

### Readiness Probe
- Endpoint: `GET /health/ready`
- Expected: 200 OK
- Checks: Database connectivity, Redis connectivity
- Failure action: Remove from load balancer

## Dependencies

- **PostgreSQL**: user-db cluster (critical)
- **Redis**: cache cluster (critical)
- **Auth Service**: authentication-api (critical)

## Metrics to Monitor

- `http_requests_total` - Total requests
- `http_request_duration_seconds` - Request latency
- `http_requests_errors_total` - Error count
- `db_connection_pool_active` - Active DB connections
- `redis_hits_total` - Cache hit rate

## Escalation Path

1. **Primary On-Call**: Platform Team (auto-paged)
2. **Secondary**: Engineering Manager (manual page if >30min)
3. **Executive**: CTO (manual page if customer-impacting >1hr)

## Recent Incidents

- 2024-10-15: Database connection pool exhaustion - Increased pool size
- 2024-09-22: Memory leak from unclosed connections - Fixed in v2.3.1
- 2024-08-10: High latency from N+1 queries - Added eager loading

See full incident history in wiki.
