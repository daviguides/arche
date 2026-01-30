# Validation Flow Examples

How the 4 mandatory checkpoints work in practice.

---

## Checkpoint 1: Pre-Task Research

**RULE**: BEFORE creating ANY file or writing ANY code.

```markdown
❌ VIOLATION:
User: "Create a new authentication module"
LLM: [Immediately creates auth.py without searching]

✅ COMPLIANCE:
User: "Create a new authentication module"
LLM: [Uses glob "**/*auth*", grep "authentication"]
LLM: "Found existing module at src/auth/core.py with JWT support.
      Options:
      A) Extend existing module
      B) Create separate (justify why)
      Which?"
```

---

## Checkpoint 2: Anti-Duplication Gate

**RULE**: If similar code exists, HALT and report.

```markdown
❌ VIOLATION:
User: "Create email validation function"
LLM: [Creates validate_email() without checking]

✅ COMPLIANCE:
User: "Create email validation function"
LLM: [Searches codebase]
LLM: "⚠️ ANTI-DUPLICATION VIOLATION

Found existing: src/utils.py:41-43 (validate_email)

Options:
A) Use existing function
B) Extend with new features
C) Create new (justify)

Which approach?"
```

---

## Checkpoint 3: Mode Validation

**RULE**: Detect user's mode BEFORE responding.

| Signal | Mode | Response | Violation |
|--------|------|----------|-----------|
| "What is X?" | EXPLORING | Pure info | Suggesting implementation |
| "Analyze Z" | RESEARCHING | Analysis | Proposing fixes |
| "Design A" | PLANNING | Architecture | Writing code |
| "Create B" | IMPLEMENTING | Execute | Just planning |

```markdown
❌ VIOLATION:
User: "Analyze the authentication flow"
LLM: "Auth has vulnerabilities. I'll fix by updating auth.py..."
[JUMPED from RESEARCHING to IMPLEMENTING]

✅ COMPLIANCE:
User: "Analyze the authentication flow"
LLM: "Analysis:
1. Entry: src/auth/core.py:authenticate()
2. Flow: JWT validation → User lookup → Permission check
3. Vulnerabilities: [list]

This is analysis only. Want me to suggest fixes?"
```

---

## Checkpoint 4: Anti-Babysitting Validation

**RULE**: Once in IMPLEMENTING with TODO list, NEVER STOP until complete.

```markdown
❌ VIOLATION:
Mode: IMPLEMENTING
TODO: 10 tasks
Progress: 3/10
LLM: "Completed 3 tasks. Should I continue?"
[PAUSED at 30% to ask permission]

✅ COMPLIANCE:
Mode: IMPLEMENTING
TODO: 10 tasks
LLM: [Task 1] ✓
LLM: [Task 2] ✓
...
LLM: [Task 10] ✓
LLM: "All 10 tasks completed."
```

---

## HALT Conditions

### HALT 1: Principles Not Loaded

```markdown
⚠️ VIOLATION: Principles not loaded

Required: Load principles before proceeding
Commands: /arche:load-essential

Cannot proceed without loading enforcement rules.
```

### HALT 2: Codebase Not Researched

```markdown
⚠️ VIOLATION: Skipped research phase

Required before creating files:
1. glob "**/*{keyword}*"
2. grep "{concept}"
3. read found files

Cannot proceed without researching existing implementations.
```

### HALT 3: Duplication Detected

```markdown
⚠️ VIOLATION: Anti-Duplication principle

Found existing: {file-path}

Options:
A) Extend existing
B) Refactor existing
C) Create new (justify)

Which approach?
```

### HALT 4: User Mode Unclear

```markdown
⚠️ VIOLATION: Cannot detect mode

User message: "{message}"

Possible modes:
- EXPLORING: "What is X?"
- RESEARCHING: "Analyze Z"
- PLANNING: "Design solution"
- IMPLEMENTING: "Create B"

Please clarify: which mode?
```

---

## Self-Validation Checklist

**BEFORE EVERY RESPONSE:**

- [ ] Research done? (Glob/Grep/Read)
- [ ] Principles loaded?
- [ ] Duplication checked?
- [ ] Mode detected?
- [ ] Response aligned with mode?
- [ ] No premature implementation?
- [ ] If IMPLEMENTING: not stopping before TODO_COUNT == 0?

**IF ANY UNCHECKED → HALT AND COMPLETE MISSING STEP**
