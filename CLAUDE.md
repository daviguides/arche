# Arché - Claude Code Project Instructions

## Project Overview

**Arché** (ἀρχή) provides essential behavioral principles for Claude Code.

**Purpose**: Plugin that modifies LLM behavior for better user experience. Unlike Gradient (plugin foundation), Arché focuses on behavioral configuration.

---

## Structure

```
arche/
├── arche/                    ← BUNDLE
│   ├── spec/
│   │   ├── behavior/         # How LLM should act
│   │   ├── knowledge/        # How to handle information
│   │   ├── meta/             # Governs other principles
│   │   └── modes/            # Essential cognitive modes
│   ├── context/
│   │   ├── guides/           # Practical compliance procedures
│   │   └── examples/         # Few-shot examples
│   └── prompts/
├── commands/
└── design/
```

---

## The 5 Essential Principles

| # | Principle | Location | Purpose |
|---|-----------|----------|---------|
| 1 | Principle Enforcement | `spec/meta/` | Research before action |
| 2 | Anti-Duplication | `spec/knowledge/` | SSOT; reference, don't repeat |
| 3 | Anti-Precocity | `spec/behavior/` | Respect user's cognitive mode |
| 4 | Anti-Babysitting | `spec/behavior/` | Execute to completion |
| 5 | LLM Conciseness | `spec/behavior/` | Maximum signal, minimum noise |

Plus: `essential-cognitive-modes.md` in `spec/modes/`

---

## Hierarchy

```
1. Principle Enforcement (Meta)     ← Governs all others
2. Anti-Duplication                 ← Highest priority
3. Anti-Precocity                   ← Respect user's mode
4. Anti-Babysitting                 ← Autonomous execution
5. LLM Conciseness                  ← Token economy
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/arche:load` | Load all essential principles |

---

## Relationship with Other Plugins

- **Dao**: Extends essential-cognitive-modes with optional modes and workflows
- **Gradient**: Uses Arché principles for plugin architecture
- **Code-Zen**: Uses conciseness, anti-duplication principles

---

## Development Notes

- **Size constraint**: Keep total ≤100KB
- **Philosophy**: Essential only - no bloat
- **Bundle pattern**: All specs inside `arche/arche/`

---

## Releasing

When creating a new version:

1. Update `.claude-plugin/plugin.json` version field
2. Commit the version bump
3. Create annotated tag: `git tag -a vX.Y.Z -m "message"`
4. Push with tag: `git push && git push origin vX.Y.Z`
