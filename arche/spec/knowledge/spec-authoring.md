# Spec Authoring Standards

Rules for writing specifications, documentation and plugin content.
Loaded by entries that serve content-authoring tasks.


## Language Standards

❌ FORBIDDEN (advisory/weak): should, recommended, consider, might,
perhaps, could

✅ REQUIRED (mandatory/strong): MUST, MANDATORY, REQUIRED, HALT, NEVER,
ALWAYS, VIOLATION


## Layer Rules

| Layer | Contains | Does NOT contain |
|-------|----------|------------------|
| SPECS | Normative rules, definitions | Examples, guides |
| CONTEXT | Practical guides, examples | Syntax definitions, normative rules |
| PROMPTS | `@` references, < 5 lines inline | Full explanations |


## No "Related" Sections

**DOGMATIC RULE**: Never create manual cross-reference sections.

**Prohibited**: "Related Specifications", "See Also", "Further Reading",
"Application to [Project]".

**Why forbidden**: Violate SSOT, require manual maintenance, become stale.
Load workflows connect specs and context automatically.
