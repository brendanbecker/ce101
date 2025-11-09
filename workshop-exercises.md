# Workshop Exercises

Hands-on practice activities for Context Engineering 101.

---

## Exercise 1: Transform Your Prompts (20 minutes)

**Objective**: Learn to provide complete context in your prompts.

### Part A: Before and After

**Basic Version**: "Update the Kubernetes deployment"

**Enhanced Version**:
```
I need to update the my-service Kubernetes deployment to increase replicas.

Location: /company/SRE/helm/charts/my-service/templates/deployment.yaml
Current state: 3 replicas
Desired state: 5 replicas
Reason: Traffic increased 40% based on metrics

Please:
1. Show current replica configuration
2. Update to 5 replicas
3. Verify no HPA conflicts
```

### Part B: Your Turn

Pick a task from last week. Write a context-rich prompt for it.

**Review checklist**:
- [ ] Includes specific file paths
- [ ] Explains what and why
- [ ] Provides relevant context
- [ ] States success criteria

---

## Exercise 2: Multi-Tab Planning (30 minutes)

**Objective**: Break down complex tasks into isolated agents.

### Scenario: Service Migration

**Task**: Migrate user-api to new Kubernetes cluster

**Subtasks**:
- Update helm chart
- Update terraform
- Update monitoring  
- Test in staging
- Document changes

**Your Tab Design**:
```
Tab 1: [purpose, location]
Tab 2: [purpose, location]
...
```

**Example Solution**:
```
Tab 1 (Green): Helm updates - /company/SRE/helm/charts/user-api/
Tab 2 (Green): Terraform updates - /company/SRE/terraform/
Tab 3 (Blue): Monitoring review - stays open as reference
Tab 4 (Green): Master coordination - aggregates and documents
```

---

## Exercise 3: Build a Data Store (45 minutes)

**Objective**: Create a searchable local inventory.

### Choose Your Project:

**Option A: Runbook Index**
```
/notes/runbooks/
├── incident-response.md
├── database-failover.md
└── index.json (searchable metadata)
```

**Option B: Azure Resource Inventory**
```
/notes/inventory/
├── azure-resources.json
├── last-updated.txt
└── README.md
```

**Option C: Work Item Replica**
```
/notes/work-items/
├── my-items.json
├── last-updated.txt
```

### Implementation Steps:

1. Design structure: What fields needed?
2. Choose format: JSON, Markdown, both?
3. Build extraction script
4. Test searchability
5. Plan update frequency

### Validation:
- Can you search it quickly?
- Is it human-readable?
- Easy to update?

---

## Exercise 4: Handoff Practice (20 minutes)

**Objective**: Generate effective handoff prompts.

### Steps:

1. Start a session, do 5-10 exchanges
2. Prompt: "Give me a handoff prompt to continue this work"
3. Review handoff - does it include:
   - Location and files
   - Work completed
   - Remaining tasks
   - Key decisions
   - Next action
4. Test in new session

---

## Exercise 5: Pattern Application (60 minutes)

**Objective**: Apply a real pattern to your work.

### Choose Pattern:
- Investigation Agent
- Parallel Updates
- Document Analysis
- Handoff Chain

### Your Task:
1. Select real work task
2. Apply chosen pattern
3. Execute with AI assistance
4. Document: What worked? What didn't?

---

## Exercise 6: Live Demo Prep (30 minutes)

**For Workshop Leaders**

Prepare a live demo showing:

1. **Bad example**: Vague prompt, poor results
2. **Good example**: Context-rich prompt, great results
3. **Multi-tab workflow**: Break down real task
4. **Handoff technique**: Generate and use handoff

### Demo Script Template:

```
"Let me show you what I used to do..."
[Show basic prompt, explain limitations]

"Now watch what happens with context engineering..."
[Show enhanced prompt, explain each element]

"For complex tasks, I use multiple tabs..."
[Demonstrate tab setup and coordination]

"And when context fills up..."
[Show handoff prompt generation]
```

---

---

## Exercise 7: Space Jam Theory - Attempting the Complex (30 minutes)

**Module/Concept**: Module 1 - Space Jam Theory

**Objective**: Build confidence in tackling complex tasks by breaking them down with AI assistance.

**Scenario**: You've been avoiding a complex infrastructure task because it seems overwhelming. Examples:
- Multi-cluster Kubernetes migration
- Complete CI/CD pipeline redesign
- Database sharding implementation
- Zero-downtime service mesh migration

### Activity

**Step 1: Pick Your "Too Complex" Task** (5 minutes)
```
Choose a real task you've been avoiding because it feels too complex for AI assistance.

Write down:
- What's the task?
- Why does it feel too complex?
- What are you afraid might go wrong?
```

**Step 2: Break It Down with AI** (15 minutes)
```
Open a new AI session and try this prompt:

"I need to [your complex task]. I've never done this before and it feels
overwhelming. I'm not sure where to start or what the major risks are.

Can you help me:
1. Break this down into phases
2. Identify the biggest risks at each phase
3. Suggest how to test/verify each phase works
4. Point out what I should learn manually before automating

I don't need you to do it all—I need help thinking it through step by step."
```

**Step 3: Evaluate the Breakdown** (5 minutes)
```
Review what AI suggested:
- Does the breakdown make sense?
- Are the phases manageable?
- Do you understand the risks better?
- Can you see yourself starting Phase 1?
```

**Step 4: Start Phase 1** (5 minutes)
```
Actually start the first phase—even just the planning:
- What files do you need to read?
- What systems do you need to understand?
- What's the smallest first step?

You don't have to complete it today. Just start.
```

### Success Criteria

- [ ] You picked a task you were avoiding
- [ ] AI helped break it into phases
- [ ] Each phase feels more manageable than the whole
- [ ] You can articulate the first 3 steps
- [ ] You feel less intimidated about starting

### Reflection Questions

1. Was the task actually as complex as you thought?
2. What surprised you about AI's breakdown?
3. Which phase do you feel most confident about?
4. What changed from "too complex" to "let's try phase 1"?
5. Will you approach complex tasks differently now?

**Key Insight**: If you can dream it, you can at least start it. The complexity is usually in your head, not the task itself.

---

## Exercise 8: Natural Language Communication Practice (25 minutes)

**Module/Concept**: Module 1 - Natural Language Communication

**Objective**: Internalize effective AI communication patterns by rewriting actual prompts.

**Scenario**: Transform command-style prompts into natural language that triggers better AI responses.

### Activity

**Part A: Before and After Comparisons** (10 minutes)

Take these command-style prompts and rewrite them using natural language patterns:

**Prompt 1 - Command Style**:
```
Fix the failing CI pipeline
```

**Your Natural Language Version**:
```
[Write your improved version here using the 5-point pattern:
1. What you're trying to accomplish
2. What you know and what you're unsure about
3. What you've tried
4. Where relevant information is
5. What success looks like]
```

**Prompt 2 - Command Style**:
```
Update terraform to use new VPC
```

**Your Natural Language Version**:
```
[Write your improved version]
```

**Prompt 3 - Command Style**:
```
Check if pods are OOMKilling
```

**Your Natural Language Version**:
```
[Write your improved version]
```

**Part B: Real Work Examples** (10 minutes)

Find 2-3 prompts you actually used this week (check your AI history):

**Original Prompt 1**:
```
[Paste your actual prompt]
```

**Improved Version**:
```
[Rewrite with natural language, context, uncertainty where appropriate]
```

**Original Prompt 2**:
```
[Paste your actual prompt]
```

**Improved Version**:
```
[Rewrite with natural language]
```

**Part C: Test the Difference** (5 minutes)

Pick one rewritten prompt and actually test it:
- Try your improved version in a new AI session
- Compare the response quality to what you remember
- Note what's different

### Success Criteria

- [ ] Rewrote at least 5 prompts using natural language
- [ ] Included context (what, why, where)
- [ ] Expressed uncertainty where appropriate
- [ ] Provided success criteria
- [ ] Tested at least one and saw improvement

### Reflection Questions

1. Which pattern was hardest to apply? (Context? Uncertainty? Success criteria?)
2. Did expressing uncertainty feel weird at first?
3. What improved most in AI responses?
4. Will this style feel natural with practice?
5. Can you apply this to asking colleagues for help too?

**Key Insight**: AI works best when you talk like you're explaining to a knowledgeable coworker. Natural language > commands.

---

## Exercise 9: Dry-Run Script Generation (40 minutes)

**Module/Concept**: Module 6 - The Dry-Run Pattern

**Objective**: Make dry-run mode standard practice by generating and testing operational scripts safely.

**Scenario**: You need a script for a production operation. Practice requesting dry-run mode and verifying output.

### Activity

**Step 1: Choose Your Operation** (5 minutes)

Pick a real operational task that needs automation:
- Cleanup old resources (pods, logs, files)
- Update configuration across services
- Database maintenance operation
- Certificate rotation
- Backup verification

**Step 2: Request Script with Dry-Run** (10 minutes)

Use this prompt pattern:

```
I need a script that [describes your operation].

Requirements:
- Include a --dry-run mode that shows what would happen without making changes
- Verbose output explaining each step
- Comments describing what each section does
- Safety checks before destructive operations
- Clear indication when running in dry-run vs real mode

This will run in production, so dry-run testing is critical.
```

**Step 3: Review Generated Script** (10 minutes)

Check the script for:
- [ ] Has --dry-run flag
- [ ] Shows what WOULD happen in dry-run
- [ ] Same code path for dry-run and real execution
- [ ] Verbose output explaining actions
- [ ] Comments for understanding
- [ ] Safety checks present

**Step 4: Test Dry-Run Mode** (10 minutes)

Actually run the script:
```bash
# In dev or staging environment
./your-script.sh --dry-run

# Verify output shows:
# - What would be changed
# - How many items affected
# - Clear indication this is dry-run
# - Instruction to run without flag for real execution
```

**Step 5: Verify Logic** (5 minutes)

Based on dry-run output:
- Does it target the right resources?
- Are the counts what you expect?
- Any unexpected items in the list?
- Logic errors or edge cases?

### Success Criteria

- [ ] Generated script with dry-run mode
- [ ] Dry-run flag actually prevents changes
- [ ] Output clearly shows what would happen
- [ ] Tested in safe environment first
- [ ] Verified logic is correct
- [ ] Feel confident about real execution

### Reflection Questions

1. Did dry-run catch any logic errors?
2. Would you have noticed those errors without dry-run?
3. How much more confident are you after seeing dry-run output?
4. Will you request dry-run mode for all operational scripts now?
5. What would have happened if you ran this in prod without testing?

**Key Insight**: Dry-run is not optional—it's due diligence. Always test scripts safely before production execution.

---

## Exercise 10: Progressive Verification Workflow (60 minutes)

**Module/Concept**: Module 6 - Progressive Verification Workflow

**Objective**: Practice the Dev → Review → Prod pattern with a real infrastructure change.

**Scenario**: You need to update a configuration or deploy a change across environments. Walk through progressive verification.

### Activity

**Choose a Real Change** (5 minutes):
- Helm chart value update
- Configuration file change
- Resource limit adjustment
- New monitoring rule
- Database parameter update

**Phase 1: Development Environment** (20 minutes)

```
Tasks:
1. Make the change in dev
2. Request AI generate any needed automation
3. Run with --dry-run first
4. Execute the change
5. Verify it works
6. Fix any issues discovered

Document:
- What worked immediately?
- What needed adjustment?
- What did you learn?
```

**What to Verify in Dev**:
- [ ] Logic is correct
- [ ] Handles expected inputs
- [ ] Error handling works
- [ ] No hardcoded credentials
- [ ] Dry-run output matches reality

**Phase 2: Review/Staging Environment** (20 minutes)

```
Tasks:
1. Apply same change to staging
2. Run with --dry-run first (again!)
3. Execute the change
4. Test with production-like conditions
5. Monitor for 15-30 minutes
6. Note any environment-specific issues

Document:
- Any differences from dev?
- Performance acceptable?
- Integration issues?
- Monitoring working?
```

**What to Verify in Staging**:
- [ ] Works with production-like data
- [ ] Performance is acceptable
- [ ] No environment-specific failures
- [ ] Monitoring detects changes
- [ ] Rollback procedure works

**Phase 3: Production Preparation** (15 minutes)

```
Don't execute yet—just prepare:

Tasks:
1. Run dry-run in production
2. Compare output to dev/staging
3. Prepare rollback plan
4. Write execution steps
5. Identify what to monitor
6. Schedule execution time (if needed)

Document:
- Is dry-run output as expected?
- Rollback ready?
- Team notified?
- Monitoring ready?
```

**What to Verify Before Production**:
- [ ] Final dry-run verification
- [ ] Rollback plan ready
- [ ] Team aware
- [ ] Monitoring active
- [ ] Maintenance window (if needed)

### Success Criteria

- [ ] Completed change in Dev
- [ ] Verified in Staging
- [ ] Prepared (but not yet executed) for Prod
- [ ] Fixed issues found in early stages
- [ ] Built confidence through progression
- [ ] Have rollback plan ready

### Reflection Questions

1. What issues did you catch in dev that would have broken staging?
2. What issues did you catch in staging that would have broken prod?
3. How much more confident are you after two successful environments?
4. Would you have skipped any stages? Glad you didn't?
5. Is progressive verification worth the extra time?

**Key Insight**: Each stage catches different issues. Skipping stages for high-risk changes is negligence, not efficiency.

---

## Exercise 11: MCP Server Evaluation (30 minutes)

**Module/Concept**: Module 8 - MCP Servers Evaluation Framework

**Objective**: Make intentional decisions about MCP server installation using the evaluation framework.

**Scenario**: You're considering installing an MCP server. Walk through the decision process.

### Activity

**Step 1: Choose a Candidate MCP Server** (5 minutes)

Pick one of these scenarios:
- Incident management system (PagerDuty, OpsGenie)
- Cloud provider API (AWS, Azure, GCP)
- Project management (Jira, Azure DevOps)
- Source control (GitHub, GitLab)
- Monitoring system (Datadog, Grafana)

Or a real MCP server you're considering.

**Step 2: Apply Frequency Questions** (5 minutes)

Answer honestly:

```
Will I use this daily? Weekly? Monthly?
[Your answer]

Is this solving a recurring pain point?
[Your answer]

Can I quantify usage frequency?
Current manual workflow: [X] times per [day/week]
Time spent: [Y] minutes per use
```

**Step 3: Evaluate Alternatives** (10 minutes)

```
Can AI do this with built-in tools?
[Check Read, Write, Bash, WebFetch capabilities]

Is there a CLI tool I could use instead?
[List CLI options: gh, kubectl, az, etc.]

Could I create a local data store? (Module 4)
[Would periodic export work? How often updated?]

Could a simple script solve this?
[Estimate script complexity vs MCP server]
```

**Step 4: Calculate Value** (5 minutes)

```
Time saved per use: [X] minutes

Usage frequency: [Y] times per [day/week/month]

Total time saved: [X × Y] = [Z] per [period]

Context cost: [Number of tools exposed]

Is time saved worth context cost?
[Your decision]
```

**Step 5: Make Decision** (5 minutes)

Use the decision tree from Module 8:

```
Decision: [ ] Install  [ ] Don't Install  [ ] Conditional

If Install:
- Trial period: [2 weeks]
- Success criteria: [What usage pattern justifies keeping?]
- Calendar reminder: [Set for evaluation date]

If Don't Install:
- Alternative approach: [What will you do instead?]
- Why not: [Specific reason]

If Conditional:
- Under what circumstances: [e.g., "During on-call rotations only"]
```

### Success Criteria

- [ ] Evaluated specific MCP server
- [ ] Answered all frequency questions honestly
- [ ] Explored at least 3 alternatives
- [ ] Calculated time saved
- [ ] Made informed decision with rationale
- [ ] If installing: defined trial period and metrics

### Reflection Questions

1. Was your initial instinct to install? Did evaluation change that?
2. Which alternative surprised you as being viable?
3. How many tools does the server expose? Need them all?
4. Could you quantify actual usage frequency?
5. What's your decision and why?

**Key Insight**: Context is precious. Only install servers you'll use intentionally and frequently. Default to "no" until proven necessary.

---

## Exercise 12: Verification Pattern Practice (45 minutes)

**Module/Concept**: Module 6 - Script Generation, Read vs Execute, Accountability

**Objective**: Develop critical review skills for AI-generated scripts before production use.

**Scenario**: Review an AI-generated script for production deployment and create a verification checklist.

### Activity

**Step 1: Generate a Production Script** (10 minutes)

Request AI generate a script for a production operation:

Example tasks:
- Deploy application update across cluster
- Database migration script
- Cleanup old resources
- Configuration update across services

```
Prompt to AI:
"Generate a script for [production operation]. This will run in production,
so include:
- Verbose comments
- Safety checks
- Dry-run mode
- Rollback instructions
- Verification steps"
```

**Step 2: Code Review Checklist** (15 minutes)

Review the generated script using this checklist:

**Understanding**:
- [ ] Do I understand what every line does?
- [ ] Can I explain this to a colleague?
- [ ] Are there any "magic" commands I don't recognize?
- [ ] Do the comments accurately describe the code?

**Security**:
- [ ] No hardcoded credentials or secrets?
- [ ] Using environment variables for sensitive data?
- [ ] Appropriate file permissions?
- [ ] No SQL injection or command injection risks?

**Safety**:
- [ ] Dry-run mode works correctly?
- [ ] Safety checks before destructive operations?
- [ ] Rollback procedure included?
- [ ] Transaction wrapping where appropriate?

**Error Handling**:
- [ ] Exits on error (set -e or equivalent)?
- [ ] Validates inputs and preconditions?
- [ ] Handles edge cases?
- [ ] Provides useful error messages?

**Production Readiness**:
- [ ] Verbose logging of actions?
- [ ] Would I want to run this at 2am during an incident?
- [ ] Does it match our team's standards?
- [ ] Can we safely run this multiple times (idempotent)?

**Step 3: Identify Issues and Improvements** (10 minutes)

Document what you found:

```
Issues Found:
1. [Specific issue - e.g., "No validation that database is reachable"]
2. [Another issue]
3. [Another issue]

Suggested Improvements:
1. [Improvement - e.g., "Add connection test before migration"]
2. [Another improvement]
3. [Another improvement]

Questions for AI:
1. [Question about unclear logic]
2. [Question about edge case handling]
```

**Step 4: Request Improvements** (10 minutes)

Ask AI to address your findings:

```
"I reviewed the script and found these issues:
[List your issues]

Can you update the script to:
1. [Specific improvement]
2. [Specific improvement]
3. [Specific improvement]

Explain what you changed and why."
```

### Success Criteria

- [ ] Generated production-ready script
- [ ] Completed full review checklist
- [ ] Identified at least 3 potential issues or improvements
- [ ] Requested and received improvements from AI
- [ ] Understand final script completely
- [ ] Feel confident about running in prod (after testing)

### Reflection Questions

1. What issues would you have missed without the checklist?
2. Did AI's first version have any security problems?
3. How did the script improve after your review?
4. Would you have caught these issues by just reading casually?
5. What will you always check for now?

**Key Insight**: AI-generated code needs the same rigor as human-written code. You are accountable for what executes in production.

---

## Bonus: Team Challenge

**Collaborative Exercise** (90 minutes)

1. Pick complex team task
2. Break into groups
3. Each group designs approach using context engineering
4. Present solutions
5. Compare strategies
6. Vote on best approach
7. Actually execute winning strategy as team

**Debrief questions**:
- What strategies worked best?
- What was harder than expected?
- What would you do differently?
- What patterns will you use regularly?

---

## Self-Assessment

After completing exercises, rate yourself:

**Beginner Skills** (Can you...):
- [ ] Write context-rich prompts with file paths
- [ ] Navigate to appropriate starting directories
- [ ] Identify when to use multiple tabs
- [ ] Use natural language instead of command-style prompts
- [ ] Request scripts with dry-run mode

**Intermediate Skills** (Can you...):
- [ ] Design multi-tab workflows for complex tasks
- [ ] Generate and use handoff prompts
- [ ] Build simple local data stores
- [ ] Break down complex tasks with AI assistance
- [ ] Apply progressive verification (Dev → Review → Prod)
- [ ] Review AI-generated scripts critically

**Advanced Skills** (Can you...):
- [ ] Orchestrate parallel agents with coordination
- [ ] Design context infrastructure (inventories, templates)
- [ ] Choose optimal patterns for different scenarios
- [ ] Attempt complex tasks you previously avoided
- [ ] Evaluate MCP server installation decisions
- [ ] Integrate verification patterns into daily workflow

**Safety and Accountability** (Do you always...):
- [ ] Request dry-run mode for operational scripts
- [ ] Test in dev/staging before production
- [ ] Review AI-generated code thoroughly
- [ ] Understand scripts before executing them
- [ ] Apply same rigor to AI code as human code
- [ ] Make intentional MCP installation decisions

---

## Next Steps

**This Week**:
- Apply one new pattern to real work
- Practice natural language communication daily
- Request dry-run mode for every operational script
- Attempt one "too complex" task using Space Jam approach

**This Month**:
- Build one local data store for frequent queries
- Implement progressive verification for high-risk changes
- Audit installed MCP servers (if applicable)
- Share learnings with team

**Ongoing**:
- Iterate and improve your approach
- Teach someone else what you learned
- Contribute examples and patterns back to team
- Maintain verification discipline

**Questions?** Bring them to office hours or team discussion.