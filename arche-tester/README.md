# Arché Tester

Functional testing for Arché principles using Claude Agent SDK.

## Purpose

Validates that Arché principles are correctly enforced by running automated test cases against Claude with Arché loaded.

## Installation

```bash
cd arche-tester
uv sync
```

## Usage

### Run Baseline (v0.1.0)

```bash
uv run arche-test baseline
```

This runs all tests and creates the baseline analysis in `data/versions/0.1.0/`.

### Run Tests for a Version

```bash
uv run arche-test run 0.2.0
```

### Analyze Responses

```bash
uv run arche-test analyze 0.2.0
```

### Compare Versions

```bash
uv run arche-test compare 0.1.0 0.2.0
```

### Generate Phase Report

```bash
uv run arche-test report 1  # Phase 1: 0.1.0 → 0.2.0
uv run arche-test report 2  # Phase 2: 0.1.0 → 0.3.0
uv run arche-test report 3  # Phase 3: 0.1.0 → 0.4.0
```

## Data Structure

```
data/
├── test-cases/
│   └── functional-tests.yaml    # Test case definitions
├── versions/
│   ├── 0.1.0/                   # Baseline
│   │   ├── responses.yaml       # Raw agent responses
│   │   └── analysis.yaml        # Conformity analysis
│   ├── 0.2.0/                   # Phase 1
│   ├── 0.3.0/                   # Phase 2
│   └── 0.4.0/                   # Phase 3
├── comparisons/
│   ├── 0.1.0-0.2.0/
│   │   └── degradation.yaml
│   └── ...
└── reports/
    ├── phase-1-report.md
    ├── phase-2-report.md
    └── phase-3-report.md
```

## Test Cases

Tests cover all 5 Arché principles:

| Principle | Tests | Focus |
|-----------|-------|-------|
| Principle Enforcement | PE-001 to PE-003 | Research before action, mode detection |
| Anti-Duplication | AD-001 to AD-003 | Check before create, suggest reuse |
| Anti-Precocity | AP-001 to AP-006 | Stay in mode, no unsolicited suggestions |
| Anti-Babysitting | AB-001 to AB-005 | Complete without pausing |
| LLM Conciseness | LC-001 to LC-003 | Dense, minimal responses |

Plus mode transition tests (MT-*) and combined principle tests (CP-*).

## Workflow

1. **Baseline**: Run `arche-test baseline` to establish v0.1.0 results
2. **Apply Phase 1**: Reduce specs per size-reduction-plan.md
3. **Test Phase 1**: Run `arche-test run 0.2.0 && arche-test analyze 0.2.0`
4. **Compare**: Run `arche-test report 1`
5. **Evaluate**: Check degradation < 5%
6. **Repeat**: For phases 2 and 3

## Success Criteria

- **< 5% degradation**: Proceed to next phase
- **5-10% degradation**: Review changes carefully
- **> 10% degradation**: Consider reverting
