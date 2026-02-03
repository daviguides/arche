# Claude Code Workflow, Spec-as-Code, and Arché

## Purpose

This document describes a practical, day-to-day workflow for using **Claude Code** effectively, with **spec-as-code** as the core abstraction and **Arché** as a behavior-optimization layer.

The goal is not blind automation. The goal is **leverage**:
- speed without chaos
- predictability without babysitting
- parallelism without mental burnout

---

## The Core Shift: From Writing Code to Writing Specifications

When you work seriously with Claude Code, something shifts naturally over time:

- You write **less code**
- You write **more specification**

Features, tasks, and bug fixes become less about “typing” and more about:
- framing the problem
- defining constraints
- defining expected behavior
- specifying acceptance criteria

In practice, “working well with Claude Code” is:
- prompt engineering
- context engineering
- **spec-as-code**

Velocity comes from clarity, not automation.

---

## A Day-to-Day Anecdote (Why This Matters)

Some time ago I tried to solve something complex using a single “super prompt”.  
It was well specified, but Claude Code still got lost.

Why?
- there is a cognitive load limit
- there is a context window limit
- and with **Opus 4.5**, the context budget burns fast
- auto-compact tends to degrade the session (it’s not reliable enough as a safety net)

That was the moment the workflow became explicit:
> **Stop pushing everything into one single prompt or session. Break work into phases and bounded tasks. Save context deliberately.**

That change alone improved:
- stability of results
- predictability of execution
- ability to run multiple sessions in parallel

---

## The Four-Element Loop (What “Good Code Assistant Usage” Requires)

Reliable outcomes are the interaction of four elements:

1) **Good Model** (ex: Opus 4.5)  
2) **Good Code Assistant / Agent** (Claude Code system behavior)  
3) **Good Instructions (Spec-as-Code)** (your task spec / constraints / acceptance criteria)  
4) **Good Context** (repo docs, runbooks, cluster maps, commands, architecture notes)

If any one of these is weak, the whole system becomes fragile.

### Diagram: The “Reliability Loop”

```
                 ┌──────────────────────┐
                 │      GOOD MODEL      │
                 │   (e.g., Opus 4.5)   │
                 └──────────┬───────────┘
                            │
                            v
┌──────────────────────┐    ┌──────────────────────┐
│   GOOD CONTEXT        │<-->| GOOD ASSISTANT/AGENT │
│ (repo docs, runbooks, │    │ (Claude Code system  │
│  clusters, commands)  │    │  behavior)           │
└──────────┬───────────┘    └──────────┬───────────┘
           │                             │
           v                             v
     ┌────────────────────────────────────────┐
     │     GOOD INSTRUCTIONS (SPEC-AS-CODE)    │
     │ (brief, constraints, steps, acceptance) │
     └───────────────────┬────────────────────┘
                         │
                         v
               ┌──────────────────────┐
               │   RELIABLE OUTCOMES  │
               │ (speed + correctness)│
               └──────────────────────┘
```

### Notes
- We typically **receive**: the model + the assistant.
- We must **create and maintain**: instructions + context.
- Arché improves the “assistant/agent behavior” so instructions and context are used consistently.

---

## Why Human-in-the-Loop Is Mandatory

Claude Code (or any LLM) does **not** think beyond what is defined.
It does not invent missing constraints responsibly.
It does not detect ambiguity unless prompted to do so.

If you remove the human dialogue from the loop, you can absolutely automate your way into a **very confident wrong result**.

The human role is not to type code.
The human role is to:
- question assumptions
- notice missing constraints
- redirect reasoning
- apply fine-grained judgment

This is why **dialogue** is the core mechanism in every phase.

---

## Phased Workflow (How We Avoid Getting Lost)

The workflow separates cognitive phases explicitly.
Each phase is **dialogal**, not fire-and-forget.

### 1. Exploration (Human-led, AI-assisted)

Goal: collect *raw material*.

What Claude Code can automate:
- searching documentation
- collecting links
- listing known constraints
- summarizing existing code or architecture

What requires human dialogue:
- deciding *what* is relevant
- spotting missing angles
- asking “what are we not looking at?”

```
Human asks
   ↓
Claude searches / summarizes
   ↓
Human refines questions
   ↓
Claude expands findings
```

Output: loosely structured knowledge.

---

### 2. Research (Analytical, still dialogal)

Goal: transform raw material into *understanding*.

Difference from exploration:
- exploration gathers
- research compares, analyzes, and deepens

What Claude Code can automate:
- comparisons
- pros/cons lists
- trade-off analysis
- pattern extraction

What requires human dialogue:
- validating reasoning
- challenging conclusions
- injecting domain intuition

This is where human “fine thinking” still dominates.

Output: validated insights and decisions.

---

### 3. Planning (The Safety Net)

Planning is a **cognitive buffer**.

It exists to:
- reduce execution risk
- expose hidden dependencies
- catch side effects early

This phase is almost always dialogal.

What Claude Code can automate:
- structuring steps
- proposing milestones
- identifying obvious risks

What requires human dialogue:
- pruning overengineering
- validating feasibility
- deciding scope boundaries

Planning prevents both human and model from “running ahead”.

Output: a bounded, reviewable plan.

---

### 4. Plan Mode (Optional but Powerful)

Plan Mode (Claude Code specific) is **not mandatory**, but useful.

Typical flow:
- human provides exploration + research + planning artifacts
- Claude consolidates them into an execution-ready plan
- human reviews and corrects

This step acts as a final coherence check.

---

### 5. Execution (Automated, After Clarity)

Only after clarity is achieved does execution become safe to automate.

At this point:
- most ambiguity is removed
- context is stable
- acceptance criteria are explicit

Claude Code can now:
- implement end-to-end
- follow the plan without babysitting

Human role during execution:
- spot-check results
- validate outcomes
- assess side effects

---

## Full Cognitive Flow

```
[ Exploration ]  <-->  Human dialogue
        |
        v
[ Research ]     <-->  Human dialogue
        |
        v
[ Planning ]     <-->  Human dialogue
        |
        v
[ Plan Mode ]    <-->  Human review (optional)
        |
        v
[ Execution ]    -->   Mostly automated
```

Dialogue tapers off only at execution — never before.

---

## Parallel Sessions (Mental Leverage)

Because phases are explicit and saved, sessions become composable:

```
Session A: Researching Feature X
Session B: Planning Incident Y
Session C: Executing Task Z
```

This avoids:
- context explosion
- reasoning degradation
- mental fatigue

---

## Markdown as First-Class Context

Over time, Markdown becomes first-class “code”.

Reusable knowledge such as:
- architecture notes
- debugging guides
- incident postmortems
- operational runbooks

...should be documented and stored in the repository.

This becomes part of the context layer that Claude Code can read directly.

Important nuance:
- Claude Code doesn’t need a RAG pipeline for this
- it can scan the repo and find relevant files
- *but only if we wrote the docs in the first place*

---

## Where Arché Fits

Arché optimizes **assistant behavior**, not thinking.

It encodes:
- phase separation
- anti-babysitting defaults
- clarity-before-execution bias

What Arché does *not* do:
- replace human judgment
- automate spec creation
- eliminate dialogue

---

## “What We Get” vs “What We Must Build”

We can split responsibilities clearly.

### Diagram: Inputs vs Responsibilities

```
GIVEN (Platform / Tooling)
────────────────────────────────────────────
1) Model
   - e.g., Opus 4.5

2) Code Assistant
   - Claude Code baseline agent/system behavior


PROVIDED BY ARCHÉ (Plugin Layer)
────────────────────────────────────────────
3) Behavior shaping for the assistant
   - principles
   - phase separation habits
   - anti-babysitting workflow defaults


DEVELOPER RESPONSIBILITY (Team Practice)
────────────────────────────────────────────
4) Spec-as-Code (Instructions)
   - brief + constraints
   - milestones + steps
   - acceptance criteria
   - risk checks / side effects

5) Context (Committed with the repo)
   - runbooks and cluster maps
   - “how to debug this service”
   - commands and locations
   - architecture notes and known pitfalls
```

### Another view: “What drives reliability”
```
Reliability = (Model + Assistant) × (Instructions + Context)

- Model + Assistant are the engine.
- Instructions + Context are the steering and map.
- Arché improves how the engine responds to steering/map.
```

---

## Final Note

This direction is less about automation and more about a **mindset shift**:
- think in specs
- commit context as part of engineering output
- phase work so context stays clean
- then let execution be automated safely

Arché encodes months of iteration around that workflow.

## Appendix A: On Incident Work - From Reactive to Proactive (and What We Can Automate)

[READ](docs/appendix_a.md)
