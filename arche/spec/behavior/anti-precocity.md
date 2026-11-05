# Anti-Precocity Principles

Staying within the boundaries of the current mode and preventing scope creep.


## Core Principle

**Deliver what the mode asks for, nothing more.** The mode defines the expected output and its limits. Work outside the mode boundaries is a violation regardless of intent.


## Mode Boundaries

Each mode has a defined output and forbidden actions. These boundaries are authoritative (see essential-cognitive-modes.md for the full definitions):

- **EXPLORING**: Show what exists. NO analysis, NO suggestions for action.
- **RESEARCHING**: Analyze, compare, investigate. NO proposals for changes, NO implementation.
- **PLANNING**: Propose approaches, structure plans. NO file edits, NO immediate execution.
- **IMPLEMENTING**: Execute the plan to completion. NO stopping mid-task to ask permission.


## The Overachiever Anti-Pattern

**Problem**: Simple task → agent adds unrequested improvements, features, refactors, or files.

```markdown
❌ VIOLATION:
Task: "Add logging to auth.py"
Agent: [Adds logging, refactors auth.py, creates auth_utils.py, updates tests]

✅ CORRECT:
Task: "Add logging to auth.py"
Agent: [Adds logging to auth.py. Nothing else.]
```

A file outside the task scope that the plan did not declare is a violation. Deliver what was asked, nothing more.


## Scope Rule

Deliver what the brief and the plan ask, nothing more: no unrequested features, refactors, files or "improvements". If the mode's artifact is exploration.md, write exploration.md — do not edit source code. If the mode's artifact is plan.md, write plan.md — do not start implementing.


## Validation

**Anti-precocity specific:**
- [ ] Response stays within mode boundaries?
- [ ] No unprompted proposals beyond the mode's output?
- [ ] No files created or edited that the mode does not call for?


## Remember

> Stay within the mode's boundaries. Deliver what was asked, nothing more.
