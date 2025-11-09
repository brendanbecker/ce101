# Integration Plan for New Concepts

## Overview

This document outlines how to integrate new concepts into the CE101 curriculum:
- MCP Servers (when to use/avoid)
- Space Jam Theory (empowerment to explore)
- Natural Language Communication (how to interact effectively)
- Learning While Working (AI as teacher, dry-run patterns, progressive verification)
- Verification Patterns (accountability and safety)
- Creation vs Verification (why AI assistance works so well)

## Current Curriculum Structure

1. Core Concepts - Four context strategies
2. Filesystem Organization - Directory structure as context
3. Multi-Tab Orchestration - Multiple specialized agents
4. Integration Patterns - Live queries vs local data (includes local data stores)
5. Practical Patterns - Real-world workflows
6. Common Pitfalls - What to avoid
7. MCP Servers - When and why to use

**Note**: Module 4 (Local Data Stores) has been archived and integrated into Module 4 (Integration Patterns)

## Proposed Integration Strategy

### Option A: Weave Throughout (Recommended)

**Early Foundation (Module 1 Expansion)**:
- Add "Space Jam Theory" as opening motivation
  - "If you can dream it, you can do it"
  - Encouragement to explore and experiment
  - Frame AI as a creative enabler
- Add "Accountability Framework" immediately after
  - You are responsible for decisions
  - LLM reads prod, generates scripts, YOU verify and execute
  - Balance empowerment with responsibility

**Natural Language as Core Skill (Module 1 or New Module 1.5)**:
- How to communicate with AI effectively
- Talk like you would to a coworker who needs explicit context
- Using uncertainty/doubt to trigger explanation and reasoning
- Reduces false confidence hallucinations
- Applies to human communication too

**MCP Servers (New Module 7)**:
- What they are and how they work
- When to consider using them
- Warning: Don't install servers you won't use intentionally
- Context cost vs productivity gain (qualitative)
- Evaluation criteria

**Learning While Working (Integrate into Modules 1 & 6)**:
- AI as teacher: discovering tools and patterns
- Explanation pattern: "explain piece by piece"
- Dry-run as standard practice for all scripts
- Manual first, automate second
- Progressive verification: Dev → Review → Prod

**Verification Patterns (Expand Module 5 or New Section)**:
- Script generation for auditability
- Dry-run mode requirement (from Learning While Working)
- Peer review workflows
- Reading vs executing in production
- Creation vs verification: AI makes creation fast, verification stays thorough
- Verbose comments for review (tokens are cheap)

### Option B: New Early Module

Create new "Module 02: Working with AI Effectively" and renumber rest:

1. Core Concepts
2. **Working with AI Effectively** (NEW)
   - Space Jam Theory
   - Natural Language Communication
   - Accountability Framework
   - Verification Patterns
   - Creation vs Verification
3. Filesystem Organization (was 2)
4. Multi-Tab Orchestration (was 3)
5. Local Data Stores (was 4)
6. Integration Patterns (was 5)
7. Practical Patterns (was 6)
8. MCP Servers (NEW)
9. Common Pitfalls (was 7)

### Option C: Bookend Structure

Keep current flow, add bookends:

0. **Getting Started with AI** (NEW - before Module 1)
   - Space Jam Theory
   - Natural Language basics
   - Accountability intro

1-7. **Current curriculum** (mostly unchanged)
   - Weave accountability reminders throughout
   - Add natural language examples where relevant

8. **MCP Servers** (NEW)

9. **Advanced Patterns** (NEW or expanded from Module 5)
   - Verification workflows
   - Script generation patterns
   - Creation vs verification advantage
   - Peer review processes

## Questions to Resolve

**Q: Where does "natural language communication" best fit?**
- Early (to set interaction patterns from the start)?
- Throughout (as examples in each module)?
- As its own focused module?

**Q: Should Space Jam Theory be:**
- A slide/callout box in Module 1?
- Opening section of expanded Module 1?
- Its own micro-module?

**Q: Accountability treatment:**
- Recurring theme woven throughout (with icon/callout)?
- Dedicated section early, then referenced?
- Both?

**Q: Verification patterns:**
- Expand Practical Patterns (Module 5)?
- New advanced module at end?
- Spread across relevant modules?

## Recommendation

I'm leaning toward **Option A with elements of C**:

1. **Expand Module 1** to include:
   - Space Jam Theory (opening motivation)
   - Accountability Framework (immediate follow-up)
   - Brief intro to natural language communication

2. **Add natural language examples throughout** existing modules
   - Show effective communication patterns in context
   - Use "doubt triggers explanation" in real scenarios

3. **Expand Module 5** (Practical Patterns) to include:
   - Script generation workflows
   - Verification and peer review
   - Creation vs verification advantage

4. **Add Module 7** for MCP Servers

5. **Update Module 6** (Common Pitfalls) to include:
   - Over-reliance on MCP servers
   - Skipping verification
   - Blind trust in outputs

This preserves the current flow while integrating new concepts where they're most relevant. It also maintains the practical, SRE-focused approach.

## Next Steps

1. Draft expanded Module 1 with Space Jam + Accountability
2. Draft MCP Servers module
3. Draft verification patterns section for Module 5
4. Create natural language examples for integration
5. Review and refine based on feedback
6. Update CLAUDE.md with new structure

## Open Questions

- How much detail on MCP server internals vs just usage guidance?
- Should we include specific MCP server recommendations or stay generic?
- Do we need a "trust but verify" checklist or decision tree?
- Should accountability have a visual reminder (icon/callout) throughout?
