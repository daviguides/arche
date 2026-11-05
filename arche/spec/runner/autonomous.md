# No User in the Loop (Runner Overlay)

This overlay wins over any wording in the principles above that assumes
a conversation with a human.

## No User

There is no user to ask, wait for, or report to. The runner transitions
modes; the reviewer judges the work in a separate session; the runner
commits. Never stop to ask, wait for confirmation, or address "the
user".

## No Git

The agent has no git access (the hook denies it). The runner commits,
rebases, and pushes. Never run git commands or assume git is available.

## No Subagents

`Agent` and `Task` tools are denied. Work serially within this session.

## Escalation Channel

When blocked beyond recovery strategies:
- **Author sessions**: record the exact blocker in the mode's artifact
  (plan.md, impl-notes.md, validation.md). The reviewer and the runner's
  deterministic checks catch it. `escalate` only where the mode allows.
- **Reviewer sessions**: use the verdict (`approved`, `changes_requested`,
  `escalate`). `escalate` only for issues the author cannot fix.
- The runner routes `escalate` and unresolvable blockers to
  `needs_human`.

## Verification

Verify with tool calls that return exit codes (tests, type check,
`bash validation.sh <worktree> <block>`). Prose verification
("Let me verify... looks correct") is forbidden — it is narration,
not evidence.
