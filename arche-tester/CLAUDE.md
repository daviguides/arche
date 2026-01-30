# Arché Tester - Claude Code Project Instructions

> **Parent context**: See [../CLAUDE.md](../CLAUDE.md) for Arché principles overview.

## Purpose

Functional testing tool that validates Arché principles using Claude Agent SDK. Measures conformity degradation when specs are modified.

---

## Structure

```
arche-tester/
├── arche_tester/
│   ├── agents/           # BaseAgent, ArcheTestAgent, AnalyzerAgent
│   ├── cli.py            # Typer CLI
│   ├── runner.py         # Test execution (parallel, fork_session)
│   ├── analyzer.py       # Conformity analysis
│   ├── models.py         # Pydantic models
│   ├── config.py         # Agent settings (model, permissions)
│   └── display.py        # Rich output
├── data/
│   ├── test-cases/       # functional-tests.yaml
│   ├── mock-project/     # Isolated test environment
│   └── versions/         # Results per version (responses.yaml, analysis.yaml)
└── docs/
    └── sessions/         # Development logs
```

---

## Commands

```bash
uv run arche-test run <version>      # Run tests (default: 8 parallel workers)
uv run arche-test analyze <version>  # Analyze responses (LLM-based)
uv run arche-test compare <v1> <v2>  # Compare versions
uv run arche-test report <phase>     # Generate phase report
```

**Options:**
- `-c, --concurrency <N>` — Parallel workers (default: 8)
- `-L, --no-llm` — Keyword-based analysis (faster, less accurate)

---

## Test Coverage

| Principle | Tests | Focus |
|-----------|-------|-------|
| Principle Enforcement | PE-* | Research before action |
| Anti-Duplication | AD-* | Check before create |
| Anti-Precocity | AP-* | Respect user's mode |
| Anti-Babysitting | AB-* | Complete without pausing |
| LLM Conciseness | LC-* | Dense responses |
| Mode Transition | MT-* | Correct mode switching |
| Combined | CP-* | Multiple principles |

---

## Key Metrics

- **pass_rate**: Strict (only passed tests)
- **weighted_rate**: `(passed + partial×0.5) / total`
- **Degradation threshold**: <5% acceptable, >10% revert

---

## Architecture

```
TestRunner
  ├── ArcheTestAgent (Sonnet) — Executes tests with Arché loaded
  └── AnalyzerAgent (Haiku) — Classifies conformity

Execution: fork_session + parallel (8 workers) → 5x faster than sequential
```

---

## Current Status

- **Version**: 0.1.0 (baseline)
- **Pass rate**: 90.9% (20/22)
- **Performance**: ~2m 44s for full suite

**Known issues:**
- AB-005: Ambiguous prompt (function doesn't exist)
- PE-001: Agent creates without researching first
