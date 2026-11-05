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
│   │   ├── behavior/         # How LLM should act (core, shared by all entries)
│   │   ├── knowledge/        # How to handle information (anti-duplication, spec-authoring)
│   │   ├── meta/             # Governs other principles (principle-enforcement)
│   │   ├── modes/            # Essential cognitive modes (mode definitions and limits)
│   │   ├── interactive/      # User-in-the-loop: mode detection by signal, fork audit
│   │   └── runner/           # Runner overlays: autonomous (authors), reviewer
│   ├── context/
│   │   ├── guides/           # Practical compliance procedures
│   │   └── examples/         # Few-shot examples
│   └── prompts/              # load, load-autonomous, load-reviewer
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

### Entries

Three entries, each composing from the same specs with a different
overlay. Each spec is written once; entries only choose what to import.

| Entry | Purpose | Overlay | chars | ~tokens |
|-------|---------|---------|------:|--------:|
| `load` (interactive) | Sessions with a human | `spec/interactive/` + `interactive-verification` | 41,784 | ~11.6k |
| `load-autonomous` | Runner author sessions (G1 discovery, G3 implementing) | `spec/runner/autonomous` | 38,936 | ~10.8k |
| `load-reviewer` | Runner reviewer sessions (G2 plan_review, G4 validate) | `spec/runner/reviewer` | 15,705 | ~4.4k |

Measured with `compile_plugin("arche", prompt=<entry>, strict=True)`
from the dev layout (`GRADIENT_PLUGIN_PATH` pointing to the plugin root).

**Spec with a runner variant**: each spec in `spec/behavior/`, `spec/meta/`,
`spec/knowledge/` and `spec/modes/` is neutralized (no user-as-interlocutor,
no git, no forks). The interactive and runner overlays add the context-specific
escalation channel. When editing a core spec, verify the compiled output of
all 3 entries.

**Release order for YAML changes**: the arche release and `install.sh` MUST
land before any workflow YAML that references a new entry. A YAML pointing
to an entry that does not exist in the installed bundle causes `PluginError`
and stops every task at that mode.

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
