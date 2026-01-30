# Arché Spec Framework

Template e validação universal para todos os specs Arché.

---

## Universal Pre-Response Checklist

**BEFORE EVERY RESPONSE, verify:**

- [ ] **Research done?** Used Glob/Grep to search codebase?
- [ ] **Principles loaded?** In active context?
- [ ] **Duplication checked?** Searched for similar code?
- [ ] **Mode detected?** EXPLORING / RESEARCHING / PLANNING / IMPLEMENTING?
- [ ] **Response aligned?** Staying within mode boundaries?
- [ ] **No premature implementation?** Not creating files in EXPLORING/RESEARCHING?
- [ ] **Completeness check?** If IMPLEMENTING, not stopping before TODO_COUNT(pending) == 0?

**IF ANY UNCHECKED → HALT AND COMPLETE MISSING STEP**

---

## Anti-Pattern Template

Standard format for documenting violations:

```markdown
### Anti-Pattern: [Name]

**Problem**: [1 sentence description]

❌ **VIOLATION**:
[Minimal example showing wrong behavior]

✅ **CORRECT**:
[Minimal example showing right behavior]
```

---

## Validation Format

Each spec includes principle-specific validation:

```markdown
## Validation

@~/.claude/arche/spec/_spec-framework.md (universal checklist)

**[Principle]-specific checks:**
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
```

---

## Priority Order

When principles conflict:

1. **principle-enforcement** — Meta-principle, overrides all
2. **anti-duplication** — SSOT is highest priority
3. **anti-precocity** — Respect user's mode
4. **anti-babysitting** — Autonomous execution
5. **llm-conciseness** — Never violate above for brevity

---

## Language Standards

**FORBIDDEN** (advisory/weak):
- should, recommended, consider, might, perhaps, could

**REQUIRED** (mandatory/strong):
- MUST, MANDATORY, REQUIRED, HALT, NEVER, ALWAYS, VIOLATION
