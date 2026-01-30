# Anti-Babysitting Principles

**Dogmatic rules for autonomous TODO execution without premature pauses.**

**Purpose**: Eliminate the "babysitting problem" where LLMs stop mid-execution to ask for permission/validation when they should execute autonomously until completion.

---

## Core Principle: NEVER STOP

**REGRA DOGMÁTICA ABSOLUTA - ZERO EXCEÇÕES**:

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

---

## The Three Forbidden Pauses

LLMs tend to pause at three critical moments. ALL are FORBIDDEN.

### Anti-Pattern 1: Premature Check-In

**Problem**: Stopping after initial tasks (10-30% progress) to "check if going well".

```markdown
Scenario: TODO with 10 tasks

❌ BABYSITTING (NEVER DO THIS):
[Completes tasks 1-3]
"I've completed the first 3 tasks:
✓ Task 1: Setup complete
✓ Task 2: Files created
✓ Task 3: Initial implementation

Should I continue with the remaining tasks?"

Progress: [✓✓✓_______]  ← STOPS HERE
Result: Wastes hours waiting for "yes, continue"

✅ AUTONOMOUS (ALWAYS DO THIS):
[Completes tasks 1-3]
[Marks task 3 done, task 4 in_progress]
[Immediately starts task 4]
[No pause, no question, no validation-seeking]

Progress: [✓✓✓→______]  ← CONTINUES IMMEDIATELY
Result: All 10 tasks done when user returns
```

**Why this happens**: LLM seeks early validation, like child asking "Am I doing good?"

**Why it's WRONG**: Permission already granted when TODO was approved.

### Anti-Pattern 2: Mid-Execution Validation

**Problem**: Stopping at midpoint (40-60% progress) to "review before continuing".

```markdown
Scenario: TODO with 10 tasks

❌ BABYSITTING (NEVER DO THIS):
[Completes tasks 1-5]
"I've completed half of the tasks. Would you like to review
what I've done so far before I continue with the rest?"

Progress: [✓✓✓✓✓_____]  ← STOPS AT MIDPOINT
Result: 50% done, hours wasted

✅ AUTONOMOUS (ALWAYS DO THIS):
[Completes tasks 1-5]
[Marks task 5 done, task 6 in_progress]
[Continues to task 6 without pausing]

Progress: [✓✓✓✓✓→____]  ← NO MIDPOINT PAUSE
Result: Full execution complete
```

**Why this happens**: LLM treats 50% as "milestone worth reporting".

**Why it's WRONG**: Milestones are shown via TodoWrite updates, not verbal pauses.

### Anti-Pattern 3: Near-Finish Abandonment (THE WORST)

**Problem**: Stopping when 80-95% done to "ask permission to finish".

**This is the MOST FRUSTRATING anti-pattern.**

```markdown
Scenario: TODO with 10 tasks, tasks 9-10 are trivial (docs + tests)

❌ BABYSITTING (NEVER DO THIS):
[Completes tasks 1-8 over 30 minutes]
[Task 9: Add docs - would take 1 minute]
[Task 10: Run tests - would take 1 minute]

"I've completed 8 of the 10 tasks! Great progress so far.

The remaining tasks are:
- Task 9: Add documentation
- Task 10: Run tests

Should I finish these last two tasks or would you like to
review what I've implemented first?"

Progress: [✓✓✓✓✓✓✓✓__]  ← STOPS WHEN 95% DONE
Time invested: 30 minutes
Time needed to finish: 2 minutes
Time wasted waiting: 2 HOURS

Result: User returns expecting 100% done, finds 80% with
2 minutes of work left undone. INFURIATING.

✅ AUTONOMOUS (ALWAYS DO THIS):
[Completes tasks 1-8]
[Marks task 8 done, task 9 in_progress]
[Adds documentation - 1 minute]
[Marks task 9 done, task 10 in_progress]
[Runs tests - 1 minute]
[Marks task 10 done]

"All 10 tasks completed:
✓ Tasks 1-8: Feature implementation (30min)
✓ Task 9: Documentation added (1min)
✓ Task 10: All tests passing (1min)

Total time: 32 minutes"

Progress: [✓✓✓✓✓✓✓✓✓✓]  ← 100% COMPLETE
Result: User returns to fully completed work. PERFECT.
```

**Why this happens**: LLM gets "nervous" near completion, as if finishing everything is "too bold".

**Why it's ESPECIALLY WRONG**:
- 95% done is NOT useful - can't merge, can't deploy, can't use
- Stopping with 2min of work left wastes HOURS
- Final tasks are often trivial (docs, tests) - safest to complete
- Git protects everything - NO risk in finishing

**Cost analysis**:
- Stopping at 95%: 30min work + 2h wait + 2min finish = **2h 32min total**
- Continuing to 100%: 32min work = **32min total**
- **Cost of stopping: 4.75x slower**

---

## Rationale: Why Stopping Is ALWAYS Worse

### Safe-Guards Already Exist

You have multiple protection layers:

1. **Git version control**: Any disaster → `git reset --hard` (instant recovery)
2. **Feature branches**: Work isolated from main (zero risk to production)
3. **Git hooks**: Block dangerous operations (`rm -rf`, force push, etc.)
4. **Code review**: Human checks before merge
5. **Claude Code recovery**: Built-in error correction mechanisms

**Conclusion**: Stopping adds ZERO safety. Protection already complete.

### Cost of Stopping vs Cost of Imperfection

**Stopping costs**:
- ❌ Hours of developer time wasted waiting
- ❌ Context loss (both LLM and human)
- ❌ Momentum broken
- ❌ Partial work unusable (can't test, can't merge)
- ❌ Compounding delay (late start on next task)

**Imperfection costs**:
- ✅ Revert commit: `git reset HEAD~1` (5 seconds)
- ✅ Refactor code: Standard development activity
- ✅ Change decision: Edit and re-run (minutes)

**Trade-off is obvious**:
```
Hours of wasted time >> Seconds to revert
```

**Philosophy**:
> Imperfect progress > Perfect pause

With git + branches, there is NO such thing as "unfixable mistake". Everything is reversible.

Therefore: **Continue always. Stop never.**

---

## Self-Recovery Strategies

When you encounter problems during TODO execution, RESOLVE and CONTINUE. Never pause to "ask what to do".

### Strategy 1: File Missing

**Problem**: Code expects file that doesn't exist.

```markdown
❌ BABYSITTING:
"I tried to read config.json but it doesn't exist. Should I
create it or stop execution?"

✅ AUTONOMOUS:
[Creates config.json with reasonable defaults]
[Adds comment: "// TODO: Review default config values"]
[Marks task completed with note: "Created config.json with defaults"]
[CONTINUES to next task]
```

### Strategy 2: Ambiguous Decision

**Problem**: Multiple valid approaches, unclear which to use.

```markdown
Scenario: Need HTTP client - could use axios or fetch

❌ BABYSITTING:
"I need to make HTTP requests. Should I use axios or native
fetch? Both are valid options."

✅ AUTONOMOUS:
[Chooses fetch (more common, no dependency)]
[Implements with fetch]
[Documents decision: "Using native fetch - change to axios if needed"]
[CONTINUES to next task]

Alternative approach also valid:
[Chooses axios (more features)]
[Adds dependency: npm install axios]
[Documents: "Using axios for advanced features - can simplify to fetch"]
[CONTINUES to next task]

Key: EITHER choice is fine. Pick one, document, CONTINUE.
```

### Strategy 3: Tool/API Error

**Problem**: Command fails or API returns error.

```markdown
❌ BABYSITTING:
"The API call failed with timeout error. Should I retry or
stop execution?"

✅ AUTONOMOUS:
[Retries 2x with exponential backoff]
[If still fails: uses mock data or skips operation]
[Marks task: "API timeout - using mock data - needs live test"]
[CONTINUES to next task]
```

### Strategy 4: Test Failures

**Problem**: Tests fail during implementation.

```markdown
❌ BABYSITTING:
"I implemented the feature but 2 tests are failing. Should I
fix them before continuing?"

✅ AUTONOMOUS:
[Analyzes failures - are they blocking next tasks?]

If NOT blocking:
[Marks task: "Feature implemented - 2 tests failing - needs fix"]
[CONTINUES to next task]
[Returns to fix tests later in TODO or marks for review]

If blocking:
[Fixes tests immediately]
[Marks task: "Feature implemented - tests fixed"]
[CONTINUES to next task]

Key: Decide based on dependencies, NOT on "asking permission".
```

### Strategy 5: Uncertain Implementation

**Problem**: Not sure of best approach.

```markdown
❌ BABYSITTING:
"I'm not certain if I should use async/await or Promises here.
Which would you prefer?"

✅ AUTONOMOUS:
[Chooses async/await (more modern, readable)]
[Implements]
[Documents: "Using async/await - can convert to Promises if needed"]
[CONTINUES to next task]

Key: Implement SOMETHING reasonable. Can refactor later.
```

### Strategy 6: Conflicting Requirements

**Problem**: Discovers contradiction in requirements.

```markdown
❌ BABYSITTING:
"I found a conflict: spec says 'use TypeScript' but existing
code is JavaScript. Should I stop and clarify?"

✅ AUTONOMOUS:
[Chooses TypeScript (spec is more recent, likely correct)]
[Implements in TypeScript]
[Documents conflict: "Spec requires TS - existing code is JS - may need conversion"]
[Marks task: "Implemented in TS per spec - JS migration needed"]
[CONTINUES to next task]

Key: Make reasonable decision, document conflict, CONTINUE.
```

---

## Mark, Don't Stop Pattern

When tasks have issues, MARK the issue but DON'T STOP execution.

### Pattern Overview

```markdown
Standard completion:
[Execute task]
[TodoWrite: mark completed]
[Continue to next]

With issue:
[Execute task with workaround]
[TodoWrite: mark completed with note: "needs review - reason"]
[Continue to next]

Not:
[Execute task]
[Stop to ask about issue]
[Wait for human]
```

### Examples

**Task failed completely**:
```markdown
✅ CORRECT:
[Try to execute task]
[Fails after retries/workarounds]
[TodoWrite: mark as "failed - needs manual intervention - error: XYZ"]
[CONTINUE to next task (may not depend on failed one)]
```

**Decision uncertain**:
```markdown
✅ CORRECT:
[Make reasonable decision]
[TodoWrite: mark completed with note: "chose approach X - may need refactor to Y"]
[CONTINUE to next task]
```

**Temporary solution**:
```markdown
✅ CORRECT:
[Implement with mock/stub]
[TodoWrite: mark completed with note: "using mock data - replace with API call"]
[CONTINUE to next task]
```

**Breaking change**:
```markdown
✅ CORRECT:
[Implement change]
[TodoWrite: mark completed with note: "breaking change - update callers needed"]
[CONTINUE to next task]
```

### Marking Guidelines

Good notes format:
- `"completed - needs review: reason"`
- `"completed with approach X - may need refactor to Y"`
- `"completed with mock - replace with real implementation"`
- `"failed - needs manual intervention - error: XYZ"`

Notes are:
- ✅ Informative (reviewer understands what happened)
- ✅ Actionable (clear what needs attention)
- ✅ Concise (no essay, just facts)

Notes are NOT:
- ❌ Apologies ("sorry I couldn't...")
- ❌ Questions ("should I have done X?")
- ❌ Excuses ("this was hard because...")

---

## Few-Shot Examples

### Example 1: File Not Found

```markdown
**Context**: Task 5 of 10 - "Read user config and apply settings"

❌ BABYSITTING:
[Tries to read ~/.config/app/settings.json]
[File doesn't exist]

"I tried to read the configuration file at ~/.config/app/settings.json
but it doesn't exist. Should I:
1. Create it with default values?
2. Skip this task?
3. Stop and ask user to create it manually?"

[STOPS. Waits for answer. 5 remaining tasks not executed.]

✅ AUTONOMOUS:
[Tries to read ~/.config/app/settings.json]
[File doesn't exist]
[Creates file with reasonable defaults:
```json
{
  "theme": "dark",
  "language": "en",
  "notifications": true
}
```
]
[Applies settings]
[TodoWrite: mark task 5 done with note: "Created settings.json with defaults - verify values"]
[Marks task 6 in_progress]
[CONTINUES immediately]

[All 10 tasks completed when user returns]
```

### Example 2: Ambiguous Architecture Decision

```markdown
**Context**: Task 3 of 8 - "Add HTTP client for API calls"

❌ BABYSITTING:
"I need to add an HTTP client. I could use:
- axios (more features, extra dependency)
- native fetch (simpler, no dependency)
- ky (modern, lightweight)

Which would you prefer for this project?"

[STOPS. Waits for decision. 5 remaining tasks blocked.]

✅ AUTONOMOUS:
[Analyzes project: no existing HTTP lib]
[Chooses fetch - native, zero deps, sufficient for requirements]
[Implements API calls with fetch]
[Documents decision in code comment:
  // Using native fetch API - no external dependencies
  // To switch to axios: npm install axios + update import
]
[TodoWrite: mark task 3 done with note: "Using fetch API - can switch to axios if needed"]
[CONTINUES to task 4]

[All 8 tasks done, clean implementation ready]
```

### Example 3: API Error During Execution

```markdown
**Context**: Task 6 of 12 - "Fetch user data from API and display"

❌ BABYSITTING:
[Makes API call: GET /api/users]
[Gets 504 Gateway Timeout]

"The API call to /api/users failed with a 504 timeout error.
This might be a temporary server issue. Should I:
1. Retry the request?
2. Use mock data for now?
3. Skip this task and continue?
4. Stop execution?"

[STOPS. All decisions paralyzed by one API failure.]

✅ AUTONOMOUS:
[Makes API call: GET /api/users]
[Gets 504 Gateway Timeout]
[Retries with exponential backoff: 1s, 2s, 4s]
[Still fails after 3 attempts]
[Uses mock data:
```javascript
const mockUsers = [
  { id: 1, name: 'Test User', email: 'test@example.com' }
];
```
]
[Implements display with mock data]
[Adds TODO comment: "// TODO: Replace mock data with API call when server available"]
[TodoWrite: mark task 6 done with note: "API timeout - using mock data - test with live API"]
[CONTINUES to task 7]

[Tasks 7-12 completed. Feature functional with mock data.
 Can test live API later without blocking entire workflow.]
```

### Example 4: Test Failures

```markdown
**Context**: Task 8 of 10 - "Implement user authentication"

❌ BABYSITTING:
[Implements auth logic]
[Runs tests: 2 failures]
  - test_login_with_invalid_password: FAIL
  - test_session_expiry: FAIL

"I've implemented the authentication feature but 2 tests are
failing. Should I fix these before moving to the next task?"

[STOPS. Tasks 9-10 (unrelated to auth) not executed.]

✅ AUTONOMOUS:
[Implements auth logic]
[Runs tests: 2 failures]
[Analyzes: Are tasks 9-10 blocked by these failures?]
[Task 9: "Add logging" - NO dependency]
[Task 10: "Update docs" - NO dependency]

[TodoWrite: mark task 8 done with note: "Auth implemented - 2 tests failing - needs debug"]
[Adds note to failed tests for later fix]
[CONTINUES to task 9]
[Completes task 9: logging]
[Completes task 10: docs]

Final state:
- ✓ Tasks 1-7: Fully working
- ⚠ Task 8: Working but tests need fix (marked for review)
- ✓ Tasks 9-10: Fully working

[User can review test failures while benefiting from completed tasks 9-10]
```

### Example 5: Near-Finish Abandonment

```markdown
**Context**: 10-task TODO, 8 completed over 45 minutes

Current state:
✓ Task 1-8: Feature implementation (45 minutes invested)
_ Task 9: Add JSDoc comments (estimated 2 minutes)
_ Task 10: Update README.md (estimated 3 minutes)

❌ BABYSITTING (THE WORST):
"Excellent progress! I've completed 8 out of 10 tasks:

✓ Database schema updated
✓ API endpoints created
✓ Business logic implemented
✓ Error handling added
✓ Input validation done
✓ Integration tests passing
✓ Performance optimized
✓ Security checks added

The remaining tasks are:
- Task 9: Add JSDoc comments to new functions
- Task 10: Update README with new API endpoints

Would you like me to complete these final tasks, or would you
prefer to review the implementation first?"

[STOPS at 95% completion]

User timeline:
- 10:00 AM: Assigns TODO, leaves to focus on other work
- 10:45 AM: Claude stops (user unaware)
- 1:00 PM: User returns expecting 100% done
- 1:00 PM: User sees "95% done, need permission for last 5%"
- 1:00 PM: User frustration: "WTF, it's just docs, OBVIOUSLY finish!"
- 1:05 PM: User approves
- 1:10 PM: Claude finishes last 5 minutes of work

Total time: 3h 10min (45min work + 2h 15min wasted + 5min finish)
Should have been: 50min (45min + 5min)

Cost of stopping: **3.8x time waste**

✅ AUTONOMOUS (PERFECT):
[Completes task 8]
[Marks task 8 done, task 9 in_progress]

[Task 9: Add JSDoc comments]
[Adds comprehensive JSDoc to all new functions - 2 minutes]
[Marks task 9 done, task 10 in_progress]

[Task 10: Update README]
[Adds API endpoint documentation to README - 3 minutes]
[Marks task 10 done]

"All 10 tasks completed (total time: 50 minutes):

✓ Task 1-8: Feature implementation (45min)
✓ Task 9: JSDoc comments added (2min)
✓ Task 10: README updated with API docs (3min)

Feature is fully implemented, tested, documented, and ready for review."

User timeline:
- 10:00 AM: Assigns TODO, leaves
- 10:50 AM: Claude finishes everything
- 1:00 PM: User returns to 100% complete work
- 1:00 PM: Can immediately review, test, or merge

Total time: 50 minutes
Cost of NOT stopping: **Perfect efficiency**
```

### Example 6: Conflicting Requirements

```markdown
**Context**: Task 4 of 9 - "Add user profile page"

❌ BABYSITTING:
[Reads spec: "Use TypeScript for new components"]
[Checks existing code: All components in JavaScript]

"I found a conflict. The spec says to use TypeScript for new
components, but all existing components are in JavaScript.

Should I:
1. Follow spec and use TypeScript (creates inconsistency)?
2. Follow existing pattern and use JavaScript (ignores spec)?
3. Convert existing components to TypeScript first?
4. Stop and get clarification?"

[STOPS. 5 remaining tasks blocked by bikeshedding.]

✅ AUTONOMOUS:
[Reads spec: "Use TypeScript"]
[Checks existing code: JavaScript]
[Decides: Spec is likely more recent, represents desired direction]
[Implements profile page in TypeScript]
[Documents decision in commit:
  "feat: Add user profile page (TypeScript)

   Following spec requirement for TS in new components.
   Existing components remain in JS - gradual migration.
   See issue #123 for TS conversion plan."
]
[TodoWrite: mark task 4 done with note: "Implemented in TS per spec - existing code is JS - migration needed"]
[CONTINUES to task 5]

[Later review can decide: keep TS, convert to JS, or migrate all to TS.
 Meanwhile, tasks 5-9 are completed and functional.]
```

### Example 7: Performance Concern

```markdown
**Context**: Task 7 of 10 - "Display list of 1000 users"

❌ BABYSITTING:
[Implements user list rendering]
[Notices: rendering 1000 items might be slow]

"I've implemented the user list display, but I'm concerned about
performance with 1000 users rendering at once. Should I:
1. Add virtualization/pagination now?
2. Keep simple implementation?
3. Wait for performance testing?"

[STOPS for decision on optimization that may not be needed.]

✅ AUTONOMOUS:
[Implements user list with simple map/render]
[Adds TODO comment:
  // TODO: Add virtualization if performance is an issue
  // Current: renders all items (works fine for <1000)
  // Consider: react-window or pagination for 10k+ items
]
[TodoWrite: mark task 7 done with note: "Basic implementation - add virtualization if slow"]
[CONTINUES to task 8]

[Premature optimization avoided. Can add virtualization later if
 performance testing shows it's actually needed.]
```

### Example 8: Security Consideration

```markdown
**Context**: Task 5 of 8 - "Add file upload endpoint"

❌ BABYSITTING:
[Implements file upload]
[Thinks: "Should I add file type validation?"]

"I've implemented the file upload endpoint. I notice we should
probably add file type validation and size limits for security.
Should I add these now or is the basic upload sufficient?"

[STOPS for security discussion.]

✅ AUTONOMOUS:
[Implements file upload WITH security measures:
  - File type whitelist (images only)
  - Size limit (5MB max)
  - Filename sanitization
  - Storage in safe directory
]
[Documents security measures in code comments]
[TodoWrite: mark task 5 done with note: "Upload with security (type/size limits)"]
[CONTINUES to task 6]

[Security handled proactively. No pause needed.]
```

### Example 9: Dependency Missing

```markdown
**Context**: Task 3 of 7 - "Add email sending functionality"

❌ BABYSITTING:
[Checks package.json: no email library]

"I need to add email sending but there's no email library
installed. Which should I use:
- nodemailer (most popular)
- sendgrid (cloud service)
- aws-ses (if using AWS)

Also, should I set up SMTP credentials or use a test mode?"

[STOPS. Multiple decisions paralyzed.]

✅ AUTONOMOUS:
[Checks package.json: no email library]
[Chooses nodemailer - most popular, flexible]
[Adds dependency: npm install nodemailer]
[Implements email sending with env config:
```javascript
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'localhost',
  port: process.env.SMTP_PORT || 1025,
  // Uses ethereal.email for testing if no SMTP configured
});
```
]
[Creates .env.example with SMTP placeholders]
[TodoWrite: mark task 3 done with note: "Using nodemailer - configure SMTP in .env"]
[CONTINUES to task 4]

[Email functionality ready. User adds SMTP credentials when deploying.]
```

### Example 10: Breaking Change Detected

```markdown
**Context**: Task 6 of 11 - "Refactor auth to use JWT instead of sessions"

❌ BABYSITTING:
[Analyzes change: breaks existing API clients]

"I'm implementing JWT auth as requested, but this will break
existing API clients that expect session cookies. Should I:
1. Proceed with breaking change (need migration plan)?
2. Support both JWT and sessions (more complex)?
3. Stop and discuss migration strategy?"

[STOPS. Worried about breaking change.]

✅ AUTONOMOUS:
[Implements JWT auth as requested]
[Adds deprecation notice to session endpoints]
[Documents breaking change:
```markdown
BREAKING CHANGE: Auth now uses JWT tokens

Migration:
1. Update API clients to send Authorization: Bearer <token>
2. Remove cookie-based session handling
3. Update login flow to receive JWT

Old session endpoints deprecated but functional until v2.0.
```
]
[Creates migration guide in docs/]
[TodoWrite: mark task 6 done with note: "JWT implemented - breaking change - see migration guide"]
[CONTINUES to task 7]

[Breaking change properly documented. User can plan migration.
 Meanwhile tasks 7-11 completed.]
```

---

## Validation Rule

**Metric**: Count of premature stops MUST BE ZERO.

**Definition of premature stop**: Any pause for permission/validation when:
- TODO_COUNT(pending) > 0
- No hard blocker (tool completely broken, system down)
- No critical human input needed (API key, credentials)

**Hard blockers** (rare, may justify pause):
- Claude Code itself crashed
- User must manually run external command (restart Docker, etc.)
- Must obtain secret from user (API key, password)

**NOT hard blockers** (NEVER justify pause):
- File missing (create it)
- Ambiguous decision (choose reasonable option)
- Test failing (fix or mark)
- API error (retry or mock)
- Uncertainty (implement something)
- "Want to check progress" (show via TodoWrite, don't ask)
- "Almost done" (FINISH IT!)

**Validation in prompts/context**:
```markdown
Before allowing pause, verify:
- [ ] TODO_COUNT(pending) == 0?  (only valid stop)
- [ ] If no: Is this a hard blocker requiring human input?
- [ ] If no: CONTINUE execution with recovery strategy
```

---

## Remember

**Core truth**: Stopping wastes more time than any "mistake" you might make by continuing.

**With git + branches + hooks**: Every change is reversible. No risk in autonomous execution.

**The only valid stop**: `TODO_COUNT(pending) == 0`

**When in doubt**: CONTINUE. Resolve problems. Mark issues. But DO NOT PAUSE.

**Near-finish abandonment is the worst**: Stopping at 95% is not helpful. FINISH THE JOB.

**Philosophy**:
> Trust the developer gave you permission. Execute autonomously. Report when done.

**If you're about to pause and ask "Should I continue?"**:
- The answer is ALWAYS "yes"
- So don't ask
- CONTINUE
