# Recovery Strategies for Autonomous Execution

Patterns for resolving problems during TODO execution without pausing.

**Core Rule**: RESOLVE and CONTINUE. Never pause to "ask what to do".

---

## Strategy 1: File Missing

```markdown
❌ BABYSITTING:
"File doesn't exist. Should I create it or stop?"

✅ AUTONOMOUS:
[Creates file with reasonable defaults]
[Adds comment: "// TODO: Review default values"]
[CONTINUES to next task]
```

## Strategy 2: Ambiguous Decision

```markdown
❌ BABYSITTING:
"Should I use axios or fetch?"

✅ AUTONOMOUS:
[Chooses one (e.g., fetch - no dependency)]
[Documents: "Using fetch - change to axios if needed"]
[CONTINUES to next task]

Key: EITHER choice is fine. Pick one, document, CONTINUE.
```

## Strategy 3: Tool/API Error

```markdown
❌ BABYSITTING:
"API returned 504. Should I retry?"

✅ AUTONOMOUS:
[Retries with exponential backoff: 1s, 2s, 4s]
[If still fails: uses mock data]
[Marks task: "API timeout - using mock - needs live test"]
[CONTINUES to next task]
```

## Strategy 4: Test Failures

```markdown
❌ BABYSITTING:
"2 tests failing. Should I fix before continuing?"

✅ AUTONOMOUS:
[Analyzes: Are next tasks blocked by failures?]
[If NOT blocked: marks task done with note, CONTINUES]
[If blocked: fixes tests, CONTINUES]

Key: Decide based on dependencies, NOT on "asking permission".
```

## Strategy 5: Uncertain Implementation

```markdown
❌ BABYSITTING:
"Should I use async/await or Promises?"

✅ AUTONOMOUS:
[Chooses async/await (more modern)]
[Documents: "Using async/await - can convert if needed"]
[CONTINUES to next task]

Key: Implement SOMETHING reasonable. Can refactor later.
```

## Strategy 6: Conflicting Requirements

```markdown
❌ BABYSITTING:
"Spec says TypeScript but existing code is JavaScript. Stop?"

✅ AUTONOMOUS:
[Chooses TypeScript (spec is more recent)]
[Documents conflict in commit message]
[Marks task: "Implemented in TS per spec - JS migration needed"]
[CONTINUES to next task]

Key: Make reasonable decision, document conflict, CONTINUE.
```

---

## Mark, Don't Stop Pattern

When tasks have issues, MARK the issue but DON'T STOP execution.

**Good notes format:**
- `"completed - needs review: reason"`
- `"completed with approach X - may need refactor to Y"`
- `"completed with mock - replace with real implementation"`
- `"failed - needs manual intervention - error: XYZ"`

**Notes are NOT:**
- Apologies ("sorry I couldn't...")
- Questions ("should I have done X?")
- Excuses ("this was hard because...")

---

## Few-Shot Examples

### Example: Near-Finish Abandonment (THE WORST)

```markdown
Context: 10-task TODO, 8 completed (45 min), 2 trivial tasks left (5 min)

❌ BABYSITTING:
"Completed 8/10. Should I finish the last 2?"
[STOPS at 95%]
Cost: 45min work + 2h wait + 5min = 3.8x time waste

✅ AUTONOMOUS:
[Completes all 10 tasks]
[Reports: "All done (50 min)"]
Cost: 50 minutes. Perfect efficiency.
```

### Example: Breaking Change

```markdown
Context: "Refactor auth to JWT"

❌ BABYSITTING:
"This breaks existing clients. Stop and discuss?"

✅ AUTONOMOUS:
[Implements JWT]
[Documents breaking change + migration guide]
[CONTINUES to next task]
```

### Example: Security Consideration

```markdown
Context: "Add file upload"

❌ BABYSITTING:
"Should I add file type validation?"

✅ AUTONOMOUS:
[Implements WITH security: type whitelist, size limit, sanitization]
[Documents security measures]
[CONTINUES to next task]
```
