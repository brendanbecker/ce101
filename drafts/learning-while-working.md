# Learning While Working: AI as Teacher

## The Core Principle

**You don't need to know how to do something before you start. The AI can teach you as you go.**

This is transformative for SREs who encounter new tools, unfamiliar systems, or technologies outside their expertise.

Traditional approach:
1. Encounter unfamiliar task
2. Read documentation for hours
3. Try to implement
4. Debug when it fails
5. Eventually succeed

AI-assisted approach:
1. Encounter unfamiliar task
2. Ask AI to explain and guide you through it
3. Learn the concepts as you implement
4. Verify each step works
5. Understand what you built and why

## AI Knows Shell Commands (Really Well)

The AI has seen countless shell commands, CLI tools, and automation patterns. It will suggest:
- Tools you didn't know existed
- Flags and options you've never used
- Combinations that solve your problem elegantly
- Alternatives you hadn't considered

**Lean into this.** Let AI expand your toolkit.

### Example: Discovery Pattern

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

**You learned:**
- How to combine find conditions
- The -mtime negative number syntax
- The -size flag with +100M format
- How to use -exec with find
- A pattern you can reuse

## The Explanation Pattern

**Always ask for explanations when learning something new.**

### Pattern: "Explain piece by piece"

❌ "Write a script to back up the database"
```
[Gets script, doesn't understand it]
```

✅ "Write a script to back up the database. Explain what each section does and
why it's necessary."
```
[Gets script with educational comments]
[Learns backup patterns]
[Can modify for future use]
```

### Pattern: "Teach me first, then help me implement"

✅ "I need to set up RBAC for a new service account in Kubernetes, but I've
never done this before. Can you explain the components I'll need (ServiceAccount,
Role, RoleBinding) and what each one does? Then help me write the manifests."

**Result**: You understand the architecture, not just copy/paste YAML.

## The Dry-Run Pattern

**Every script AI generates should have a dry-run mode.**

This is crucial for:
- Safety (see what would happen without doing it)
- Learning (understand the actions without risk)
- Verification (confirm it does what you expect)

### Requesting Dry-Run

When asking AI to generate scripts:

✅ "Generate a script that [does the task]. Include:
- A dry-run mode that shows what would happen without making changes
- Verbose output explaining each step
- Comments describing what each section does"

### Example: Cleanup Script with Dry-Run

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
  echo "DRY RUN: Would delete ${PODS} pods"
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

**You can now:**
1. Run with `--dry-run` to see what it would do
2. Read the comments to understand how it works
3. Verify the logic in a safe environment
4. Learn the kubectl and jq patterns for future use

## The Step-by-Step Pattern

**For unfamiliar tasks, ask AI to guide you through step by step.**

Don't automate what you don't understand yet. Walk through it manually first.

### Pattern: Manual First, Automate Second

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

## The Progressive Verification Workflow

**Dev → Review → Prod**

This is how you safely promote new automation:

### Phase 1: Development
- Ask AI to teach you the task
- Walk through manually to understand
- Have AI generate automation with dry-run
- Test in dev environment with dry-run
- Run actual automation in dev
- Verify results thoroughly

### Phase 2: Review/Staging
- Run same automation in review environment
- Verify it works in environment closer to prod
- Identify any environment-specific issues
- Refine automation if needed

### Phase 3: Production
- Run automation in production
- Monitor closely
- Have rollback plan ready
- Document what you learned

### Why This Works

**You're not blindly running AI-generated code in production.**

You've:
- ✅ Learned what the task involves
- ✅ Understood the automation
- ✅ Tested with dry-run
- ✅ Verified in dev
- ✅ Validated in staging
- ✅ Built confidence through progression

## Real-World Example: Database Migration

**Scenario**: You need to migrate a PostgreSQL database to a new schema version, but you've never done this manually before.

### Step 1: Learning Phase (Dev)

```
You: "I need to migrate our PostgreSQL database from schema v1 to v2. I've
never done a Postgres migration manually. Can you explain the process and
walk me through it step by step in our dev database first?"

AI: [Explains migration concepts: backup, schema changes, data transformation,
verification]

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

### Step 2: Script Generation (Still in Dev)

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

### Step 3: Review Environment

```
You: [Runs same script in review with --dry-run first]
You: [Verifies expected changes]
You: [Runs actual migration]
You: [Tests application against migrated database]
You: [Confirms everything works]
```

### Step 4: Production

```
You: [Schedules maintenance window]
You: [Runs script in production]
You: [Monitors closely]
You: [Success!]
```

**Outcome**: You successfully migrated the database AND you learned how to do
PostgreSQL migrations. Next time will be even easier.

## Learning Opportunities

### Tools You Might Discover

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

## The Teaching Request Pattern

Frame your requests to trigger educational responses:

❌ "Fix this"
✅ "I don't understand why this is failing. Can you explain what's happening
and teach me how to debug this type of issue?"

❌ "Write a backup script"
✅ "I need to implement backups but I'm not familiar with the best practices
for PostgreSQL backups. Can you explain the options and help me choose the
right approach? Then we'll write the script together."

❌ "Set up monitoring"
✅ "I need to set up Prometheus monitoring for our service. I've never
configured Prometheus before. Can you explain the key concepts (metrics,
labels, scraping) and then help me write the configuration?"

## Dry-Run as Standard Practice

**Make dry-run mode a requirement for all operational scripts.**

### The Dry-Run Checklist

Every script should have:
- [ ] `--dry-run` flag that prevents actual changes
- [ ] Clear output showing what WOULD happen
- [ ] Verbose mode explaining each action
- [ ] Same code path as real execution (just skips the actual changes)

### Good Dry-Run Output

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

## Combining Learning and Safety

The beautiful thing about this pattern:

**Learning** → Understanding → Confidence → **Safety**

When you:
1. Ask AI to teach you
2. Walk through manually
3. Generate automation with dry-run
4. Test progressively through environments

You get:
- ✅ Knowledge of how things work
- ✅ Confidence in the automation
- ✅ Safety through verification
- ✅ Skills for next time

## Key Takeaways

1. **AI is an excellent teacher** - It can explain as it helps
2. **Ask for explanations** - "Explain piece by piece" should be standard
3. **Dry-run is mandatory** - Every script should have safe testing mode
4. **Manual before automated** - Understand the process first
5. **Progressive verification** - Dev → Review → Prod
6. **Learn while working** - Each task teaches you something new
7. **Discover new tools** - AI knows tools you don't; ask it to teach you

## Practical Exercise

Pick a task you need to do but don't fully understand how:

1. **Ask AI to teach you the manual process**
   - "Explain step by step how to..."
   - Execute manually in dev
   - Verify you understand

2. **Generate automation with dry-run**
   - "Now help me automate this with dry-run mode"
   - Review the script
   - Understand what it does

3. **Progressive testing**
   - Dry-run in dev
   - Execute in dev
   - Promote to review
   - Eventually production

4. **Reflect on what you learned**
   - New tools?
   - New patterns?
   - Skills for future use?

---

**Remember**: Every task is an opportunity to learn. AI can teach you while helping you accomplish your goals. The dry-run pattern keeps you safe while you learn.
