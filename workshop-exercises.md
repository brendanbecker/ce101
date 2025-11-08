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

**Intermediate Skills** (Can you...):
- [ ] Design multi-tab workflows for complex tasks
- [ ] Generate and use handoff prompts
- [ ] Build simple local data stores

**Advanced Skills** (Can you...):
- [ ] Orchestrate parallel agents with coordination
- [ ] Design context infrastructure (inventories, templates)
- [ ] Choose optimal patterns for different scenarios

---

## Next Steps

- Apply one pattern to real work this week
- Share results with team
- Iterate and improve your approach
- Teach someone else what you learned

**Questions?** Bring them to office hours or team discussion.