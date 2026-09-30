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

**Documentation**: `docs/` folder is at `./../gradients-docs/arche-docs`

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

- **Gradient**: Uses Arché principles for plugin architecture
- **Zazen**: Zen principles for code clarity (uses conciseness, anti-duplication)
- **Shodo**: Python standards for elegant code (uses conciseness)

---

## Development Notes

- **Size constraint**: Keep total ≤100KB
- **Philosophy**: Essential only - no bloat
- **Bundle pattern**: All specs inside `arche/arche/`

---

## Releasing — mandatory workflow

Every plugin modification MUST follow this sequence. No exceptions.

### 1. Bump version

Patch for fixes/tweaks, minor for new skills or behavioral changes:

```bash
# From gradients/arche/
# Edit .claude-plugin/plugin.json version field
# Also update install.sh header if it shows a version
```

### 2. Commit and push

```bash
git add -A && git commit -m "bump: vX.Y.Z — <what changed>"
git tag -a vX.Y.Z -m "<what changed>"
git push && git push origin vX.Y.Z
```

### 3. Run install.sh

```bash
~/work/sources/continuum/gradients/arche/install.sh
```

Note: install.sh clones from the GitHub remote (not local source), so
the push in step 2 must land before running it.

### 4. Verify cache is not stale

The plugin cache (`~/.claude/plugins/cache/daviguides/arche/`) is
unstable — even after a successful install, it can preserve stale
state from previous versions. This is a known unresolved bug in the
Claude Code plugin system.

After install, always verify:

```bash
# Compare installed vs source timestamps
diff <(ls -lR ~/.claude/arche/spec/) <(ls -lR arche/spec/)

# Check cache version matches
ls ~/.claude/plugins/cache/daviguides/arche/

# If stale, nuke cache and reinstall
rm -rf ~/.claude/plugins/cache/daviguides/arche/
rm -rf ~/.claude/arche/
./install.sh
```

Do NOT move to the next task with a stale cache — the session will
load outdated skills silently.
