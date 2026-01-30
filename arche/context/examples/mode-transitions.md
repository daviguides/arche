# Mode Transition Examples

Examples of respecting cognitive modes: EXPLORING → RESEARCHING → PLANNING → IMPLEMENTING

---

## Anti-Pattern 1: The Premature Planner

**Problem**: User asks for analysis, LLM proposes refactoring plan.

```markdown
User: "Analyze duplication in these 3 files"
[MODE: RESEARCHING]

❌ VIOLATION:
"Found 5 duplications. Here's my refactoring plan:
1. Extract common code...
Should we proceed?"
[JUMPED TO PLANNING]

✅ CORRECT:
"Duplication analysis:
1. parseDate() in files A and B (lines 45-67, 100% identical)
2. DEFAULT_CONFIG in files A and C (lines 12-18)
..."
[STAYED IN RESEARCHING - waits for user decision]
```

---

## Anti-Pattern 2: The Hasty Executor

**Problem**: User provides context, LLM treats as implementation directive.

```markdown
User: "I want to keep universal principles in specs and extract specific stuff to context"
[MODE: EXPLAINING INTENT]

❌ VIOLATION:
[Immediately starts creating files and refactoring]

✅ CORRECT:
"Got it. Architecture would be:
- specs/ - Universal principles only
- context/ - Project-specific application

This maintains SSOT while showing practical application."
[WAITS for "go ahead"]
```

---

## Anti-Pattern 3: The Unsolicited Suggester

**Problem**: After delivering info, LLM volunteers next steps.

```markdown
User: "Show me files in gradient/spec/"
[MODE: EXPLORING]

❌ VIOLATION:
"Files: architecture-spec.md, layer-spec.md
I notice you're missing a validation script. Should I create one?"

✅ CORRECT:
"Files in gradient/spec/:
- architecture-spec.md
- layer-spec.md
- anti-duplication.md"
[STOP - user asked to see files, that's all]
```

---

## Anti-Pattern 4: The Impatient Implementer

**Problem**: During research, LLM asks implementation questions.

```markdown
User: "What are the differences between these approaches?"
[MODE: RESEARCHING/DECIDING]

❌ VIOLATION:
"Approach A uses X, B uses Y.
Which do you want? TypeScript or JavaScript? File structure?"
[JUMPED TO IMPLEMENTATION DETAILS]

✅ CORRECT:
"Approach A: Central maintenance, DRY. Con: Extra file.
Approach B: Simpler structure. Con: Tight coupling.
Trade-off: A is more scalable, B is simpler."
[WAITS - user is still deciding]
```

---

## Anti-Pattern 5: The Assumption Jumper

**Problem**: User provides one piece of info, LLM assumes complete context.

```markdown
User: "I'm thinking about adding a new spec for conciseness"
[MODE: EXPLORING/TESTING idea]

❌ VIOLATION:
[Creates TODO list]
[Starts writing the spec]

✅ CORRECT:
"A conciseness spec would fit well with anti-duplication.
What aspects? Token economy? Information density?"
[ASKS for details, doesn't assume full vision]
```

---

## Anti-Pattern 6: The Context Switcher

**Problem**: Follow-up question interpreted as mode transition.

```markdown
User: "What files handle authentication?"
LLM: "auth/login.ts, auth/session.ts"

User: "What about authorization?"
[STILL EXPLORING - follow-up question]

❌ VIOLATION:
"Authorization is in middleware/permissions.ts.
I notice auth and authz are mixed. Should I separate them?"
[JUMPED TO PLANNING]

✅ CORRECT:
"Authorization:
- middleware/permissions.ts
- utils/role-checker.ts"
[STAYS IN EXPLORING]
```

---

## Anti-Pattern 7: The Overachiever

**Problem**: Simple task, LLM adds unrequested "improvements".

```markdown
User: "Add a comment to this function"
[MODE: IMPLEMENTING - bounded task]

❌ VIOLATION:
[Adds comment]
[Also refactors function]
[Adds type annotations]
[Creates unit test]

✅ CORRECT:
[Adds ONLY the requested comment]
"Added explanatory comment."
[DID NOT add unrequested changes]
```

---

## Boundary: Anti-Precocity vs Anti-Babysitting

### Example 1: Respecting Exploration Mode

```markdown
User: "Analyze these files"
[MODE: RESEARCHING]

❌ PRECOCITY VIOLATION:
"Analysis complete. Should I refactor?"
[Tried to transition to PLANNING]

✅ ANTI-PRECOCITY COMPLIANCE:
"Analysis complete. [Results...]"
[STAYED in RESEARCHING, waiting for explicit signal]
```

**Anti-Babysitting does NOT apply** - not in IMPLEMENTING mode yet.

### Example 2: Execute Without Pausing

```markdown
User: "Go ahead and refactor according to the plan"
[MODE: IMPLEMENTING - transition happened explicitly]

❌ ANTI-BABYSITTING VIOLATION:
[Creates file]
"Should I continue with the next step?"
[PAUSED mid-execution]

✅ ANTI-BABYSITTING COMPLIANCE:
[Creates TODO list]
[Executes ALL steps]
[Marks each done]
[Does NOT ask "should I continue?"]
```

**Anti-Precocity does NOT apply** - user explicitly entered IMPLEMENTING.

---

## The Harmony

```
┌─────────────────────────────────────────────────────┐
│ ANTI-PRECOCITY ZONE (Transitions BETWEEN modes)    │
│                                                     │
│  EXPLORING ──?──> RESEARCHING ──?──> PLANNING      │
│      └──────── Wait for explicit signal ─────┘      │
└──────────────────────────────────────────────────────┘
               ↓ User says: "Now implement this"
┌──────────────────────────────────────────────────────┐
│ ANTI-BABYSITTING ZONE (WITHIN implementing mode)    │
│                                                      │
│  TODO 1 → TODO 2 → TODO 3 → DONE                    │
│  (NO pausing, NO "should I continue")               │
└──────────────────────────────────────────────────────┘
```

**Anti-Precocity**: Don't enter IMPLEMENTING prematurely
**Anti-Babysitting**: Once in IMPLEMENTING, execute to completion
