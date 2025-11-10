# Module 6: Practical Patterns

Real-world workflows and examples for common SRE tasks.

---

## Foundational Safety Patterns

Before diving into specific workflows, let's establish the core patterns that make AI-assisted work both powerful and safe. These aren't just best practices - they're the foundation for everything else in this module.

### The Creation vs Verification Advantage

**The fundamental insight**: Creation is time-consuming. Verification is faster.

Many SRE tasks are hard to create but easier to verify. AI excels at generation, turning hours of writing into minutes. You still verify carefully - that part doesn't change - but you've eliminated the time-consuming creation step.

#### The Practical Advantage

**Traditional workflow:**
- You write the solution: Hours
- You verify it works: Minutes

**AI-assisted workflow:**
- AI generates the solution: Minutes
- You verify it works: Same time as before

**Result**: You're much more productive without sacrificing safety.

#### Real Examples with Time Comparisons

**Example 1: Terraform Module**

Task: Write a Terraform module to provision a VPC with public/private subnets, NAT gateways, and route tables.

**Without AI**:
- Create: 2-4 hours of writing, looking up syntax, debugging
- Verify: 30 minutes of testing and review
- **Total: 2.5-4.5 hours**

**With AI**:
- Create: 5 minutes (AI generates code)
- Verify: Still 30 minutes of review and testing
- **Total: 35 minutes**

**Time saved**: 2-4 hours
**Safety preserved**: Same verification process
**Your productivity**: 4-7x increase

**Example 2: Database Migration Script**

Task: Write SQL migration with data transformation and integrity checks.

**Without AI**:
- Research best practices: 30 minutes
- Write migration logic: 1-2 hours
- Add rollback procedures: 30 minutes
- Write verification queries: 30 minutes
- Test and debug: 1 hour
- **Total: 3.5-4.5 hours**

**With AI**:
- Describe requirements: 5 minutes
- AI generates complete script: 5 minutes
- Review and understand: 30 minutes
- Test and verify: 1 hour (same as before)
- **Total: 1 hour 40 minutes**

**Time saved**: 2-3 hours
**Safety preserved**: Same testing process
**Learning bonus**: AI explains patterns you can reuse

**Example 3: Kubernetes RBAC Configuration**

Task: Set up RBAC for new service account with appropriate permissions.

**Without AI**:
- Read RBAC documentation: 45 minutes
- Write ServiceAccount, Role, RoleBinding: 1 hour
- Debug permission issues: 1-2 hours
- Test access patterns: 30 minutes
- **Total: 3-4 hours**

**With AI**:
- Describe requirements: 5 minutes
- AI generates manifests with explanations: 5 minutes
- Review for security issues: 20 minutes
- Test access patterns: 30 minutes (same as before)
- **Total: 1 hour**

**Time saved**: 2-3 hours
**Safety preserved**: Same security review
**Understanding**: AI explains RBAC concepts while building

#### Why This Works

Verification doesn't require perfect knowledge. You're checking:
- Does this logic make sense?
- Are there obvious security issues?
- Does it handle edge cases?
- Does it work when tested?

These are easier questions than "How do I build this from scratch?"

#### Maintaining Safety Through Verification

Your verification process should be thorough:

**Code Review Checklist**:
- [ ] Do I understand what this code does?
- [ ] Are there security vulnerabilities?
- [ ] Does it handle errors appropriately?
- [ ] Are there hardcoded credentials or secrets?
- [ ] Does it match our team's standards?
- [ ] Can I explain this to a colleague?

**Testing Checklist**:
- [ ] Tested in dev/staging environment
- [ ] Edge cases considered
- [ ] Rollback plan exists
- [ ] Monitoring in place to detect issues

**The Standard**:
Apply the same rigor you would to human-written code. AI-generated doesn't mean "skip the review."

> ⚠️ **Accountability**: You are responsible for understanding and verifying AI-generated code before deploying it to production. Fast generation doesn't mean fast deployment - maintain your testing and review standards.

#### The Productivity Multiplier

When you eliminate the creation bottleneck:

**Old constraint**: Your typing speed and knowledge breadth
**New constraint**: Your verification speed and judgment

You can tackle more ambitious tasks because the creation cost dropped from hours to minutes. Your judgment and verification skills become the valuable parts.

**This is empowering, not risky** - as long as you maintain verification standards.

---

### Learning While Working: AI as Teacher

**Core principle**: You don't need to know how to do something before you start. The AI can teach you as you go.

This is transformative for SREs who encounter new tools, unfamiliar systems, or technologies outside their expertise.

#### Traditional vs AI-Assisted Learning

**Traditional approach**:
1. Encounter unfamiliar task
2. Read documentation for hours
3. Try to implement
4. Debug when it fails
5. Eventually succeed

**AI-assisted approach**:
1. Encounter unfamiliar task
2. Ask AI to explain and guide you through it
3. Learn the concepts as you implement
4. Verify each step works
5. Understand what you built and why

#### AI Knows Shell Commands (Really Well)

The AI has seen countless shell commands, CLI tools, and automation patterns. It will suggest:
- Tools you didn't know existed
- Flags and options you've never used
- Combinations that solve your problem elegantly
- Alternatives you hadn't considered

**Lean into this.** Let AI expand your toolkit.

#### The Discovery Pattern

**Example: Learning find with Multiple Conditions**

**You:**
```
I need to find all files in /var/log that were modified in the last 7 days
and are larger than 100MB. I usually just use find with -mtime but I'm not
sure how to combine that with a size check.
```

**AI:**
```
You can combine multiple conditions in find:

find /var/log -type f -mtime -7 -size +100M

Let me break this down:
- -type f: Only files (not directories)
- -mtime -7: Modified within last 7 days (negative means "less than")
- -size +100M: Larger than 100 megabytes

If you want to see the sizes in human-readable format:

find /var/log -type f -mtime -7 -size +100M -exec ls -lh {} \;

This executes 'ls -lh' on each file found. The {} is replaced with the
filename, and \; terminates the -exec command.
```

**You learned**:
- How to combine find conditions
- The -mtime negative number syntax
- The -size flag with +100M format
- How to use -exec with find
- A pattern you can reuse

#### The "Explain Piece by Piece" Pattern

**Always ask for explanations when learning something new.**

❌ **Ineffective**: "Write a script to back up the database"
```
[Gets script, doesn't understand it]
```

✅ **Effective**: "Write a script to back up the database. Explain what each section does and why it's necessary."
```
[Gets script with educational comments]
[Learns backup patterns]
[Can modify for future use]
```

#### The "Teach Me First" Pattern

✅ **Effective approach**:
```
I need to set up RBAC for a new service account in Kubernetes, but I've
never done this before. Can you explain the components I'll need
(ServiceAccount, Role, RoleBinding) and what each one does? Then help me
write the manifests.
```

**Result**: You understand the architecture, not just copy/paste YAML.

#### Teaching Request Patterns

Frame your requests to trigger educational responses:

❌ "Fix this"
✅ "I don't understand why this is failing. Can you explain what's happening and teach me how to debug this type of issue?"

❌ "Write a backup script"
✅ "I need to implement backups but I'm not familiar with the best practices for PostgreSQL backups. Can you explain the options and help me choose the right approach? Then we'll write the script together."

❌ "Set up monitoring"
✅ "I need to set up Prometheus monitoring for our service. I've never configured Prometheus before. Can you explain the key concepts (metrics, labels, scraping) and then help me write the configuration?"

#### Tools You Might Discover

When working with AI, you'll encounter:

**Text processing**:
- `jq` for JSON manipulation
- `yq` for YAML processing
- `awk` and `sed` patterns you didn't know
- `column` for formatting output

**System administration**:
- `systemd` commands beyond start/stop
- `journalctl` advanced filtering
- `ss` instead of `netstat`
- `lsof` patterns for debugging

**Kubernetes**:
- `kubectl` flags you've never used
- Custom output formats with `-o jsonpath`
- Field selectors and label selectors
- Debug techniques with ephemeral containers

**Networking**:
- `tcpdump` for packet capture
- `mtr` for network diagnostics
- `curl` advanced options
- `openssl` commands for certificate inspection

**Ask AI to teach you these tools as you need them.**

#### Manual First, Automate Second

**For unfamiliar tasks, walk through manually before automating.**

Don't automate what you don't understand yet. Learn the process first.

**Step 1: Learn the process**
```
You: "I need to rotate the TLS certificates for our ingress controller, but
I've never done this before. Can you walk me through the manual process step
by step? I want to understand what's happening before I automate it."

AI: [Provides step-by-step manual instructions with explanations]

You: [Execute each step in dev environment]
You: [Understand what each step does]
You: [Verify it works]
```

**Step 2: Automate what you learned**
```
You: "Now that I understand the process, can you help me write a script that
automates these steps? Include dry-run mode and comments explaining each
section based on what we just did manually."

AI: [Generates script based on the manual process you just learned]

You: [Review script - you recognize the steps]
You: [Run with --dry-run in dev]
You: [Verify automation works]
```

**Step 3: Progressive deployment**
```
Dev environment: Test the automation, verify it works
Review environment: Run automation, verify no issues
Production: Run automation with confidence
```

> ⚠️ **Accountability**: Learning while working doesn't mean skipping verification. Understanding what the code does is part of your responsibility before executing it in production.

#### Real-World Example: Database Migration

**Scenario**: You need to migrate a PostgreSQL database to a new schema version, but you've never done this manually before.

**Phase 1: Learning (Dev)**

```
You: "I need to migrate our PostgreSQL database from schema v1 to v2. I've
never done a Postgres migration manually. Can you explain the process and
walk me through it step by step in our dev database first?"

AI: [Explains migration concepts: backup, schema changes, data
transformation, verification]

You: "Okay, let's do this manually in dev so I understand each step. First,
how do I back up the database?"

AI: [Provides backup command with explanation]

You: [Executes backup, verifies it worked]

You: "Good, backup created. Now what?"

AI: [Guides through schema changes]
```

**You learn**:
- How to backup PostgreSQL
- How to apply schema changes
- How to verify migration worked
- What can go wrong and how to rollback

**Phase 2: Script Generation (Still in Dev)**

```
You: "Now that I understand the process, help me write a migration script.
Include:
- Dry-run mode that shows what would happen
- Automatic backup before migration
- Verification checks after each major step
- Rollback instructions if something fails
- Verbose logging of all actions"

AI: [Generates comprehensive migration script]

You: [Reviews script - recognizes all the steps from manual process]
You: [Runs with --dry-run]
You: "The dry run shows it would drop the 'old_status' column. That's correct."
You: [Runs actual script in dev]
You: [Verifies migration succeeded]
```

**Phase 3: Review Environment**

```
You: [Runs same script in review with --dry-run first]
You: [Verifies expected changes]
You: [Runs actual migration]
You: [Tests application against migrated database]
You: [Confirms everything works]
```

**Phase 4: Production**

```
You: [Schedules maintenance window]
You: [Runs script in production]
You: [Monitors closely]
You: [Success!]
```

**Outcome**: You successfully migrated the database AND you learned how to do PostgreSQL migrations. Next time will be even easier.

#### Key Takeaways

1. **AI is an excellent teacher** - It can explain as it helps
2. **Ask for explanations** - "Explain piece by piece" should be standard
3. **Discover new tools** - AI knows tools you don't; ask it to teach you
4. **Manual before automated** - Understand the process first
5. **Learning doesn't skip verification** - Understanding is part of accountability

---

### The Dry-Run Pattern

**Principle**: Every operational script should have a dry-run mode. This is not optional.

Dry-run is crucial for:
- **Safety**: See what would happen without doing it
- **Learning**: Understand the actions without risk
- **Verification**: Confirm it does what you expect
- **Communication**: Show others what will happen

#### Requesting Dry-Run From AI

When asking AI to generate scripts, make dry-run explicit:

✅ **Effective request**:
```
Generate a script that [does the task]. Include:
- A dry-run mode that shows what would happen without making changes
- Verbose output explaining each step
- Comments describing what each section does
```

#### Example: Cleanup Script with Dry-Run

**Request:**
```
I need a script to delete Kubernetes pods in the 'staging' namespace that
have been in 'Completed' status for more than 30 days. Include a dry-run
mode so I can verify what it will delete before running it for real.
```

**AI generates:**
```bash
#!/bin/bash
# Delete old completed pods in staging namespace
# Usage: ./cleanup-pods.sh [--dry-run]

NAMESPACE="staging"
DRY_RUN=false

# Parse arguments
if [[ "$1" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "DRY RUN MODE - No pods will be deleted"
  echo "========================================"
fi

# Get completed pods older than 30 days
# The --field-selector status.phase=Succeeded finds completed pods
# jq filters based on completion timestamp
PODS=$(kubectl get pods -n "$NAMESPACE" \
  --field-selector status.phase=Succeeded \
  -o json | \
  jq -r --arg date "$(date -d '30 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.items[] | select(.status.containerStatuses[0].state.terminated.finishedAt < $date) | .metadata.name')

if [ -z "$PODS" ]; then
  echo "No old completed pods found in namespace $NAMESPACE"
  exit 0
fi

echo "Found pods to delete:"
echo "$PODS"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "DRY RUN: Would delete $(echo "$PODS" | wc -l) pods"
  echo "Run without --dry-run to actually delete these pods"
  exit 0
fi

# Actually delete pods
echo "Deleting pods..."
for pod in $PODS; do
  echo "Deleting pod: $pod"
  kubectl delete pod "$pod" -n "$NAMESPACE"
done

echo "Cleanup complete"
```

**You can now**:
1. Run with `--dry-run` to see what it would do
2. Read the comments to understand how it works
3. Verify the logic in a safe environment
4. Learn the kubectl and jq patterns for future use

#### What Good Dry-Run Output Looks Like

```bash
$ ./deploy.sh --dry-run
DRY RUN MODE - No changes will be made
=========================================

Would perform the following actions:

1. Build Docker image: myapp:v2.1.0
   - Using Dockerfile at ./Dockerfile
   - Tagging as: registry.example.com/myapp:v2.1.0

2. Push image to registry
   - Target: registry.example.com/myapp:v2.1.0

3. Update Kubernetes deployment
   - Namespace: production
   - Deployment: myapp
   - Current image: myapp:v2.0.5
   - New image: myapp:v2.1.0

4. Wait for rollout to complete
   - Timeout: 5 minutes
   - Will watch pod status

Run without --dry-run to execute these actions.
```

**You know exactly what will happen before it happens.**

#### The Dry-Run Checklist

Every operational script should have:

- [ ] `--dry-run` flag that prevents actual changes
- [ ] Clear output showing what WOULD happen
- [ ] Verbose mode explaining each action
- [ ] Same code path as real execution (just skips the actual changes)
- [ ] Exit code indicating what would have been done

#### Dry-Run for Different Types of Operations

**Kubernetes Operations**:
```bash
if [ "$DRY_RUN" = true ]; then
  echo "Would run: kubectl apply -f manifest.yaml"
  kubectl apply -f manifest.yaml --dry-run=client
else
  kubectl apply -f manifest.yaml
fi
```

**Database Operations**:
```sql
-- Dry run: Use transactions and rollback
BEGIN TRANSACTION;

-- Perform all operations
UPDATE users SET status = 'active' WHERE last_login > NOW() - INTERVAL '90 days';

-- In dry-run mode: Show what would change, then rollback
SELECT 'Would update ' || COUNT(*) || ' users' FROM users
WHERE last_login > NOW() - INTERVAL '90 days';

ROLLBACK;  -- Change to COMMIT for real execution
```

**File Operations**:
```bash
if [ "$DRY_RUN" = true ]; then
  echo "Would delete: $file"
else
  echo "Deleting: $file"
  rm "$file"
fi
```

> ⚠️ **Accountability**: Dry-run testing is part of due diligence. Running scripts in production without first testing with dry-run is negligent. Always dry-run first.

#### Integration with Progressive Verification

Dry-run fits naturally into progressive verification:

1. **Dev**: Dry-run to understand, then execute
2. **Review**: Dry-run to verify, then execute
3. **Prod**: Dry-run final check, then execute

Each environment gets a dry-run verification before real execution.

#### Key Takeaways

1. **Dry-run is mandatory** for operational scripts
2. **Request it explicitly** when asking AI to generate scripts
3. **Good dry-run output** shows exactly what would happen
4. **Same logic, different action** - dry-run uses same code path
5. **Part of verification** - dry-run is step one of testing

---

### Progressive Verification Workflow

**Pattern**: Dev → Review → Prod

This is how you safely promote new automation and changes through environments, building confidence at each stage.

#### Why Progressive Verification Works

**You're not blindly running AI-generated code in production.**

You've:
- ✅ Learned what the task involves
- ✅ Understood the automation
- ✅ Tested with dry-run
- ✅ Verified in dev
- ✅ Validated in staging
- ✅ Built confidence through progression

Each stage reduces risk and increases confidence.

#### The Three Stages

**Phase 1: Development Environment**
- Learn the task manually
- Have AI generate automation with dry-run
- Test in dev with dry-run first
- Run actual automation in dev
- Verify results thoroughly
- Fix any issues discovered

**Phase 2: Review/Staging Environment**
- Run same automation in review environment
- Verify it works in environment closer to prod
- Identify any environment-specific issues
- Test with realistic data volumes
- Refine automation if needed

**Phase 3: Production Environment**
- Run automation in production
- Monitor closely
- Have rollback plan ready
- Document what you learned
- Update runbooks with insights

#### What to Verify at Each Stage

**Development**:
- [ ] Logic is correct
- [ ] Handles expected inputs
- [ ] Error handling works
- [ ] Dry-run output is accurate
- [ ] No hardcoded credentials
- [ ] Comments explain what's happening

**Review/Staging**:
- [ ] Works with production-like data
- [ ] Performance is acceptable
- [ ] No environment-specific failures
- [ ] Integrates with dependent systems
- [ ] Monitoring detects issues
- [ ] Rollback procedure works

**Production**:
- [ ] Final dry-run verification
- [ ] Maintenance window scheduled if needed
- [ ] Team notified
- [ ] Monitoring active
- [ ] Rollback plan ready
- [ ] Execute and monitor closely

#### Real-World Example: Helm Chart Update

**Scenario**: Updating resource limits across all microservices.

**Stage 1: Development**

```
You: "I need to update CPU and memory limits for our microservices. Let's
start in dev. Generate a script that updates the helm values for each
service and re-deploys. Include dry-run mode."

AI: [Generates script]

You: [Reviews script]
You: [Runs ./update-limits.sh --dry-run in dev]
You: "Dry run looks good. Shows updating 5 services."
You: [Runs ./update-limits.sh in dev]
You: [Monitors pod restarts, verifies new limits]
You: [Confirms applications still work]
```

**Issues found**:
- One service OOMKills with new limit (adjust values)
- Need to add health check wait time (update script)

**Stage 2: Review/Staging**

```
You: [Runs updated script with --dry-run in staging]
You: [Verifies changes look correct]
You: [Runs ./update-limits.sh in staging]
You: [Monitors with production-like traffic]
You: [Confirms performance is acceptable]
You: [Tests for 24 hours]
```

**Issues found**:
- None, but learned staging handles rollout well

**Stage 3: Production**

```
You: [Schedules change during low-traffic window]
You: [Notifies team]
You: [Runs ./update-limits.sh --dry-run in prod]
You: "Dry run confirms 5 services, same as dev and staging"
You: [Runs ./update-limits.sh in prod]
You: [Monitors dashboards closely]
You: [All services healthy]
You: [Success!]
```

#### Building Confidence Through Progression

**After Dev**: "It works in principle"
**After Review**: "It works with realistic conditions"
**Before Prod**: "I'm confident this will work"

Each stage builds on the previous:
- Dev proves the logic
- Review proves the scalability
- Prod executes with confidence

#### When to Skip Stages (Rarely)

**Never skip verification entirely**, but you might compress stages for:

**Low-risk changes**:
- Documentation updates
- Monitoring dashboard changes
- Non-critical configuration tweaks

**Still maintain**:
- Dry-run testing
- Peer review
- Rollback plan

**High-risk changes always go through all stages**.

#### Integration with Learning Pattern

Progressive verification works beautifully with learning while working:

1. **Learn in dev** (manual process)
2. **Automate in dev** (with AI help)
3. **Refine in review** (real conditions)
4. **Execute in prod** (with confidence)

You've learned, automated, tested, and deployed safely.

> ⚠️ **Accountability**: Skipping progressive verification for high-risk changes is professional negligence. Each stage exists to catch issues before production. Use appropriate rigor based on change risk.

#### Key Takeaways

1. **Dev → Review → Prod** is the standard promotion path
2. **Each stage builds confidence** and catches different issues
3. **Verify specific things** at each stage (logic, scale, production-readiness)
4. **Learn and refine** as you progress through environments
5. **Never skip verification** for high-risk changes

---

### The Script Generation Pattern

**Core pattern**: Instead of having AI execute, have it generate scripts you verify and run.

This is one of the safest patterns for production work because it separates generation from execution and enables verification.

#### Why Script Generation Works

**Benefits**:
1. **Auditability**: Script can be reviewed by multiple people
2. **Version control**: Check the script into git
3. **Testing**: Run in non-prod first
4. **Peer review**: Subject to normal code review process
5. **Repeatability**: Same script can run multiple times
6. **Documentation**: Script IS the documentation of what was done

#### The Pattern

❌ **Risky approach**:
```
"Fix the production database by running these commands"
```

✅ **Safe approach**:
```
"Generate a script that would fix the production database. Include:
- Comments explaining each step
- Safety checks before destructive operations
- Rollback procedures if something fails
- Verbose output so I can see what's happening
I'll review the script and test it in staging before running in prod."
```

#### Example: Database Migration Script

**Request:**
```
I need to migrate data from the old users table to the new users_v2 table
in production. The migration needs to:
- Copy all active users
- Update foreign key references in 3 other tables
- Verify data integrity
- Run within a transaction we can rollback

Can you generate a SQL script I can review? Include comments explaining
each step and add checks to verify the migration worked.
```

**AI generates:**
```sql
-- Migration script: users to users_v2
-- Author: Generated by AI, reviewed by [YOUR NAME]
-- Date: [DATE]
-- IMPORTANT: Test in staging first!

BEGIN TRANSACTION;

-- Step 1: Verify current state
-- Expected: users table exists with active users
SELECT COUNT(*) as active_users FROM users WHERE status = 'active';
-- [Manually verify this count matches expectations]

-- Step 2: Copy active users to new table
-- This preserves the original data until we verify
INSERT INTO users_v2 (id, email, name, created_at)
SELECT id, email, name, created_at
FROM users
WHERE status = 'active';

-- Verify: Same count in both tables
SELECT
  (SELECT COUNT(*) FROM users WHERE status = 'active') as original_count,
  (SELECT COUNT(*) FROM users_v2) as new_count;
-- [Manually verify counts match]

-- Step 3: Update foreign key references
-- orders table
UPDATE orders
SET user_id_v2 = user_id
WHERE user_id IN (SELECT id FROM users_v2);

-- payments table
UPDATE payments
SET user_id_v2 = user_id
WHERE user_id IN (SELECT id FROM users_v2);

-- sessions table
UPDATE sessions
SET user_id_v2 = user_id
WHERE user_id IN (SELECT id FROM users_v2);

-- Step 4: Verify foreign key updates
SELECT
  'orders' as table_name,
  COUNT(*) as updated_count
FROM orders
WHERE user_id_v2 IS NOT NULL;

SELECT
  'payments' as table_name,
  COUNT(*) as updated_count
FROM payments
WHERE user_id_v2 IS NOT NULL;

SELECT
  'sessions' as table_name,
  COUNT(*) as updated_count
FROM sessions
WHERE user_id_v2 IS NOT NULL;

-- Step 5: Final verification
-- Check for orphaned references
SELECT COUNT(*) as orphaned_orders FROM orders WHERE user_id_v2 IS NULL;
-- [Should be 0 or expected number of deleted users]

-- If everything looks good, COMMIT;
-- If anything is wrong, ROLLBACK;
```

**You review:**
- Logic is sound
- Comments help you understand
- Verification steps are included
- You can test in staging
- You can walk through in incident post-mortem if needed

**You execute:**
- In staging first (within transaction, rollback to test)
- In production during maintenance window
- You run it, you own it
- But AI saved you hours of writing

#### Verbose Comments Pattern

**Tokens are cheap. Use them.**

When asking AI to generate scripts for production:

✅ "Add verbose comments explaining what each section does and why"

✅ "Include comments that explain the safety checks"

✅ "Add comments noting what to verify at each step"

**Cost**: A few hundred extra tokens
**Benefit**: Significantly easier verification and long-term maintenance

**Why verbose comments matter**:
1. **Review**: Easier for you and peers to review
2. **Learning**: You understand what it does
3. **Maintenance**: Future you thanks present you
4. **Incident response**: Clear what the script was supposed to do
5. **Onboarding**: New team members can understand

#### Peer Review Integration

AI-generated scripts should go through the same review process as human-written code.

**The workflow**:

1. **AI generates** the solution
2. **You review** for correctness
3. **Create PR** with AI-generated code
4. **Peers review** like any other code
5. **Test** in non-prod environment
6. **Approve and merge**
7. **Execute** through normal deployment process

**Important**: Note in the PR that it's AI-generated. This is transparency, not hiding anything.

```markdown
## Description
Database migration script for users to users_v2 table.

## Testing
- [ ] Tested in dev environment
- [ ] Validated with transaction rollback in staging
- [ ] Verified data counts match
- [ ] Checked foreign key integrity

## Notes
Initial script generated by AI, reviewed and modified for our specific
requirements. All verification steps tested in staging.

## Rollback Plan
Script runs in transaction. If any verification fails, ROLLBACK instead
of COMMIT. Original users table remains untouched until verification passes.
```

> ⚠️ **Accountability**: Peer review of AI-generated code is not optional for production changes. Just because AI wrote it doesn't mean it skips your team's review process. Treat it like any other code.

#### Scripts for Different Scenarios

**Deployment Script**:
```bash
#!/bin/bash
# Deploy application version to production
# Usage: ./deploy.sh <version> [--dry-run]

# Generated by AI, reviewed by: [YOUR NAME]
# Date: [DATE]

VERSION=$1
DRY_RUN=false

if [[ "$2" == "--dry-run" ]]; then
  DRY_RUN=true
fi

# [Verbose comments explaining each step]
# [Safety checks]
# [Dry-run mode]
# [Rollback instructions]
```

**Cleanup Script**:
```python
#!/usr/bin/env python3
"""
Clean up old CloudWatch log groups
Generated by AI, reviewed by: [YOUR NAME]
"""

# [Verbose comments]
# [Dry-run mode]
# [Safety checks for production log groups]
# [Confirmation prompts]
```

**Configuration Update**:
```bash
#!/bin/bash
# Update nginx configuration across all servers
# Generated by AI, reviewed by: [YOUR NAME]

# [Verbose comments]
# [Backup current config first]
# [Test new config before applying]
# [Rollback procedure if nginx fails to reload]
```

#### When Scripts Are Better Than Direct Execution

**Use scripts for**:
- Changes to production systems
- Multi-step operations
- Changes that need peer review
- Operations you might need to repeat
- Changes that should be documented
- Operations with rollback requirements

**Direct commands might be okay for**:
- Quick reads from production
- One-time investigations
- Non-destructive queries
- Development environment work

> ⚠️ **Accountability**: For any change that could cause an incident, generate a script and review it. The few minutes of creating a script could save hours of incident response.

#### Key Takeaways

1. **Generate scripts, not executions** for production work
2. **Verbose comments are cheap** and make review easier
3. **Peer review still applies** to AI-generated code
4. **Version control your scripts** like any code
5. **Test before prod** using progressive verification
6. **Scripts are documentation** of what was done

---

### Read vs Execute Pattern

**Safe pattern for production:**

✅ AI can READ from production
✅ AI can GENERATE scripts for production
❌ AI should NOT EXECUTE against production (you execute after review)

This establishes clear, safe boundaries for AI assistance in production environments.

#### Why This Works

**Reading is safe** - no changes, just gathering information
**Generating is safe** - you review before executing
**Direct execution is risky** - no verification step

#### Safe Reading Patterns

AI can safely read from production to help you understand what's happening:

**Database queries**:
```
✅ "Query the production database to show me all users who haven't logged in
in 90 days. I need to plan a cleanup."

✅ "Show me the current table sizes in the production database. I'm
investigating disk usage."

✅ "Find all database connections from the api service in the last hour."
```

**Kubernetes inspection**:
```
✅ "Check the Kubernetes events for namespace 'api' to see if there are any
warning signs about the recent deployment."

✅ "Show me which pods in production are using more than 80% of their memory
limits."

✅ "List all CronJobs in the production cluster and when they last ran."
```

**Log analysis**:
```
✅ "Read the CloudWatch logs for the lambda function to find the error pattern
that started at 14:30 today."

✅ "Analyze the nginx access logs to see which endpoints have the highest
error rates."

✅ "Search application logs for exceptions related to the payment service."
```

**Configuration inspection**:
```
✅ "Show me the current helm values for the user-api service in production."

✅ "Read the terraform state to see what's actually deployed in AWS."

✅ "Check the current nginx configuration on the production load balancers."
```

**Why reading is valuable**:
- Helps you understand the current state
- Gathers information for decision-making
- No risk of changing anything
- Can inform what actions to take

#### Safe Generation Patterns

AI can generate scripts and commands for you to review and execute:

**Generating cleanup commands**:
```
✅ "Generate a script that would delete those inactive users. Include a dry-run
mode and verbose logging. I'll review it before running."

Result: Script you can review, test in staging, then execute in prod
```

**Generating rollback procedures**:
```
✅ "Create a kubectl command I could use to rollback that deployment if needed.
I want to have it ready just in case."

Result: Command ready to use if needed, but you decide when
```

**Generating configuration changes**:
```
✅ "Generate the terraform changes needed to add a new security group rule. I'll
review and apply through our normal PR process."

Result: Terraform code you can review and test
```

**Generating migration scripts**:
```
✅ "Generate a SQL migration script for the schema change. Include rollback
procedures and verification queries. I'll test in staging first."

Result: Script to review, test, and eventually execute
```

#### Unsafe Execution Patterns

**What to avoid**:

❌ **Direct execution without review**:
```
"Delete all inactive users"
"Rollback the production deployment"
"Run this migration script in production"
"Scale down the user-api deployment"
```

**Why these are risky**:
- No review step
- No verification
- No dry-run testing
- Can't easily undo
- No documentation of what was done

#### The Principle: AI Prepares, You Execute

**AI helps you prepare the action. You decide to execute it.**

This keeps you in control while leveraging AI's ability to generate solutions quickly.

**The workflow**:
1. AI reads production to understand current state
2. AI generates script/commands to solve the problem
3. You review the generated solution
4. You test in non-prod
5. You execute in production
6. You verify the results

You maintain control and accountability at every step.

#### Example: Production Database Cleanup

**Safe approach using Read and Generate**:

```
Step 1 - Read (Safe):
You: "Query the production database to show all sessions older than 90 days.
Group by month so I can see the distribution."

AI: [Executes SELECT query, shows results]

You: "Okay, there are 2.3 million old sessions. Most are from 6+ months ago."

Step 2 - Generate (Safe):
You: "Generate a script to delete sessions older than 90 days. Requirements:
- Delete in batches of 1000 to avoid long locks
- Include dry-run mode showing how many would be deleted
- Log progress after each batch
- Include verification queries
I'll test this in staging before running in production."

AI: [Generates script with all requirements]

Step 3 - Review (Your responsibility):
You: [Reviews script]
You: [Checks batch size, dry-run logic, verification]

Step 4 - Test (Your responsibility):
You: [Runs with --dry-run in staging]
You: [Verifies it would delete correct records]
You: [Runs actual script in staging]
You: [Verifies staging cleanup worked]

Step 5 - Execute (Your decision):
You: [Schedules maintenance window]
You: [Runs in production]
You: [Monitors progress]
```

**What happened**:
- AI read safely from production (Step 1)
- AI generated the solution (Step 2)
- You reviewed and controlled execution (Steps 3-5)
- You maintained accountability throughout

#### Exceptions: When AI Can Execute Safely

**Read-only operations** in any environment:
- Queries that don't modify data
- Inspecting configurations
- Analyzing logs
- Checking status

**Non-production environments** (with more flexibility):
- Development environments
- Personal test environments
- Isolated sandbox environments

**Even then**: Understand what it's doing. Don't blindly execute.

> ⚠️ **Accountability**: The boundary between reading and executing is your safety line. AI reads and generates, you review and execute. This pattern keeps you accountable and in control.

#### Integration with Other Patterns

**Read + Generate + Progressive Verification**:
1. Read from prod to understand
2. Generate script to solve
3. Test in dev (execute yourself)
4. Test in staging (execute yourself)
5. Run in prod (execute yourself)

**Read + Generate + Peer Review**:
1. Read from prod to understand
2. Generate script to solve
3. Create PR with generated script
4. Team reviews
5. You execute after approval

These patterns layer together naturally.

#### Key Takeaways

1. **AI reads from prod safely** - gathering information is low-risk
2. **AI generates for you to execute** - maintains verification step
3. **Direct execution requires review** - you decide when to run
4. **Clear boundaries** - read and generate are safe, execute requires control
5. **You maintain accountability** - by controlling execution

---

## Practical Workflows

Now that we've established the foundational safety patterns, let's look at specific workflows for common SRE tasks. These workflows combine the principles above into real-world scenarios.

### Pattern 1: The Investigation Agent

**Use case**: Debugging a production issue that requires exploration and follow-up questions.

### Setup
```bash
# Start Codex in the relevant service directory
cd /company/SRE/helm/charts/my-service/

# Initial prompt
Context: Production pods for my-service are crashlooping
Available info:
- Recent logs saved to /tmp/my-service-crash-logs.txt
- Helm chart in current directory
- kubectl access to production cluster

Task: Investigate the root cause of the crashloop
```

### Workflow
The agent stays alive for iterative investigation:

```
You: "Check the logs for any obvious errors"
Agent: [analyzes logs, finds OOM killer messages]

You: "Look at the current memory limits in our helm values"
Agent: [shows values.yaml with limits: memory: "512Mi"]

You: "Compare to what other similar services use"
Agent: [searches other charts, finds they use 1Gi]

You: "Check our actual memory usage in Prometheus"
Agent: [queries metrics, shows average 800Mi usage]

You: "Create a fix and explain the changes needed"
Agent: [proposes updated values with justification]
```

**Key technique**: Keep the agent alive with all context loaded. Don't start fresh sessions for each question.

---

## Pattern 2: Parallel Updates with Coordination

**Use case**: Making related changes across multiple repositories or components.

### Setup: Blue-Green Cluster Swap

**Task breakdown**:
- Update helm chart A
- Update helm chart B (same repo as A)
- Update cluster sync script
- Search for related work items
- Document all changes

### Tab Layout
```
Tab 1 (Green):  Helm Chart A
  Location: /company/SRE/helm/charts/
  Command: git worktree add ../charts-worktree-a
  Task: Update chart A for new cluster

Tab 2 (Green):  Helm Chart B  
  Location: /company/SRE/helm/charts/
  Command: git worktree add ../charts-worktree-b
  Task: Update chart B for new cluster

Tab 3 (Blue):   Sync Script
  Location: /company/SRE/scripts/
  Task: Update cluster-sync.sh to handle helm changes

Tab 4 (Yellow): Work Item Search
  Location: /company/SRE/notes/
  Task: Search local work item replica for related items
  Status: Stays open as reference

Tab 5 (Green):  Master Coordination
  Location: /company/SRE/
  Task: Aggregate results and create wiki documentation
```

### Coordination Workflow

**Step 1**: Work happens in parallel (Tabs 1-3)

**Step 2**: Aggregate in master tab (Tab 5)
```
I've completed these changes:

Chart A: [paste summary from Tab 1]
Chart B: [paste summary from Tab 2]  
Sync Script: [paste summary from Tab 3]
Related Work Items: [reference from Tab 4]

Please:
1. Create a comprehensive wiki document for these changes
2. Generate a deployment checklist
3. Identify any dependencies I may have missed
```

**Step 3**: Use agent output to update wiki via Azure DevOps MCP

**Why it works**: Each tab maintains focused context. Manual aggregation ensures you review all changes before creating final documentation.

---

## Pattern 3: The Document Analysis Agent

**Use case**: Working with large reference documents (architecture docs, RFCs, vendor documentation).

### Setup
```bash
cd /company/SRE/docs/

# Load the document
Here's our 40-page Kubernetes architecture document [attach or paste]

Keep this loaded. I'll be asking questions about it throughout the day.
```

### Usage Patterns

**Reference queries**:
```
"What's our standard for pod resource requests?"
"Where do we document our backup procedures?"
"What's the process for emergency rollbacks?"
```

**Comparison queries**:
```
"Compare our current ingress config to what the architecture doc recommends"
"Does our implementation match the documented disaster recovery plan?"
```

**Implementation guidance**:
```
"I need to add a new service. According to our architecture doc, what 
do I need to configure for monitoring, logging, and alerting?"
```

**Why it works**: Document stays loaded in context. No need to re-upload or re-explain for each question.

---

## Pattern 4: The Dual Data Store Pattern

**Use case**: Fast local searches combined with live updates.

### Setup: Work Item Management

**Local replica** (for searching):
```
/company/SRE/notes/work-items/
├── my-work-items.json
├── team-work-items.json
└── last-updated.txt
```

**Azure DevOps MCP** (for updating):
- Connected via MCP server
- Used for writes and critical reads

### Workflow

**Tab 1: Search (Local)**
```
Search my local work item replica for all open items related to "helm chart updates"

[Fast search through JSON file]
→ Found items: 12345, 12347, 12389
```

**Tab 2: Update (Live)**
```
Using Azure DevOps MCP:

Update work item 12345:
- Status: In Progress → Done
- Add comment: "Updated ingress-nginx to 4.8, tested in staging"
- Link to related item: 12347
```

**Why both**: Local for fast searches, live for accurate writes.

**Maintenance**: Update local replica weekly or after major changes
```
"Regenerate my work item replica with current data from Azure DevOps"
```

---

## Pattern 5: The Handoff Chain

**Use case**: Long-running work that exceeds context window capacity.

### Monitoring Context Usage

Most tools show context usage. Keep an eye on it - when it starts feeling cluttered or you notice it climbing, consider a handoff.

### Handoff Workflow

**Step 1**: When context is getting full, prepare to handoff
```
Give me a handoff prompt I can copy into a new Codex session to continue this work.
```

**Step 2**: Agent generates comprehensive handoff
```
We're migrating the user-api service to the new Kubernetes cluster.

Location: /company/SRE/helm/charts/user-api/
Current branch: feature/cluster-migration

Completed:
- Updated Chart.yaml to version 2.1.0
- Modified values.yaml for new cluster endpoints
- Updated ingress configuration for new domain
- Tested template rendering with helm template
- Created git worktree at ../user-api-migration/

Remaining tasks:
- Update production values override (values/production.yaml)
- Test deployment in staging environment  
- Update monitoring dashboards for new cluster
- Document changes in wiki

Key decisions made:
- Using ClusterIP service instead of LoadBalancer (cost optimization)
- Maintaining existing resource limits (no changes needed)
- Added new health check endpoint configuration

Known issues:
- Staging namespace doesn't exist yet (needs to be created first)
- Some ConfigMaps reference old cluster name (need updating)

Files modified:
- Chart.yaml
- values.yaml
- templates/deployment.yaml (health check)
- templates/ingress.yaml (domain update)

Next immediate action: Create staging namespace, then test deployment.
```

**Step 3**: Copy entire handoff into new session

**Step 4**: Continue work in fresh context

**Why it works**: Agent knows its own context better than you do. It generates comprehensive handoffs automatically.

---

## Pattern 6: The Multi-Repo Investigation

**Use case**: Tracking down issues that span multiple repositories.

### Scenario
Database connection errors in production. Could be:
- Application code (Dev repo)
- Kubernetes configuration (SRE helm charts)
- Terraform infrastructure (SRE terraform)
- Network policies (SRE ansible)

### Approach: Fan-Out Investigation

```
Tab 1: Application code
  Location: /company/Dev/user-api/
  Task: Check database connection config and retry logic

Tab 2: Kubernetes config
  Location: /company/SRE/helm/charts/user-api/
  Task: Verify secrets, connection strings, and network policies

Tab 3: Infrastructure
  Location: /company/SRE/terraform/azure-infrastructure/
  Task: Check database firewall rules and network configuration

Tab 4: Network policies
  Location: /company/SRE/ansible/
  Task: Review any recent network policy changes

Tab 5: Aggregation
  Location: /company/SRE/
  Task: Collect findings and determine root cause
```

**Each tab** investigates independently, then reports findings to Tab 5 for synthesis.

---

## Pattern 7: The Runbook Generator

**Use case**: Convert an incident resolution into a reusable runbook.

### During Incident

**Investigation tab**:
```
Keep this tab open during the incident.
Document each step as we troubleshoot.

Issue: High database CPU usage
Investigation steps:
[Each command and finding gets added to context]
```

### After Incident

**Same tab**:
```
Based on our troubleshooting session above, create a runbook for future incidents of this type.

Format:
- Symptoms and alerts
- Investigation steps
- Common causes
- Resolution procedures
- Prevention measures

Save to: /company/SRE/notes/runbooks/database-high-cpu.md
```

**Why it works**: All context from the actual incident is already loaded. The runbook reflects real troubleshooting, not theoretical steps.

---

## Pattern 8: The Terraform Drift Detective

**Use case**: Identify differences between actual Azure resources and terraform state.

### Setup: Local Azure Inventory

**Build searchable inventory**:
```bash
cd /company/SRE/notes/inventory/

# Generate current state
Create a script that:
1. Queries all Azure resources via az cli
2. Outputs JSON with: name, type, location, resource group, key properties
3. Saves to azure-resources.json
4. Includes timestamp in last-updated.txt
```

### Drift Detection Workflow

**Tab 1: Inventory current state**
```
Run the Azure inventory script
Save output to azure-resources.json
```

**Tab 2: Compare to terraform**
```
Location: /company/SRE/terraform/azure-infrastructure/

Compare azure-resources.json to our terraform state.

Report:
- Resources in Azure but not in terraform
- Resources in terraform but not in Azure  
- Configuration differences for resources in both

Focus on: VMs, AKS clusters, storage accounts, network resources
```

**Tab 3: Resolution**
```
For each drift identified:
1. Determine if Azure or terraform is correct
2. Generate terraform to import unmanaged resources, OR
3. Generate commands to remove resources that shouldn't exist, OR
4. Generate terraform updates to match desired state
```

---

## Pattern 9: The Emergency Rollback

**Use case**: Fast rollback with documentation for post-mortem.

### Setup
```
Tab 1 (Red): Execute rollback
  - Immediate action
  - Rolling back helm deployment

Tab 2 (Yellow): Document actions  
  - Parallel documentation
  - Captures each step taken

Tab 3 (Blue): Investigation
  - Why did we need to rollback?
  - What broke?
```

### Tab 1: Execution
```
URGENT: Need to rollback user-api deployment

Current version: 2.1.0 (deployed 10 minutes ago)
Previous version: 2.0.3 (stable)
Location: /company/SRE/helm/charts/user-api/

Execute rollback to 2.0.3 now.
Show me each command before running.
```

### Tab 2: Concurrent Documentation
```
Document rollback in progress:

Time: [timestamp]
Service: user-api  
Reason: [paste error messages]
Action: Rolling back 2.1.0 → 2.0.3
Executed by: [your name]

[Keep updating as rollback progresses]
```

### Tab 3: Post-Rollback Analysis
```
Load the diff between versions 2.0.3 and 2.1.0

Analyze what changed and what likely caused the issue
Look for: configuration changes, dependency updates, code changes in critical paths
```

**Why separate tabs**: Rollback happens urgently in Tab 1. Documentation happens in parallel in Tab 2. Investigation can start immediately in Tab 3 without waiting for rollback completion.

---

## Pattern 10: The Configuration Validator

**Use case**: Validate changes across all environments before deploying.

### Setup
```
/company/SRE/helm/charts/my-service/
├── values.yaml (defaults)
├── values/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
```

### Validation Workflow
```
I'm about to change the resource limits in the my-service helm chart.

Please:
1. Show current resource limits in all environment value files
2. After I make changes, validate that:
   - All environments have consistent structure
   - Production has higher limits than staging
   - No environment is missing required fields
   - All syntax is valid YAML
3. Generate helm template output for each environment to catch any issues
```

**Catches**: Syntax errors, missing overrides, environment inconsistencies

---

## Anti-Patterns to Avoid

### ❌ The Everything Tab
One tab trying to do investigation + fixes + testing + documentation + wiki updates

**Why it fails**: Context becomes cluttered, focus is lost, hard to track what's been done

**Instead**: Separate tabs for separate concerns

---

### ❌ The Context-Free Request
```
"Fix the broken thing"
```

**Why it fails**: No information about what's broken, where it is, or what "fixed" looks like

**Instead**: Always provide context
```
The my-service deployment in production is crashlooping.
Logs at /tmp/my-service.log show OOM errors.
Helm chart at /company/SRE/helm/charts/my-service/
Current memory limit: 512Mi
```

---

### ❌ The Stale Data Store
You built a local Azure inventory 3 months ago and never updated it.

**Why it fails**: Agent makes decisions based on outdated information

**Instead**: 
- Update inventories regularly
- Include "last updated" timestamp
- Verify critical info against live sources when it matters

---

## Choosing the Right Pattern

| Scenario | Recommended Pattern |
|----------|-------------------|
| Investigating production issue | Investigation Agent |
| Multi-part infrastructure update | Parallel Updates with Coordination |
| Working with large docs | Document Analysis Agent |
| Managing work items | Dual Data Store |
| Long-running migration | Handoff Chain |
| Cross-repo troubleshooting | Multi-Repo Investigation |
| Post-incident documentation | Runbook Generator |
| Finding terraform drift | Drift Detective |
| Emergency response | Emergency Rollback |
| Pre-deployment validation | Configuration Validator |

---

## Next Steps

- Try one pattern with a real task this week
- Document what worked and what didn't
- Share your experience with the team

**[← Back to Multi-Tab Orchestration](04-multi-tab-orchestration.md)** | **[Common Pitfalls →](06-common-pitfalls.md)**
