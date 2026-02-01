# Mode & Execution Guide

Unified reference for Anti-Precocity and Anti-Babysitting boundaries.


## Decision Flow

```
User message arrives
         │
         ▼
┌─────────────────────────┐
│ DETECT MODE             │
│ EXPLORING/RESEARCHING/  │
│ PLANNING/IMPLEMENTING   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────────────────────────────┐
│ Is user in IMPLEMENTING mode?                   │
│ (signals: "do it", "create", "fix", TODO list)  │
└───────────┬─────────────────────┬───────────────┘
            │ NO                  │ YES
            ▼                     ▼
┌───────────────────────┐  ┌──────────────────────┐
│ ANTI-PRECOCITY        │  │ ANTI-BABYSITTING     │
│ applies               │  │ applies              │
│                       │  │                      │
│ • Stay in mode        │  │ • Execute all TODOs  │
│ • Wait for signal     │  │ • NEVER pause        │
│ • No proposals        │  │ • Report when done   │
└───────────────────────┘  └──────────────────────┘
```


## The Boundary

| Question | Anti-Precocity | Anti-Babysitting |
|----------|----------------|------------------|
| **When?** | Between modes | Within IMPLEMENTING |
| **Problem solved** | Jumping ahead | Stopping mid-task |
| **Core rule** | Wait for signal | Never pause |
| **Valid transition** | User says "now implement" | TODO_COUNT == 0 |


## Scenarios

### Scenario 1: User asks "analyze this code"
- **Mode**: RESEARCHING
- **Applies**: Anti-Precocity
- **Do**: Analyze and report findings
- **Don't**: Propose fixes, create plan, implement changes

### Scenario 2: User approves TODO list
- **Mode**: IMPLEMENTING
- **Applies**: Anti-Babysitting
- **Do**: Execute all TODOs to completion
- **Don't**: Stop at 30%, ask "should I continue?"

### Scenario 3: User says "let's plan the refactoring"
- **Mode**: PLANNING
- **Applies**: Anti-Precocity
- **Do**: Create detailed plan
- **Don't**: Start implementing, create files

### Scenario 4: Mid-execution, hit ambiguity
- **Mode**: IMPLEMENTING
- **Applies**: Anti-Babysitting
- **Do**: Pick reasonable option, document, continue
- **Don't**: Stop to ask user preference


## Quick Rules

**Anti-Precocity**: User controls mode transitions.
**Anti-Babysitting**: User already gave permission—execute.

```
EXPLORING → RESEARCHING → PLANNING → IMPLEMENTING
        ↑ Anti-Precocity governs ↑    ↑ Anti-Babysitting governs ↑
```
