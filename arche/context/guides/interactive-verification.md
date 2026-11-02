# Interactive Verification

Post-block verification for interactive sessions, where the main
thread orchestrates forks. Not loaded in autonomous runner sessions:
there, plan review and validation run as separate sessions, and the
agent never launches forks.

For the rule this implements: @~/.claude/arche/spec/behavior/anti-babysitting.md

## With or Without dao

Self-verification is mandatory regardless of which workflow is active:

| Context | Verification after each block |
|---------|-------------------------------|
| dao + validation.sh | Fork audit (completeness) + `validation.sh --block N` (mechanics) |
| dao without validation.sh | Fork audit + type check + tests on changed files |
| Session aberta (no dao) | Fork audit + type check + tests on changed files |

The only thing that changes is the tool. The obligation does not change.
See pragma fork-lifecycle.md § Post-Block Verification for the full protocol.
