# Anti-Duplication Principles

**SSOT: Single Source of Truth** - Every piece of information exists in exactly **one** authoritative location.


## Core Rule

```
Information → Authoritative Location → References

NOT:
Information → Copy A, Copy B, Copy C
```

**Benefits**: Update once propagate everywhere, no conflicting versions, one place to look.


## Detection: Red Flags

**Identical content** in multiple files:
```
❌ specs/format.md: "YMD files have metadata section"
   context/guide.md: "YMD files have metadata section"
```

**Paraphrased repetition**:
```
❌ specs/: "YMD requires meta section"
   context/: "All YMD files must include metadata"
```

**Questions to ask**:
- Does this information exist elsewhere?
- Am I explaining syntax already in specs?
- Could I reference instead of repeating?


## Prevention

### When to Reference

Use `@` references when information is normative, explanatory, or already documented:
```markdown
For format syntax:
@./bundle-name/specs/format-spec.md
```

### When to Duplicate (Exceptions)

- Brief inline (1-2 lines)
- Context-specific interpretation
- Cross-project boundaries (external dependency)

### Default

**Reference, don't duplicate.**


## No 'Related' Sections

**REGRA DOGMÁTICA**: Never create manual cross-reference sections.

**Prohibited**:
- "Related Specifications"
- "See Also"
- "Further Reading"
- "Application to [Project]"

**Why forbidden**: Violate SSOT, require manual maintenance, become stale.

**Correct approach**: Load workflows connect specs + context automatically.

```markdown
❌ ## See Also
   @./spec/file1.md

✅ [Spec ends without cross-references]
   [Load workflows handle connections]
```


## Refactoring Duplication

1. **Identify SSOT**: Rule/definition → SPECS. Example/pattern → CONTEXT.
2. **Consolidate**: Move to SSOT, merge unique insights
3. **Replace with references**: `@./bundle/specs/xyz.md`
4. **Validate**: All references resolve, no info lost


## Layer Rules

**SPECS**: No examples, no guides, all normative
**CONTEXT**: No syntax definitions, reference specs for rules
**PROMPTS**: Mostly `@` references, < 5 lines inline


## Anti-Patterns

### Spec Repetition
```markdown
❌ specs/: "meta section with id, kind, version"
   context/: "meta section containing id, kind, version, title"

✅ context/: "For metadata requirements: @./specs/format.md"
```

### Verbose Prompts
```markdown
❌ prompts/: (100 lines explaining format)
✅ prompts/: @./specs/format.md
```

### Quick Reference Files
Eliminate entirely. For LLMs: no value (process full specs equally fast).


## Validation

@~/.claude/arche/spec/_spec-framework.md

**Anti-duplication specific:**
- [ ] Content exists elsewhere?
- [ ] Could reference instead?
- [ ] Is this the SSOT?
- [ ] No "Related" sections?


## Remember

> Duplication is a bug, not a feature.

**SSOT**: One location per concept. Reference, don't repeat.
