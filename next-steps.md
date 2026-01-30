# Arché - Next Steps

**Status**: Core implementation complete

---

## Pending Actions

### 1. Update gradient delegation

**File**: `gradient/commands/load-essential.md`

- [ ] Update `/gradient:load-essential` to delegate to `/arche:load-essential`

### 2. Remove legacy specs from gradient

**Remove**: `gradient/gradient/spec/universal-principles/`

```
├── anti-duplication.md      → now in arche
├── anti-babysitting.md      → now in arche
├── anti-precocity.md        → now in arche (split)
├── llm-conciseness.md       → now in arche
└── principle-enforcement.md → now in arche
```

**Rationale**: Arché is now the SSOT for these principles

---

## Completed

- [x] Folder structure (bundle pattern)
- [x] 6 specs (behavior/, knowledge/, meta/, modes/)
- [x] prompts/load-essential.md
- [x] commands/load-essential.md
- [x] plugin.json
- [x] install.sh
- [x] CLAUDE.md
- [x] design/decisions.md

---

## Reference

- Decisions: `design/decisions.md`
- Size: 100KB (within 104KB limit)
