# Module 1: Core Concepts

## The Mental Model Shift

### The Old Way
```
"Write me a script to check disk space"
```

You get a generic script that may or may not fit your environment.

### The New Way
```
I need to monitor disk usage across our Kubernetes cluster.

Relevant files: 
- /monitoring/prometheus-rules.yaml (current alerts)
- /scripts/disk-check.sh (existing script we're replacing)

Requirements:
- Alert at 80% usage
- Integrate with our Slack webhook
- Output JSON for Datadog

Show me the existing script first, then propose improvements.
```

You get a script tailored to your actual infrastructure.

**The difference**: You're giving the AI the context it needs to do the job *right*, not just *done*.

---

## Space Jam Theory: If You Can Dream It, You Can Do It

### The Self-Imposed Limit

You're staring at a complex migration:
- 47 microservices to move from EKS to GKE
- Custom service mesh configurations
- Stateful workloads with persistent volumes
- Zero-downtime requirement

Your first thought: "This is too complex for AI to help with."

**Stop right there.**

That assumption is your biggest barrier to productivity. Not the complexity of the task. Not the limitations of AI. Your own self-imposed limit on what's possible.

### How to Approach Complex Tasks

**Don't ask**: "Can AI handle this?"
**Ask instead**: "How can AI help me break this down?"

Complex tasks aren't single problems. They're collections of smaller problems that AI excels at:
- Analyzing existing configurations
- Generating migration scripts and automation
- Creating test cases and validation logic
- Documenting decisions and rationale
- Researching best practices

**Example approach:**
```
I need to migrate 47 microservices from EKS to GKE. I've never done a
cross-cloud Kubernetes migration at this scale before.

Let me start by asking AI to help me:
1. Break down the migration into phases
2. Identify the biggest risks
3. Create a testing strategy
4. Build automation for the repetitive parts

I don't need AI to do it all. I need AI to help me think it through.
```

You're not replacing your expertise. You're **amplifying it**.

### Real SRE Examples

**Multi-region database failover procedure**:
- You understand the business logic and failure scenarios
- AI helps document the procedure step-by-step
- AI generates the runbook with all edge cases
- You verify and test each step

**Kubernetes RBAC policy design**:
- You know your security requirements
- AI helps translate requirements to policies
- AI generates the YAML with proper least-privilege
- You review for completeness and test

### The Key Insight

**You bring**: Domain knowledge, requirements, judgment, verification
**AI brings**: Pattern recognition, code generation, documentation, research

Together, you can tackle problems you'd never attempt alone—not because they're impossible, but because they'd take too long to do manually.

**If you can dream it, you can at least start it.** The rest is just breaking it down.

---

## Accountability Framework: You Are Responsible

### The Balance

We just told you to dream big and attempt complex tasks with AI assistance.

Now we're telling you something equally important:

**You are accountable for everything that executes in production.**

Not the AI. Not the tool. You.

### The Professional Responsibility

AI is a powerful accelerator for:
- Reading production configurations
- Analyzing logs and metrics
- Generating automation scripts
- Drafting runbooks and documentation

But there's a critical difference between **generation** and **execution**:

**AI can read prod. You execute against prod.**

### The Verification Pattern

Every AI-generated artifact must go through your professional filter:

```
AI generates → You review → You test → You execute
```

This isn't bureaucracy. This is **engineering discipline**.

### What This Looks Like

**For scripts**:
1. AI generates the automation
2. You read every line
3. You test in non-prod first
4. You verify the logic is correct
5. You execute (or schedule) in prod

**For configuration changes**:
1. AI proposes the change
2. You validate against requirements
3. You check for unintended side effects
4. You test rendering/parsing
5. You commit and deploy through normal workflow

**For incident response**:
1. AI helps analyze logs and suggest fixes
2. You verify the diagnosis makes sense
3. You test the fix in staging
4. You apply to prod with proper change control
5. You monitor the results

### The Productivity Advantage: Verification is Faster Than Creation

Here's the counterintuitive truth: **Verification is easier than generation.**

**Example:**
- Writing a migration script from scratch: 4 hours
- Reviewing an AI-generated migration script: 30 minutes
- Testing it thoroughly: 1 hour
- **Total time saved: 2.5 hours**

**Why this works:**

AI is great at:
- Generating comprehensive scripts with error handling
- Adding detailed comments explaining each step
- Including dry-run modes for safe testing
- Documenting assumptions and edge cases

You're great at:
- Spotting logical errors
- Catching missing edge cases
- Understanding business context
- Knowing what "correct" looks like for your environment

**The AI-generated script likely has better error handling, more comprehensive logging, and clearer documentation than you'd write under time pressure.**

You still review every line. You still test thoroughly. But you didn't have to spend 4 hours writing it.

**This division of labor is why AI assistance provides 4-7x productivity gains without sacrificing safety.**

### Accountability Callouts

Throughout this course, you'll see occasional reminders:

> **⚠️ Accountability**: [Specific verification step for this pattern]

These aren't nagging. They're checkpoints to ensure safe, professional practices.

---

## Effective Communication: How to Talk to AI

### Natural Language Communication

#### The Counterintuitive Truth

Most people think AI needs:
- Precise, formal language
- Perfectly structured prompts
- Commands like you're programming

The truth is the opposite.

**AI works best when you talk to it like a knowledgeable coworker who needs context.**

#### Why This Works (The Technical Bit)

Large Language Models (LLMs) are trained on human communication—documentation, Stack Overflow posts, GitHub issues, technical discussions. They learned to:

- Interpret natural language
- Handle ambiguity through context
- Ask clarifying questions
- Explain reasoning

When you talk naturally, you're working **with** the model's training, not against it.

#### The Doubt Advantage

Here's something that surprises people:

**Expressing uncertainty makes AI responses more accurate.**

**Why**: When you say "I'm not sure" or "I think it might be", you signal to the model that it needs to:
- Provide more explanation
- Show its reasoning
- Check assumptions
- Offer alternatives

This reduces hallucinations and increases the educational value of responses.

#### Examples: Command vs. Natural Language

**Command-style (less effective)**:
```
Fix disk space alert threshold to 85%
```

What's missing: Why? Where? What are the implications?

**Natural language (more effective)**:
```
I need to update our disk space alert threshold from 80% to 85%. We've been
getting too many false positives—47 last month according to our incident log.

I'm not sure if 85% is the right number, or if we should look at rate of
change instead. The current alert is in /monitoring/prometheus/alerts/disk-space.yaml.

Can you show me the current rule and suggest whether threshold adjustment or
rate-of-change would be better for our situation?
```

What you get: Education + solution, not just a change.

#### The Context-First Pattern

Effective AI communication follows this structure:

```
1. What you're trying to accomplish (the goal)
2. What you know and what you're unsure about (context + uncertainty)
3. What you've already tried or checked (prior work)
4. Where the relevant information is (file paths, systems)
5. What success looks like (acceptance criteria)
```

You don't need all five every time. But including more usually gets better results.

#### Real Examples from SRE Work

**Ineffective**:
```
Check the logs
```

**Effective**:
```
Our API started returning 502s about 20 minutes ago. I've checked the
application logs in /var/log/app.log and see connection timeouts to the
database, but I'm not sure if that's the root cause or a symptom.

Can you help me:
1. Analyze the logs for patterns around the time it started
2. Suggest what else I should check
3. Help me determine if this is a DB issue or something else
```

---

**Ineffective**:
```
Write terraform for S3 bucket
```

**Effective**:
```
I need to create an S3 bucket for our application logs. Based on our
existing buckets in /terraform/modules/s3/, it looks like we have a standard
module, but I'm not sure if it handles the lifecycle rules we need for logs.

Requirements:
- Logs should transition to IA after 30 days
- Delete after 90 days
- Server-side encryption required
- No public access

Can you show me if our existing module supports this, or if we need to
extend it?
```

---

**Ineffective**:
```
Fix the kubernetes deployment
```

**Effective**:
```
The deployment for our auth service isn't starting pods correctly. Looking at
/k8s/apps/auth/deployment.yaml, I see we recently changed the resource limits,
and now pods are in CrashLoopBackOff.

I think it might be OOMKilled, but the events are a bit unclear. Can you help
me interpret the pod events and suggest whether to increase memory limits or
if there's a different issue?
```

#### When to Be More Formal vs. More Conversational

**Use formal/structured style when**:
- Providing specifications or requirements
- Listing configuration values
- Defining acceptance criteria
- Documenting decisions

**Use conversational style when**:
- Explaining the problem context
- Describing what you've tried
- Expressing uncertainty
- Asking for explanations

**Best approach**: Mix them. Context in natural language, specifications in structured format.

#### The Explanation Pattern

When you want to learn, not just get an answer:

```
Can you explain [topic] piece by piece?

I understand [what you know], but I'm fuzzy on [what you don't].

Show me an example and walk through what each part does.
```

This triggers the model to:
- Break down complex topics
- Provide step-by-step explanation
- Use examples
- Check your understanding

#### Common Mistakes to Avoid

❌ **Being too brief to save tokens**
Tokens are cheap. Misunderstandings are expensive.

❌ **Assuming AI knows your environment**
It doesn't. Tell it about your setup.

❌ **Hiding uncertainty to seem confident**
Confidence prompts confident (sometimes wrong) answers. Uncertainty prompts thorough answers.

❌ **Using jargon without context**
Even if AI knows the jargon, explain how you're using it.

#### The Meta-Benefit

These communication patterns don't just work with AI.

They make you better at:
- Writing documentation
- Asking colleagues for help
- Explaining problems in incident channels
- Creating clear tickets and runbooks

**Natural language communication is a professional skill, regardless of who you're talking to.**

---

### Meeseeks Theory: AI Does Exactly What You Ask

#### "Oooohh! Can Do!"

Like Mr. Meeseeks from Rick and Morty, AI enthusiastically does **exactly** what you request—even if that's not what you actually needed.

#### The Real Problem Isn't Hallucination

The common fear: "AI will make stuff up and mislead me."

The actual problem: **AI will do precisely what you asked, even when your request was vague or incomplete.**

#### Examples of Literal Compliance

**Vague request:**
```
Fix the config
```

**AI's enthusiastic response:**
```
Sure! I'll fix the syntax error in config.yaml.
```

**What you actually needed:** Update the database connection string in production config, not fix a YAML syntax error in the test config.

**The AI did exactly what you asked** (fix "the" config), but it wasn't helpful because you didn't specify which config or what kind of fix.

---

**Vague request:**
```
Update the script
```

**AI's enthusiastic response:**
```
I've updated the script to use Python 3.11 syntax!
```

**What you actually needed:** Add error handling for database connection failures.

**The AI did exactly what you asked** (update the script), just not the update you wanted.

---

**Vague request:**
```
Check the deployment
```

**AI's enthusiastic response:**
```
The deployment.yaml file has valid YAML syntax!
```

**What you actually needed:** Investigate why the deployment isn't scaling properly under load.

**The AI did exactly what you asked** (check the deployment), but you got a syntax check instead of a scaling investigation.

#### The Context Trap: Solutions Without Sufficient Context

Here's the more dangerous pattern:

**You're in a hurry. You need a solution. You ask AI for one immediately.**

AI enthusiastically provides a solution based on the limited context you gave—and that solution might lead you down entirely the wrong path.

**Example:**

```
You: "Write me a script to restart pods that are crashing"

AI: "Sure! Here's a script that detects CrashLoopBackOff and deletes the pods..."
```

**The problem**: AI gave you exactly what you asked for, but you never established:
- Why the pods are crashing
- Whether restarting is the right solution
- What the actual root cause might be
- Whether this is a symptom of a bigger issue

**The better approach:**

```
I have pods going into CrashLoopBackOff in the auth-service deployment. Before I
decide how to handle this, can you help me:

1. Analyze the pod events and logs to understand why they're crashing
2. Determine if this is a configuration issue, resource constraint, or application bug
3. Then suggest the appropriate fix based on what we find

The deployment is at /k8s/apps/auth/deployment.yaml and I can grab logs if needed.
```

**Why this matters**: AI will happily generate solutions to the wrong problem if you push it toward solutions before establishing proper context.

**The pattern to avoid:**
1. Encounter problem
2. Immediately ask for solution
3. AI generates solution based on incomplete understanding
4. You implement it
5. Wrong solution for wrong problem

**The pattern to follow:**
1. Encounter problem
2. Ask AI to help investigate and understand
3. Establish context together
4. Then ask for solution
5. Right solution for right problem

**Remember**: AI's eagerness to help can work against you if you encourage it to skip the investigation phase.

#### Why This Matters for Context Engineering

This is **why** context engineering matters:

- ✅ **Clear context** → AI does useful work that solves your actual problem
- ❌ **Vague context** → AI does technically correct but unhelpful work

The solution isn't to avoid AI. The solution is to **be specific about what you want.**

#### How to Be Specific

Instead of vague commands, provide:

1. **What you're trying to accomplish** (the actual goal)
2. **What specific thing needs attention** (file path, system, component)
3. **What kind of change or investigation** (fix what? update how? check for what?)
4. **Why you're doing this** (context helps AI understand intent)

**Example transformation:**

❌ **Vague:** "Fix the config"

✅ **Specific:**
```
The API service can't connect to the database in production. I need to verify
the connection string in /company/SRE/helm/charts/api/values/prod.yaml is
correct. We recently changed the database endpoint last week.

Can you:
1. Show the current connection string
2. Check if it matches the database endpoint format for our new Azure instance
3. Suggest the correct connection string if it's wrong
```

#### The Counterintuitive Part

Being more specific and providing more context feels like it takes longer.

**It does take 30 more seconds upfront.**

**It saves 10 minutes of back-and-forth clarification.**

#### Meeseeks Theory in Practice

When AI gives you an unhelpful response, don't think "AI is bad at this."

Think: **"Did I give it enough context to understand what I actually need?"**

Most "hallucinations" and "wrong answers" are really:
- Literal compliance with vague requests
- Reasonable interpretation of ambiguous instructions
- Best effort with insufficient context

#### The Fix

**Don't fight the AI's eagerness to help. Channel it with clarity.**

- Specific requests → Specific helpful results
- Vague requests → Vague technically-correct results

**Meeseeks Theory + Context Engineering = AI does exactly the useful thing you needed**

---

## The Four Context Strategies

Context Engineering uses four fundamental strategies for managing information:

### 1. SELECT - Point to the Right Information

**What it is**: Direct the AI to relevant files, directories, or data sources rather than expecting it to guess.

**When to use**:
- Starting a new task
- AI needs domain-specific information
- Working with large codebases

**Examples**:
```bash
# Explicit file selection
"Check /terraform/azure-infrastructure/main.tf for the AKS cluster config"

# Directory-based selection  
"Search the /runbooks directory for any documentation about database failovers"

# Pattern-based selection
"Find all helm charts that use the nginx-ingress controller"
```

**SRE Use Cases**:
- Pointing to terraform state files
- Directing to specific runbooks
- Selecting relevant log files
- Querying MCP servers for live data

---

### 2. WRITE - Persist Information Externally

**What it is**: Save context outside the AI's session so it's available later or across multiple sessions.

**When to use**:
- Need to remember decisions across sessions
- Building reusable knowledge
- Sharing context across multiple agents

**Examples**:
```bash
# Handoff prompts
"Give me a handoff prompt I can use to continue this work in a new session"

# Knowledge bases
Create runbook at /notes/runbooks/new-procedure.md

# Local inventories
Build Azure resource inventory at /notes/inventory/azure-resources.json
```

**SRE Use Cases**:
- Creating handoff prompts when context fills up
- Building searchable incident histories
- Maintaining resource inventories
- Documenting decisions and solutions

---

### 3. ISOLATE - One Agent, One Job

**What it is**: Use separate agents (terminal tabs/sessions) for separate concerns instead of mixing multiple tasks in one context.

**When to use**:
- Complex multi-part tasks
- Independent work streams
- Need to maintain focus on specific aspects

**Examples**:
```bash
# Instead of one tab doing everything:
Tab 1: Update helm chart A
Tab 2: Update helm chart B  
Tab 3: Update sync script
Tab 4: Search work items (reference)
Tab 5: Aggregate and create documentation
```

**SRE Use Cases**:
- Parallel infrastructure updates
- Separating investigation from remediation
- Document analysis in one tab, execution in another
- Different agents for different services

**Why it works**: Each agent maintains focused context without interference from unrelated information.

---

### 4. COMPRESS - Rarely Needed in 2025

**What it is**: Reduce context size through summarization or truncation.

**When to use**: Rarely. Modern context windows are large enough that isolation is usually better.

#### Context Windows in 2025: Bigger Than You Think

**Reality check:**
- Chat-gpt5-codex, Claude Code: 200k tokens
- GPT-4o: 128k tokens
- Most codebases fit entirely in one session

**What 200k tokens can hold:**
- ~150,000 words of text
- ~75-100 medium-sized source files
- Entire helm charts, terraform modules, runbooks, incident logs
- Long conversation histories (100+ exchanges)

**What this means for you:**
- Stop worrying about token counts for normal work
- Compression is rarely needed
- You can load entire runbooks, long log files, multiple related files
- Handoffs are for CLARITY (clean slate), not capacity

#### When You Still Need Compression

**Extremely rare scenarios:**
- Multiple very large files (50k+ lines each) in one session
- Extremely long sessions (100+ messages with extensive file reads)
- Combined large codebase + extensive conversation history

**Even then, isolation is usually better than compression.**

#### Our Approach

- **Don't preemptively compress**. Tokens are cheap, clarity is expensive.
- **Use handoff prompts** when context feels cluttered (typically 40-60% as a guideline for clarity, not capacity)
- **Prefer isolation** over compression - split into multiple agents instead
- **Monitor your context meter** - if below 60%, don't worry about it

#### The Clarity Threshold (Not Capacity)

**Use handoffs when:**
- Context feels messy (lots of different topics mixed together)
- Hard to remember what was discussed
- You want a clean slate for new approach
- **NOT because you're running out of tokens**

**Context at 40%:** Plenty of room, only handoff if it feels cluttered
**Context at 60%:** Still fine, handoff for clarity if desired
**Context at 80%:** Now it matters, consider handoff or new session
**Context at 90%+:** Time to handoff or wrap up

#### Example of Good Compression

When you do need handoff, agent generates concise summary:

```
Agent's handoff:
"We've updated the helm chart to version 4.8, modified resource limits,
and tested rendering. Remaining: update production values and document changes."
```

vs. keeping the entire 30-message conversation history in new session.

#### Key Insight

**With 200k token windows, compression is a clarity tool, not a capacity requirement.**

Focus on organizing your work (isolation, multiple tabs) rather than saving tokens.

---

## Exercise: Transform Your Prompt

Take a task you did recently. Write two versions:

**Version 1 - Basic Prompt**:
```
[What you might naturally type]
```

**Version 2 - Context-Engineered**:
```
[Include: task description, relevant files, requirements, success criteria]
```

### Example

**Version 1**:
```
Update the alert threshold
```

**Version 2**:
```
I need to update our disk space alert threshold from 80% to 85%.

Current alert: /monitoring/prometheus/alerts/disk-space.yaml
Context: We had 47 false positives last month (logged in incidents/2024-11.md)

Please:
1. Show me the current alert rule
2. Update the threshold to 85%
3. Verify syntax is valid
4. Suggest any related alerts that should also be updated
```

---

## Next Steps

Now that you understand the core strategies, learn how to apply them:

- **[Filesystem Organization →](02-filesystem-organization.md)** - Structure your workspace for optimal context
- **[Multi-Tab Orchestration →](05-multi-tab-orchestration.md)** - Manage complex tasks across multiple agents

---

**Questions?** Bring them to the workshop or add to the discussion thread.
