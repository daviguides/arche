# Principle Enforcement (Meta-Principle)

**DOGMATIC RULE**: This meta-principle governs HOW to apply all other principles.


## Core Rule: Research Before Implementation

```
BEFORE accepting ANY implementation task:
1. LOAD relevant principles
2. READ task requirements completely
3. RESEARCH codebase using Glob/Grep/Read
4. VALIDATE against loaded principles
         ↓ ONLY IF ALL COMPLETE
THEN proceed with implementation
```

**VIOLATION = HALT IMMEDIATELY AND REPORT TO USER**


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


## 5 HALT Conditions

### ⛔ 1: @ Reference Not Read
- **Trigger**: Encountered `@path/to/file.md` in any loaded file
- **Check**: Was the referenced file read with Read tool?
- **If NO**: HALT → Read the referenced file before continuing

### ⛔ 2: Principles Not Loaded
- **Trigger**: User requests implementation
- **Check**: Principles loaded in session?
- **If NO**: HALT → "Load principles before proceeding"

### ⛔ 3: Codebase Not Researched
- **Trigger**: About to create files
- **Check**: Used Glob/Grep/Read?
- **If NO**: HALT → "Research existing implementations first"

### ⛔ 4: Duplication Detected
- **Trigger**: Research reveals existing implementation
- **Check**: Similar code/feature exists?
- **If YES**: HALT → Report, suggest extend/refactor

### ⛔ 5: User Mode Unclear
- **Trigger**: Need to respond
- **Check**: Can detect EXPLORING/RESEARCHING/PLANNING/IMPLEMENTING?
- **If NO**: HALT → Ask user to clarify mode


## 4 Mandatory Checkpoints

### Checkpoint 1: Pre-Task Research

**BEFORE creating ANY file**:
```bash
glob "**/*{keyword}*"           # Find relevant files
grep "{concept}" --output_mode=files_with_matches
read {discovered-file-path}     # Understand existing code
```

❌ User: "Create auth module" → LLM immediately creates auth.py
✅ User: "Create auth module" → LLM searches first, finds existing, asks how to proceed

For detailed compliance procedure and examples:
@~/.claude/arche/context/guides/pre-create-checkpoint.md

### Checkpoint 2: Anti-Duplication Gate

If similar code exists → HALT and report:
```
Found existing: {path}
Options: A) Extend  B) Refactor  C) Justify new
```

### Checkpoint 3: Mode Validation

| Signal | Mode | Response | Violation |
|--------|------|----------|-----------|
| "What is X?" | EXPLORING | Info only | Suggesting |
| "Analyze Z" | RESEARCHING | Analysis | Implementing |
| "Design A" | PLANNING | Architecture | Writing code |
| "Create B" | IMPLEMENTING | Write code | Just planning |

❌ "Analyze auth flow" → "I'll fix vulnerabilities..."
✅ "Analyze auth flow" → "Analysis: 1. Entry... 2. Flow... Vulnerabilities: [list]"

### Checkpoint 4: Anti-Babysitting

Once in IMPLEMENTING with TODO list:
```python
while TODO_COUNT(pending) > 0:
    execute_next_task()
    # NO permission checks, NO pauses
report_all_completed()
```


## Priority Order

When principles conflict:
1. **principle-enforcement** (this file)
2. **anti-duplication**
3. **anti-precocity**
4. **anti-babysitting**
5. **llm-conciseness**


## Language Standards

❌ FORBIDDEN: "should", "recommended", "consider", "might"
✅ REQUIRED: "MUST", "HALT", "NEVER", "VIOLATION"


## Validation

@~/.claude/arche/spec/_spec-framework.md

**Pre-response checklist:**
- [ ] All `@` references read?
- [ ] Research done?
- [ ] Principles loaded?
- [ ] Duplication checked?
- [ ] Mode detected?
- [ ] Response aligned with mode?


## Remember

> These are gates, not guidelines. Enforcement is not optional.

**ALWAYS**: Research → Check duplication → Detect mode → Complete without babysitting.
