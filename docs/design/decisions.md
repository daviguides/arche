# Arché - Architectural Decisions

Decisions made during plugin design.

---

## Decision 1: What is Arché?

**Date**: 2026-01-29

**Context**: Clarifying the purpose of the plugin.

**Decision**: Arché is NOT a technical foundation for other plugins. It is a **set of essential behavioral principles** that modify Claude Code behavior for a better user experience.

**Rationale**:
- These principles have been validated by the author and others
- They are loaded ALWAYS, in ANY session, for ANY type of work
- They govern LLM behavior, not plugin architecture

---

## Decision 2: Anti-Precocity Split

**Date**: 2026-01-29

**Context**: The original `anti-precocity.md` (921 lines) contains both behavioral principles AND cognitive flow definitions.

**Decision**: Split into 2 files within Arché:

| File | Content | Purpose |
|------|---------|---------|
| `anti-precocity.md` | The PRINCIPLE | Don't jump modes without explicit signal |
| `essential-cognitive-modes.md` | The ESSENTIAL FLOW | The 4 base modes that can be extended |

**Content Distribution**:

### Goes to `anti-precocity.md`:
- Core principle: "Mode transitions must be explicitly triggered by the user"
- 4 Dogmatic rules (MODE DETECTION, STAY IN MODE, EXPLICIT SIGNALS, ZERO PROACTIVE)
- 7 Anti-patterns (Deadly Precocities)
- Detection methods / Red flags
- Self-assessment questions

### Goes to `essential-cognitive-modes.md`:
- 4 Principal modes definitions (EXPLORING, RESEARCHING, PLANNING, IMPLEMENTING)
- Signal vocabulary for each mode
- Transition signals
- Anti-Precocity vs Anti-Babysitting zones diagram
- Mode boundaries (what's allowed/forbidden in each)

**Rationale**:
- Separation of concerns: principle vs flow
- Both are essential (always loaded)
- "Essential" naming indicates these are BASE modes that Tao can extend/modify

---

## Decision 3: Relationship with Dao

**Date**: 2026-01-29

**Context**: What goes to Dao vs Arché regarding cognitive modes.

**Decision**:

```
ARCHÉ (base, always loads)
└── essential-cognitive-modes.md  ← The 4 base modes

DAO (extends/modifies)
├── optional-modes.md             ← DEBUGGING, REVIEWING, LEARNING, DECIDING
└── [other workflows]             ← Custom flows, variations
```

**Rationale**:
- Essential modes are so fundamental they must load in every session
- Dao workflows can extend or modify the base modes
- Maintains extensibility without duplicating core definitions

---

## Decision 4: Arché Principles Hierarchy

**Date**: 2026-01-29

**Context**: Establishing the order/priority of principles.

**Decision**: From README.md hierarchy:

```
1. Principle Enforcement (Meta)     ← Governs all others
2. Anti-Duplication                 ← Highest priority
3. Anti-Precocity                   ← Respect user's mode
4. Anti-Babysitting                 ← Autonomous execution
5. LLM Conciseness                  ← Token economy
```

Plus:
- `essential-cognitive-modes.md` as companion to Anti-Precocity

**Rationale**:
- Meta-principle must come first
- Anti-Duplication prevents waste
- Anti-Precocity respects user flow
- Anti-Babysitting enables completion
- Conciseness optimizes output

---

## Open Questions

### Q1: File naming consistency
Should all principle files follow same pattern?
- `anti-duplication.md`
- `anti-babysitting.md`
- `anti-precocity.md`
- `llm-conciseness.md` (not "anti-")
- `principle-enforcement.md` (not "anti-")

### Q2: Essential modes location
Should `essential-cognitive-modes.md` be in `spec/principles/` or separate folder like `spec/modes/`?

---

## Decision 5: Folder Structure (Option C)

**Date**: 2026-01-29

**Context**: How to organize spec files in Arché.

**Decision**: Option C - Organize by conceptual category:

```
arche/
├── spec/
│   ├── behavior/              # How LLM should act
│   │   ├── anti-babysitting.md
│   │   ├── anti-precocity.md
│   │   └── llm-conciseness.md
│   ├── knowledge/             # How to handle information
│   │   └── anti-duplication.md
│   ├── meta/                  # Governs other principles
│   │   └── principle-enforcement.md
│   └── modes/                 # Cognitive modes
│       └── essential-cognitive-modes.md
├── context/
│   └── guides/
├── prompts/
└── commands/
```

**Rationale**:
- Groups principles by their nature
- Clear semantic separation
- Modes separate from principles (Dao extends modes, not principles)

---

## Decision 6: Content Size Monitoring

**Date**: 2026-01-29

**Context**: Original files total 104KB.

| File | Size |
|------|------|
| anti-precocity.md | 25K |
| anti-babysitting.md | 24K |
| llm-conciseness.md | 16K |
| principle-enforcement.md | 15K |
| anti-duplication.md | 12K |
| **TOTAL** | **104K** |

**Decision**:
- Do NOT increase size with current modifications
- Size reduction is a future task, not current scope
- Monitor total size after extraction

---

## References

- Source files: `gradient/gradient/spec/universal-principles/`
- Arché README: `/Users/daviguides/work/sources/gradients/arche/README.md`
- Arché next-steps: `/Users/daviguides/work/sources/gradients/arche/next-steps.md`
