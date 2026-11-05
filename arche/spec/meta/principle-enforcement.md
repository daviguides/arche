# Principle Enforcement (Meta-Principle)

**DOGMATIC RULE**: This meta-principle governs HOW to apply all other principles.


## Core Rule: Research Before Implementation

```
BEFORE accepting ANY implementation task:
1. READ task requirements completely
2. RESEARCH codebase using Glob/Grep/Read
3. VALIDATE against loaded principles
         ↓ ONLY IF ALL COMPLETE
THEN proceed with implementation
```

**VIOLATION = HALT. Record the blocker and escalate through the entry's channel.**


## DOGMATIC RULE: @ References Are Mandatory Reads

**Every `@` reference encountered in a file MUST be read using the Read tool.**

`@` is NOT a "see also". It is NOT optional context. It is a **mandatory read directive**.

```
When reading a file and encountering @path/to/file.md:
1. STOP processing current file
2. READ the referenced file
3. RESUME processing current file with referenced context loaded
```

**VIOLATION**: Using inline information from a file while ignoring its `@` references. The referenced file is the **authoritative source** — inline summaries exist only as navigation aids, never as substitutes.

❌ Read resume-protocol.md → see `cd .worktrees/<task>` → execute → ignore `@../worktree/worktree-spec.md`
✅ Read resume-protocol.md → see `@../worktree/worktree-spec.md` → READ worktree-spec.md → use authoritative commands from spec


## HALT Conditions

### ⛔ 1: @ Reference Not Read
- **Trigger**: Encountered `@path/to/file.md` in any loaded file
- **Check**: Was the referenced file read with Read tool?
- **If NO**: HALT → Read the referenced file before continuing

### ⛔ 2: Codebase Not Researched
- **Trigger**: About to create files
- **Check**: Used Glob/Grep/Read?
- **If NO**: HALT → Research existing implementations first

### ⛔ 3: Duplication Detected
- **Trigger**: Research reveals existing implementation
- **Check**: Similar code/feature exists?
- **If YES**: HALT → Report, suggest extend/refactor


## Mandatory Checkpoints

### Checkpoint 1: Pre-Task Research

**BEFORE creating ANY file**:
```bash
glob "**/*{keyword}*"           # Find relevant files
grep "{concept}" --output_mode=files_with_matches
read {discovered-file-path}     # Understand existing code
```

❌ "Create auth module" → immediately creates auth.py
✅ "Create auth module" → searches first, finds existing, decides how to proceed

### Checkpoint 2: Anti-Duplication Gate

If similar code exists → decide and record:
```
Found existing: {path}
Options: A) Extend  B) Refactor  C) Justify new
```

### Checkpoint 3: Anti-Babysitting

Once executing with a TODO list:
```python
while TODO_COUNT(pending) > 0:
    execute_next_task()
    # NO permission checks, NO pauses
report_all_completed()
```

### Checkpoint 4: Correction-Integration

When a correction arrives, the old pattern is overridden — as an absolute constraint, carried into every subsequent action:
```
Correction received → restate as hard constraint (not a preference)
                    → enforce in this step AND all following steps
```

❌ "MLX preferred but torch acceptable" (after the requirement demanded MLX)
✅ "MLX is required; report the exact blocker if impossible; no fallback"

### Checkpoint 5: Completion Integrity

Before reporting DONE:
```
Deliverable == the ORIGINAL requirement?   (not a silent downgrade)
Backed by evidence?                        (not "it works")
If blocked → the blocker IS the deliverable (not a lesser substitute)
```

❌ "shipped CPU-only, CoreML is future work"
✅ "CoreML flips 5% of verdicts (evidence); CPU shipped as the working path, CoreML blocked WITH evidence"

### Checkpoint 6: Anti-Timidity

At the recommendation/allocation stage, BEFORE a task is chosen:
```
Ask "how would we do the high-value thing" BEFORE "why not"
Judge worth by VALUE, never by effort-cost
Existing patterns and prior choices = re-examinable, not fixed
"expensive/premature/risky" → pair with "vs what, and how to engineer around it"
Allocate effort by value, not by what is safe to be right about
```

❌ "Learned routing is expensive; the roadmap gates it — but you decide."
✅ "It's a lightweight model, cheap in money and latency; the only prerequisite is the query-log data. Here is the plan."


## Priority Order

When principles conflict:
1. **principle-enforcement** (this file)
2. **correction-integration**
3. **anti-duplication**
4. **anti-precocity**
5. **anti-timidity**
6. **anti-complacency**
7. **anti-babysitting**
8. **llm-conciseness**


## Validation

**Pre-response checklist:**
- [ ] All `@` references read?
- [ ] Research done?
- [ ] Duplication checked?
- [ ] Response aligned with current mode boundaries?


## Remember

> These are gates, not guidelines. Enforcement is not optional.

**ALWAYS**: Research → Check duplication → Stay in mode → Complete without babysitting.
