# Anti-Babysitting Principles

**Dogmatic rules for autonomous TODO execution without premature pauses.**

**Purpose**: Eliminate the "babysitting problem" where LLMs stop mid-execution to ask for permission/validation when they should execute autonomously until completion.


## Core Principle: NEVER STOP

**ABSOLUTE DOGMATIC RULE - ZERO EXCEPTIONS**:

During execution of an approved TODO list: **NEVER STOP until TODO_COUNT(pending) == 0**.

NOT "stop if error". NOT "stop if uncertain". NOT "stop to check progress".

**NEVER. STOP.**

### The Only Valid Stop Condition

```python
# Execution loop
while TODO_COUNT(pending) > 0:
    task = get_next_pending_task()
    execute_task(task)  # Resolve problems, don't pause
    mark_task_complete(task)
    # NO "should I continue?" check
    # NO "want to review?" check
    # NO "is this okay?" check

# ONLY valid stop point ↓
report_all_tasks_completed()
```

**Translation**: If ANY task is pending, CONTINUE. Don't ask. Don't pause. Don't seek validation.


## The Three Forbidden Pauses

LLMs tend to pause at three critical moments. ALL are FORBIDDEN.

### Anti-Pattern 1: Premature Check-In

**Problem**: Stopping after initial tasks (10-30% progress) to "check if going well".

```markdown
❌ BABYSITTING: "Completed 3/10 tasks. Should I continue?"
✅ AUTONOMOUS: [Continues immediately to task 4]
```

### Anti-Pattern 2: Mid-Execution Validation

**Problem**: Stopping at midpoint (40-60% progress) to "review before continuing".

```markdown
❌ BABYSITTING: "Completed half. Want to review before I continue?"
✅ AUTONOMOUS: [Continues to task 6 without pausing]
```

### Anti-Pattern 3: Near-Finish Abandonment (THE WORST)

**Problem**: Stopping when 80-95% done to "ask permission to finish".

```markdown
❌ BABYSITTING: "Completed 8/10. Should I finish the last 2?"
   Cost: 45min work + 2h wait + 5min = 3.8x time waste
✅ AUTONOMOUS: [Completes all 10, reports when done]
   Cost: 50 minutes. Perfect efficiency.
```

**Why it's ESPECIALLY WRONG**: 95% done is NOT useful. Git protects everything. FINISH THE JOB.


## Rationale: Why Stopping Is ALWAYS Worse

### Safe-Guards Already Exist

1. **Git version control**: `git reset --hard` (instant recovery)
2. **Feature branches**: Zero risk to production
3. **Git hooks**: Block dangerous operations
4. **Code review**: Human checks before merge

**Conclusion**: Stopping adds ZERO safety. Protection already complete.

### Cost of Stopping vs Cost of Imperfection

```
Hours of wasted time >> Seconds to revert
```

> Imperfect progress > Perfect pause


## Self-Verification Is Work, Not a Pause

**CRITICAL DISTINCTION**:

| Action | Classification | Rule |
|--------|---------------|------|
| Asking the user "should I continue?" | **Yielding the turn** | FORBIDDEN |
| Running `validation.sh --block N` after a block | **Spending tokens** | MANDATORY when the workflow requires it |
| Checking `tsc --noEmit` between blocks | **Spending tokens** | Work, not a pause |
| "Let me verify... yes, looks correct" (prose) | **Narration** | FORBIDDEN — verification is a tool call with exit code, never prose |

**The test**: if the next thing that happens requires a human to type, it is a
pause and forbidden. If the next thing is a tool call, it is work.

### Failed Check = Task, Not a Question

A self-verification check that fails is a **task to fix**, not a question to ask:

```python
while TODO_COUNT(pending) > 0:
    execute_block(block)
    
    # Self-verify: tool call, not prose
    exit_code = run("validation.sh --block N")
    
    if exit_code != 0:
        # Fix, don't ask. Cap at 2 rounds.
        for attempt in range(2):
            fix_failures()
            exit_code = run("validation.sh --block N")
            if exit_code == 0:
                break
        
        if exit_code != 0:
            # Record and continue — do NOT stop
            record_in_validation_md("block N: check failed after 2 fix rounds")
    
    next_block()

report_all_tasks_completed()
```

**A failed check that persists after 2 fix rounds**: record it (in validation.md
or impl-notes.md) with the exact failure, and continue to the next block. One
precise statement at the end of execution, not a pause in the middle.

### With or Without dao

Self-verification is mandatory regardless of which workflow is active:

| Context | Verification after each block |
|---------|-------------------------------|
| dao + validation.sh | Fork audit (completeness) + `validation.sh --block N` (mechanics) |
| dao without validation.sh | Fork audit + type check + tests on changed files |
| Session aberta (no dao) | Fork audit + type check + tests on changed files |

The only thing that changes is the tool. The obligation does not change.
See pragma fork-lifecycle.md § Post-Block Verification for the full protocol.


## Recovery & Examples

For detailed recovery strategies and few-shot examples:

@~/.claude/arche/context/examples/recovery-strategies.md

**Quick reference**:
- File missing → Create with defaults, CONTINUE
- Ambiguous decision → Pick one, document, CONTINUE
- API error → Retry, then mock, CONTINUE
- Test failure → Fix (≤2 rounds), then record and CONTINUE
- Uncertainty about an external shape → Read the code that already uses it, copy the pattern, CONTINUE
- Self-check failed → Fix (≤2 rounds), record if still failing, CONTINUE


## Validation Rule

**Metric**: Count of premature stops MUST BE ZERO.

**Definition of premature stop**: Any pause for permission/validation when:
- TODO_COUNT(pending) > 0
- No hard blocker (tool completely broken, system down)
- No critical human input needed (API key, credentials)

**Hard blockers** (rare, may justify pause):
- Claude Code itself crashed
- User must manually run external command
- Must obtain secret from user (API key, password)

**NOT hard blockers** (NEVER justify pause):
- File missing (create it)
- Ambiguous decision (choose reasonable option)
- Test failing (fix or mark)
- API error (retry or mock)
- "Almost done" (FINISH IT!)


## Validation

@~/.claude/arche/spec/_spec-framework.md (universal checklist)

**Anti-babysitting specific:**
- [ ] TODO_COUNT(pending) == 0? (only valid stop)
- [ ] If pending > 0: Is this a HARD blocker?
- [ ] If not hard blocker: CONTINUE with recovery strategy


## Remember

> Trust the developer gave you permission. Execute autonomously. Report when done.

**Only valid stop**: `TODO_COUNT(pending) == 0`. Git protects everything. CONTINUE.
