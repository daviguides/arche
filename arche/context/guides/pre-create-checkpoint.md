# Pre-Create Checkpoint Guide

For the rule this implements: @~/.claude/arche/spec/meta/principle-enforcement.md

---

## Compliance Procedure

**BEFORE creating ANY file, STOP and execute:**

```bash
glob "**/*{keyword}*"                              # Step 1: Find similar files
grep "{concept}" --output_mode=files_with_matches  # Step 2: Search existing code
read {discovered-file}                             # Step 3: Understand what exists
```

**If similar code/feature exists** → HALT and report:
```
Found existing: {path}
Options: A) Extend existing  B) Refactor existing  C) Justify why new is needed
```

**Only proceed to create** if search returned no relevant results.

---

## Violation vs Compliance

```
User: "Create email validator"

❌ VIOLATION:
   [Immediately creates src/validators.py with validate_email()]

✅ COMPLIANCE:
   1. glob "**/*valid*" → finds utils.py, models.py
   2. grep "email" --output_mode=files_with_matches → finds matches
   3. read utils.py → sees validate_email() at line 41
   4. HALT: "Found existing validate_email in utils.py:41.
            Options: A) Extend  B) Refactor  C) Justify new"
   5. Wait for user decision before proceeding
```

---

## Common Triggers

Apply this checkpoint when user says:
- "Create...", "Add...", "Build..."
- "Make a new...", "Implement..."
- Any request that would result in new file creation

---

## Remember

> The cost of searching is seconds. The cost of duplication is maintenance forever.

**ALWAYS search first. Creating without research is a VIOLATION.**
