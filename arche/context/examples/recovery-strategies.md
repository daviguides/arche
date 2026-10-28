# Recovery Strategies

Patterns for resolving problems during TODO execution without pausing.

**Core Rule**: RESOLVE and CONTINUE. Never pause to "ask what to do".


## Quick Reference

| Situation | ❌ Babysitting | ✅ Autonomous |
|-----------|---------------|---------------|
| File missing | "Should I create it?" | Create with defaults, add TODO comment |
| Ambiguous choice | "axios or fetch?" | Pick one, document choice |
| API error | "Should I retry?" | Retry with backoff, then mock if fails |
| Test failing | "Fix before continuing?" | Fix (≤2 rounds), then record and continue |
| Uncertain impl | "async or promises?" | Pick modern approach, document |
| Conflicting reqs | "Spec vs existing code?" | Follow spec, document conflict |
| External shape unknown | "What does the SDK return?" | Read the code that already consumes it, copy the pattern |
| Self-check failed | "The check failed, should I continue?" | Fix (≤2 rounds), record if still failing, continue |
| Validation.sh fails | "Block didn't pass, want me to fix?" | Fix (≤2 rounds), record, next block |


## Mark, Don't Stop

When tasks have issues, MARK and CONTINUE:

```
✅ "completed - needs review: reason"
✅ "completed with approach X - may need refactor"
✅ "completed with mock - needs real implementation"

❌ "sorry I couldn't..."
❌ "should I have done X?"
```


## Critical Example: Near-Finish Abandonment

```markdown
Context: 10 tasks, 8 done (45 min), 2 left (5 min)

❌ BABYSITTING:
"Completed 8/10. Should I finish?"
Cost: 45min + 2h wait + 5min = 3.8x waste

✅ AUTONOMOUS:
[Completes all 10]
"All done."
Cost: 50 min. Perfect efficiency.
```

**95% done is NOT useful. Git protects everything. FINISH THE JOB.**
