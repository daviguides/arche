# Arché

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Essential principles for LLM behavior, designed as a Claude Code plugin.

## What is Arché?

**Arché** (ἀρχή) is an ancient Greek word meaning "origin", "first principle", or "foundation". The pre-Socratic philosophers used it to describe the fundamental substance or principle from which everything else derives.

Arché provides the **essential principles** that govern LLM behavior - the foundational axioms that must be loaded before any work begins.

## Philosophy

### The First Principle (ἀρχή)

Just as the Greek philosophers sought the arché of the universe - the fundamental principle underlying all things - this plugin defines the arché of LLM behavior: the inviolable principles that shape how Claude Code operates.

> *"The arché is that from which all things come to be, and into which they are finally resolved."*
> — Aristotle, on the pre-Socratics

### The Four Essential Principles

| Principle | Greek Virtue | Purpose |
|-----------|--------------|---------|
| **Anti-Duplication** | Aletheia (truth) | Single source of truth; reference, don't repeat |
| **Anti-Babysitting** | Autarkeia (self-sufficiency) | Execute to completion; never stop mid-task |
| **LLM Conciseness** | Sophrosyne (moderation) | Maximum signal, minimum noise |
| **Principle Enforcement** | Nomos (law) | Mandatory gates; research before action |

### Hierarchy of Principles

```
┌─────────────────────────────────────────┐
│ 1. Principle Enforcement (Meta)         │  ← Governs all others
├─────────────────────────────────────────┤
│ 2. Anti-Duplication                     │  ← Highest priority
├─────────────────────────────────────────┤
│ 3. Anti-Precocity*                      │  ← Respect user's mode
├─────────────────────────────────────────┤
│ 4. Anti-Babysitting                     │  ← Autonomous execution
├─────────────────────────────────────────┤
│ 5. LLM Conciseness                      │  ← Token economy
└─────────────────────────────────────────┘

* Anti-Precocity optional modes → migrated to Dao plugin
```

## Relationship with Other Plugins

Arche is the foundation upon which other plugins build:

| Plugin | Philosophy | Depends on Arché |
|--------|------------|------------------|
| **arche** | Greek (ἀρχή) | — (is the foundation) |
| **code-zen** | Zen Buddhism | Uses conciseness, anti-duplication |
| **dao** | Taoism (道) | Uses anti-babysitting, adds workflow extensions |
| **gradient** | Architecture | Uses all principles for plugin creation |

```
        ┌─────────┐
        │  arche  │  ← Essential principles (load first)
        └────┬────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
┌───────┐ ┌─────┐ ┌──────────┐
│code-zen│ │ dao │ │ gradient │
└───────┘ └─────┘ └──────────┘
```

## Principles

### Anti-Duplication

**Single Source of Truth (SSOT)**: Every piece of information exists in exactly one authoritative location.

- Reference, don't repeat
- If it exists, extend it
- No "Related" sections (load workflows handle connections)

### Anti-Babysitting

**Execute to completion**: Once in IMPLEMENTING mode with a TODO list, never stop until `TODO_COUNT(pending) == 0`.

- No premature check-ins
- No mid-execution validation requests
- Mark issues, don't stop for them

### LLM Conciseness

**Maximum signal, minimum noise**: Every token must carry semantic value.

- Eliminate filler words
- Active voice, imperative mood
- Code > prose; show, don't tell

### Principle Enforcement

**Research before implementation**: Mandatory gates before any action.

- Load principles before working
- Search codebase before creating
- Detect user's mode before responding

## Project Structure

```
arche/
├── spec/                    # Normative specifications
│   └── principles/          # The four essential principles
├── context/                 # Applied examples
│   └── guides/              # How to apply principles
├── prompts/                 # Workflow orchestrators
│   └── load.md              # Load all principles
├── commands/                # User-facing commands
└── agents/                  # Specialized agents
```

## Installation

*Coming soon*

```bash
# Future one-line installation
sh -c "$(curl -fsSL https://raw.githubusercontent.com/daviguides/arche/main/install.sh)"
```

## Usage

*Coming soon*

```bash
/arche:load                  # Load all essential principles
/arche:validate              # Check compliance with principles
```

## Status

🚧 **In Development** - Extracting from gradient plugin.

## License

MIT License

## Author

Essential principles for Claude Code behavior.

---

> *"Know the first principle, and all else follows."*
> — Ancient Greek wisdom
