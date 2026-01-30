# Next Steps: Arche Plugin Setup

**Status**: Architectural decisions documented
**Next Session**: Extract and split principles from gradient

---

## Architectural Decisions

See `design/decisions.md` for full rationale.

**Key Decisions**:
1. Arché = behavioral principles (not plugin foundation)
2. Anti-Precocity splits into 2 files
3. Essential cognitive modes stay in Arché (Dao extends them)

---

## TODO

### 1. Create folder structure

```bash
mkdir -p arche/spec/{behavior,knowledge,meta,modes}
mkdir -p arche/{context/guides,prompts,commands,agents,.claude-plugin}
```

Target structure (Option C - by category):
```
arche/
├── .claude-plugin/
│   └── plugin.json               ✅
├── arche/                        ← BUNDLE
│   ├── spec/
│   │   ├── behavior/             # How LLM should act
│   │   │   ├── anti-babysitting.md    ✅
│   │   │   ├── anti-precocity.md      ✅ (principle only)
│   │   │   └── llm-conciseness.md     ✅
│   │   ├── knowledge/            # How to handle information
│   │   │   └── anti-duplication.md    ✅
│   │   ├── meta/                 # Governs other principles
│   │   │   └── principle-enforcement.md ✅
│   │   └── modes/                # Cognitive modes
│   │       └── essential-cognitive-modes.md ✅
│   ├── context/
│   │   └── guides/               (placeholder)
│   └── prompts/
│       └── load-essential.md     ✅
├── commands/
│   └── load-essential.md         ✅
├── design/
│   └── decisions.md              ✅
└── agents/                       (future)
```

**Size constraint**: Total must stay ≤104KB (current size)

### 2. Extract principles from gradient

| Source (gradient) | Destination (arche) | Notes |
|-------------------|---------------------|-------|
| `anti-babysitting.md` | `spec/behavior/` | Direct copy (24K) |
| `anti-precocity.md` | `spec/behavior/anti-precocity.md` | **SPLIT**: Principle only (~12K) |
| `anti-precocity.md` | `spec/modes/essential-cognitive-modes.md` | **SPLIT**: 4 modes (~13K) |
| `llm-conciseness.md` | `spec/behavior/` | Direct copy (16K) |
| `anti-duplication.md` | `spec/knowledge/` | Direct copy (12K) |
| `principle-enforcement.md` | `spec/meta/` | Direct copy (15K) |

**Goes to Dao** (not Arché):
- Optional modes (DEBUGGING, REVIEWING, LEARNING, DECIDING)
- Advanced workflows

### 3. Create plugin.json

```json
{
  "name": "arche",
  "version": "0.1.0",
  "description": "Essential behavioral principles for Claude Code"
}
```

### 4. Create user-facing commands

| Command | Purpose |
|---------|---------|
| `/arche:load-essential` | Load all essential principles |
| `/arche:validate` | Check compliance with principles |

### 5. Update gradient plugin

After extraction:
- Remove `universal-principles/` from gradient
- Add note about arche dependency in gradient docs
- Update `/gradient:load-essential` to delegate to `/arche:load-essential`

---

## Anti-Precocity Split Details

### File 1: `anti-precocity.md` (Principle)

Content to include:
- Core Philosophy / Fundamental Problem
- Central Principle: "Mode transitions must be explicitly triggered"
- 4 Dogmatic Rules (RULE 1-4)
- 7 Anti-Patterns (Deadly Precocities)
- Detection Methods / Red Flags
- Self-Assessment Questions
- Validation Checklist

### File 2: `essential-cognitive-modes.md` (Flow)

Content to include:
- The 4 Principal Modes (EXPLORING, RESEARCHING, PLANNING, IMPLEMENTING)
- Each mode's definition, signals, appropriate response, examples
- Signal vocabulary (Appendix from original)
- Transition signals
- Anti-Precocity vs Anti-Babysitting zones diagram
- Mode boundaries (what's allowed/forbidden per mode)

---

## Migration Plan

```
BEFORE (gradient):
gradient/spec/universal-principles/
├── anti-duplication.md         (12K)
├── anti-babysitting.md         (24K)
├── anti-precocity.md           (25K) ← mixed content
├── llm-conciseness.md          (16K)
└── principle-enforcement.md    (15K)
                         TOTAL: 104K

AFTER (arche + dao):
arche/spec/
├── behavior/
│   ├── anti-babysitting.md     (24K)
│   ├── anti-precocity.md       (~12K) ← principle only
│   └── llm-conciseness.md      (16K)
├── knowledge/
│   └── anti-duplication.md     (12K)
├── meta/
│   └── principle-enforcement.md (15K)
└── modes/
    └── essential-cognitive-modes.md (~13K) ← from anti-precocity
                         TARGET: ≤104K

dao/spec/workflows/
├── optional-modes.md           ← DEBUGGING, REVIEWING, etc.
└── [other workflows]
```

---

## Reference

- Gradient plugin: `/Users/daviguides/work/sources/gradients/gradient/`
- Source principles: `gradient/gradient/spec/universal-principles/`
- Decisions: `arche/design/decisions.md`
