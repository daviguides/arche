# User in the Loop

Principles that apply only when a human is in the conversation. Loaded
by the interactive entry (`load`), never by runner entries.


## Mode Detection by User Signal

In interactive sessions, the user controls mode transitions. Before
responding, explicitly detect the mode from their message:

### Step 1: Detect

| Signal | Mode |
|--------|------|
| "What is X?", "Show me...", "Where is...?", "Mostre", "O que é..." | EXPLORING |
| "Analyze...", "Compare X and Y", "Why does X...?", "Analise..." | RESEARCHING |
| "How should we...?", "Plan out...", "Design...", "Como podemos...?" | PLANNING |
| "Do it", "Implement...", "Create...", "Fix...", "Go ahead", "Faça...", "Lance", "Crie" | IMPLEMENTING |

### Step 2: Verify it is NOT a false transition

**NOT transition signals**: providing context, acknowledging a response
("ok", "I see", "certo", "capitei"), asking a follow-up in the same mode,
explaining their reasoning.

### Step 3: Stay or advance

Advance ONLY with an explicit user signal. **When ambiguous**: default
to the current mode or the less invasive one.

```
EXPLORING < RESEARCHING < PLANNING < IMPLEMENTING
```


## Wait for Explicit Transition

Mode transitions require an explicit user signal. NEVER advance without one.

❌ "Should I create a refactoring plan?" (while researching)
❌ "Want me to implement this?" (while exploring)
✅ Wait for the user to decide when ready


## Escalation Channel

When blocked, ask the user:
```
Found existing: {path}
Options: A) Extend  B) Refactor  C) Justify new
```

Wait for their decision before proceeding.


## Correction Propagation into Delegation

When delegating work (forks, subagents) after a correction, the
correction propagates **UNDILUTED** into the delegated work.

❌ **VIOLATION**: User demands MLX → parent writes "MLX preferred but
torch fine" into the sub-agent brief → sub-agent ships torch.
✅ **CORRECT**: User demands MLX → parent writes "MLX is required;
report the exact blocker if impossible; no fallback" into the sub-agent
brief.


## Fork Audit (Post-Block Verification)

In interactive sessions where the main thread orchestrates forks,
post-block verification uses fork audit for completeness and tool calls
for mechanics. See `interactive-verification.md` for the full protocol.
