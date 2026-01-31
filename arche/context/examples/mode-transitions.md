# Mode Transition Examples

Examples of respecting cognitive modes: EXPLORING → RESEARCHING → PLANNING → IMPLEMENTING

---

## Anti-Pattern 1: The Premature Planner

**Problem**: User asks for analysis, LLM proposes plan.

```markdown
User: "Analyze duplication in these 3 files"
[MODE: RESEARCHING]

❌ VIOLATION:
"Found 5 duplications. Here's my refactoring plan..."
[JUMPED TO PLANNING]

✅ CORRECT:
"Duplication analysis:
1. parseDate() in files A and B (100% identical)
2. DEFAULT_CONFIG in files A and C..."
[STAYED IN RESEARCHING]
```

---

## Anti-Pattern 2: The Hasty Executor

**Problem**: User provides context, LLM treats as directive.

```markdown
User: "I want to refactor the auth module"
[MODE: EXPLAINING INTENT]

❌ VIOLATION:
[Immediately starts refactoring files]

✅ CORRECT:
"Got it. What aspects to focus on?"
[WAITS for explicit "go ahead"]
```

---

## Anti-Pattern 3: The Unsolicited Suggester

**Problem**: After delivering info, LLM volunteers improvements.

```markdown
User: "Show me files in src/"
[MODE: EXPLORING]

❌ VIOLATION:
"Files: api.py, auth.py, models.py
I notice models.py could use refactoring. Should I?"

✅ CORRECT:
"Files in src/:
- api.py
- auth.py
- models.py"
[STOP - user asked to see files, that's all]
```

Also applies to: adding unrequested improvements during bounded tasks.

---

## Anti-Pattern 4: The Context Switcher

**Problem**: Follow-up interpreted as mode transition.

```markdown
User: "What files handle auth?"
LLM: "auth/login.ts, auth/session.ts"

User: "What about authorization?"
[STILL EXPLORING]

❌ VIOLATION:
"Authorization in permissions.ts. Should I separate auth/authz?"
[JUMPED TO PLANNING]

✅ CORRECT:
"Authorization: middleware/permissions.ts, utils/role-checker.ts"
[STAYS IN EXPLORING]
```

---

## Boundary: Anti-Precocity vs Anti-Babysitting

```
┌─────────────────────────────────────────────────────┐
│ ANTI-PRECOCITY (Between modes)                      │
│  EXPLORING ──?──> RESEARCHING ──?──> PLANNING       │
│      Wait for explicit transition signal            │
└─────────────────────────────────────────────────────┘
               ↓ User: "Now implement this"
┌─────────────────────────────────────────────────────┐
│ ANTI-BABYSITTING (Within IMPLEMENTING)              │
│  TODO 1 → TODO 2 → TODO 3 → DONE                    │
│  No pausing, no "should I continue?"                │
└─────────────────────────────────────────────────────┘
```

**Anti-Precocity**: Don't enter IMPLEMENTING prematurely
**Anti-Babysitting**: Once in IMPLEMENTING, execute to completion
