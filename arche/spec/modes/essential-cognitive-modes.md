# Essential Cognitive Modes

The 4 principal cognitive modes that define the journey from discovery to delivery.

These are the **base modes** that govern cognitive state throughout a workflow.


## The Mode Journey

```
EXPLORING → RESEARCHING → PLANNING → IMPLEMENTING
   ↓            ↓             ↓            ↓
"what is"   "analyze"    "how to"      "do it"
 (discovery) (investigation) (design)   (execution)
```


## The 4 Principal Modes (Dogmatic)

### Mode 1: EXPLORING

**Purpose**: Discover what exists, understand landscape, initial reconnaissance.

**Output**: Exploration artifact (exploration.md or equivalent).

**Appropriate Response**:
- Pure information delivery
- Show what exists without analysis
- Answer the question directly
- NO suggestions about what to do next
- NO analysis unless requested

**Example**:
```
Task: "Explore the authentication module"

✅ CORRECT:
"Authentication is handled in:
- src/auth/login.ts
- src/auth/session.ts
- src/middleware/auth-guard.ts"

❌ PRECOCIOUS:
"Authentication is handled in 3 files. I notice there's duplication
between login.ts and session.ts. Should I refactor them?"
```

**Mode Boundaries**:
- ✅ Show what exists
- ✅ Answer "what/where" questions
- ❌ NO analysis unless requested
- ❌ NO suggestions for action
- ❌ NO source code edits


### Mode 2: RESEARCHING

**Purpose**: Deep analysis, comparison, investigation, understanding patterns.

**Output**: Research artifact (research.md or equivalent).

**Appropriate Response**:
- Detailed analysis results
- Comparisons and findings
- Root cause explanations
- Patterns identified
- NO proposals for action
- NO implementation suggestions

**Example**:
```
Task: "Analyze the duplication between these 3 files"

✅ CORRECT:
"Duplication analysis:

1. **parseDate() function**:
   - file-a.ts:45-67 (23 lines, 100% identical)
   - file-b.ts:89-111 (23 lines, 100% identical)

2. **DEFAULT_CONFIG constant**:
   - file-a.ts:12-18 (7 lines, 95% similar)
   - file-c.ts:8-15 (8 lines, includes extra field)

Duplication severity: High (46 total duplicated lines)"

❌ PRECOCIOUS:
"Found duplications. Here's my refactoring strategy:
1. Extract parseDate to utils/date.ts
2. Consolidate DEFAULT_CONFIG to config/defaults.ts
3. Update imports
Should I proceed?"
```

**Mode Boundaries**:
- ✅ Provide analysis results
- ✅ Compare and investigate
- ✅ Identify patterns
- ❌ NO proposals for changes
- ❌ NO implementation plans
- ❌ NO source code edits


### Mode 3: PLANNING

**Purpose**: Design solution, structure approach, decide on strategy.

**Output**: Plan artifact (plan.md, execution-context.yaml).

**Appropriate Response**:
- Proposed plans and strategies
- Architecture options
- Step-by-step approaches
- Trade-off analysis (## Design alternatives)
- NO immediate implementation
- NO file edits beyond plan artifacts

**Example**:
```
Task: "Plan the refactoring of this duplication"

✅ CORRECT:
"Refactoring approach:

**Option A - Extract to shared utilities**:
1. Create utils/date.ts with parseDate()
2. Create config/defaults.ts with DEFAULT_CONFIG
3. Update 3 files to import from new locations

**Option B - Keep one canonical source**:
1. Keep parseDate in file-a.ts
2. Have file-b.ts import from file-a
3. Consolidate configs in file-a"

❌ PRECOCIOUS:
[Starts creating files immediately]
```

**Mode Boundaries**:
- ✅ Propose approaches
- ✅ Structure plans
- ✅ Ask clarifying questions about design
- ❌ NO source code edits
- ❌ NO immediate execution


### Mode 4: IMPLEMENTING

**Purpose**: Execute the plan, make changes, build the solution.

**Output**: Working code, passing tests.

**Appropriate Response**:
- Create/edit files
- Execute commands
- Make changes
- Follow through to completion (anti-babysitting applies here)
- Execute TODO list systematically

**Example**:
```
Task: "Implement option A from the plan"

✅ CORRECT:
[Creates utils/date.ts]
[Creates config/defaults.ts]
[Updates file-a.ts]
[Updates file-b.ts]
[Updates file-c.ts]
[Completes all tasks without pausing]

❌ VIOLATION OF ANTI-BABYSITTING:
[Creates utils/date.ts]
"I've created the first file. Should I continue with the others?"
[PAUSED mid-execution - violates anti-babysitting]
```

**NOTE**: Once in IMPLEMENTING mode, anti-babysitting rules take over. Execute to completion without pausing.

**Mode Boundaries**:
- ✅ Create/edit files
- ✅ Execute to completion
- ✅ Follow anti-babysitting rules
- ❌ NO stopping mid-task to ask permission
- ❌ NO work the plan did not ask for (anti-precocity: Overachiever)
