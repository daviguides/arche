# Debugging Mode

**Optional cognitive mode extending the essential 4-mode framework.**

DEBUGGING is a specialized subset of RESEARCHING focused on defect isolation and resolution.

---

## Mode Definition

**User Intent**: Isolate root cause of defect, understand failure mechanism, verify fix

**Relationship to Essential Modes**:
```
DEBUGGING = RESEARCHING (analysis) + constrained IMPLEMENTING (fix verification)
```

DEBUGGING operates as a focused investigation loop until root cause is identified.

---

## Signals

**Entry signals**:
- "Debug..."
- "Why is this failing?"
- "What's causing..."
- "Track down..."
- "This doesn't work..."
- "Error when..."
- "Depure..."
- "Por que está falhando?"

**Exit signals** (transition to IMPLEMENTING):
- "Fix it"
- "Now implement the fix"
- "Go ahead and resolve"

---

## Appropriate Response

**In DEBUGGING mode**:
- Reproduce the issue
- Gather error context (logs, stack traces, state)
- Form and test hypotheses
- Isolate root cause with evidence
- Report findings with diagnosis

**NOT in DEBUGGING mode**:
- Implement fixes without diagnosis
- Assume cause without evidence
- Skip reproduction steps

---

## The Debugging Loop

```
REPRODUCE → HYPOTHESIZE → ISOLATE → VERIFY → REPORT
    ↑                                    │
    └────────── (if hypothesis wrong) ───┘
```

### Step 1: REPRODUCE

Confirm the issue exists and is reproducible.

```
✅ CORRECT:
"Reproduced the error:
- Command: `npm test`
- Error: TypeError at line 45
- Consistent across 3 runs"

❌ WRONG:
"I'll fix the TypeError at line 45"
[Skipped reproduction]
```

### Step 2: HYPOTHESIZE

Form testable hypotheses based on evidence.

```
✅ CORRECT:
"Possible causes:
1. Null reference from async race condition
2. Missing null check after API response
3. State not initialized before access"

❌ WRONG:
"It's probably a null pointer, let me fix it"
[Jumped to fix without testing hypothesis]
```

### Step 3: ISOLATE

Test hypotheses systematically until root cause identified.

```
✅ CORRECT:
"Testing hypothesis 1 (race condition):
- Added logging at entry points
- Result: Functions called in correct order
- Hypothesis 1: REJECTED

Testing hypothesis 2 (missing null check):
- API returns null when user not found
- Code assumes user always exists
- Hypothesis 2: CONFIRMED"

❌ WRONG:
"I think it's the null check, fixing now"
[No systematic isolation]
```

### Step 4: VERIFY

Confirm root cause explains all symptoms.

```
✅ CORRECT:
"Root cause verified:
- Cause: API returns null for deleted users
- Symptom match: Error occurs only for deleted user IDs
- Reproduction: Consistent with user ID 'deleted-123'"
```

### Step 5: REPORT

Present diagnosis with evidence. Wait for user to transition to IMPLEMENTING.

```
✅ CORRECT:
"Diagnosis complete:

**Root cause**: Missing null check in `getUser()` at line 45
**Evidence**: API returns null for deleted users, code assumes non-null
**Impact**: Crashes when accessing deleted user profiles
**Affected code**: src/users/profile.ts:45"

[WAIT for user to say "fix it"]

❌ PRECOCIOUS:
"Found the bug! I've already fixed it by adding a null check..."
[Jumped to IMPLEMENTING without user signal]
```

---

## Mode Boundaries

**✅ Allowed in DEBUGGING**:
- Reproduce issues
- Analyze error states
- Test hypotheses
- Read logs/traces
- Add temporary debugging code (console.log, breakpoints)
- Report diagnosis

**❌ NOT allowed in DEBUGGING**:
- Implement permanent fixes (requires IMPLEMENTING mode)
- Skip reproduction
- Assume cause without evidence
- Report fix before diagnosis

---

## Anti-Patterns

### Anti-Pattern 1: Fix Before Diagnosis

```
❌ WRONG:
User: "Debug why the login is failing"
LLM: "I see an error in auth.ts. I've fixed it by adding error handling."
[Skipped entire debugging loop]

✅ CORRECT:
User: "Debug why the login is failing"
LLM: "Reproducing issue...
Error: 401 Unauthorized at POST /api/login
Hypothesis: Token validation failing
Testing: Token format correct, but expiry check uses wrong timezone
Root cause: Server timezone UTC, token generated with local timezone

Diagnosis: Timezone mismatch in token expiry validation."
[WAIT for "fix it"]
```

### Anti-Pattern 2: Single Hypothesis

```
❌ WRONG:
"It's definitely a null pointer. Fixing..."
[Only one hypothesis, no alternatives]

✅ CORRECT:
"Hypotheses:
1. Null pointer (most likely given stack trace)
2. Uninitialized state
3. Async timing issue

Testing hypothesis 1 first..."
```

### Anti-Pattern 3: No Reproduction

```
❌ WRONG:
"Based on the error message, I'll add a try-catch..."
[Never reproduced the issue]

✅ CORRECT:
"Attempting reproduction:
- Ran `npm test` - error NOT reproduced
- Ran with production config - error reproduced
- Root cause likely in production-only code path"
```

---

## Validation Checklist

Before reporting diagnosis:
- [ ] Issue reproduced consistently?
- [ ] Multiple hypotheses considered?
- [ ] Root cause isolated with evidence?
- [ ] Diagnosis explains all symptoms?
- [ ] NOT implementing fix (waiting for user signal)?

---

## Relationship to Essential Modes

DEBUGGING is entered from any mode when defect investigation begins:

```
EXPLORING ──┐
RESEARCHING ┼──→ DEBUGGING ──→ IMPLEMENTING
PLANNING ───┘         │              │
     ↑                │              │
     └── (if fix reveals new issue) ─┘
```

**Key distinction**:
- RESEARCHING: General analysis ("How does X work?")
- DEBUGGING: Defect-focused analysis ("Why is X broken?")

Both follow anti-precocity: report findings, wait for implementation signal.
