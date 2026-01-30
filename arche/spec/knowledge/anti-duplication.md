# Anti-Duplication Principles

**Universal principles for preventing duplication and verbosity in layered architectures.**

---

## Core Philosophy

### Single Source of Truth (SSOT)

**Principle**: Every piece of information must exist in exactly **one** authoritative location.

**Rationale**:
- Eliminates maintenance burden (update once, propagate everywhere)
- Prevents inconsistencies (no conflicting versions)
- Reduces cognitive load (one place to look)
- Minimizes token waste (for LLMs)

**Implementation**:
```
Information ─→ Authoritative Location ─→ References
```

Not:
```
Information ─→ Location A (copy)
           ─→ Location B (copy)
           ─→ Location C (copy)
```

---

## Detection: Symptoms of Duplication

### Red Flags

**1. Identical Content in Multiple Files**
```
❌ BAD:
specs/format.md:
  "YMD files have metadata section"

context/guide.md:
  "YMD files have metadata section"
```

**2. Paraphrased Repetition**
```
❌ BAD:
specs/format.md:
  "YMD requires meta section"

context/examples.md:
  "All YMD files must include metadata"
```

**3. Explanation Duplication**
```
❌ BAD:
specs/syntax.md:
  Explains how variables work (50 lines)

context/guide.md:
  Explains how variables work again (45 lines)
```

**4. Example Redundancy**
```
❌ BAD:
Multiple files showing the same example
with slight variations but no new insight
```

### Detection Questions

Ask yourself:
- Does this information exist elsewhere?
- Am I explaining syntax that's already in specs?
- Am I showing an example that's already documented?
- Could I reference instead of repeating?

---

## Prevention: Reference vs Duplicate

### When to Reference

Use `@` references when:
- Information is **normative** (defined elsewhere)
- Content is **explanatory** (already documented)
- Examples are **complete** (shown elsewhere)
- Rules are **authoritative** (specs exist)

**Example**:
```markdown
For format syntax, see:
@./bundle-name/specs/format-spec.md

For complete examples:
@./bundle-name/context/examples.md
```

### When to Duplicate (Exceptions)

Only duplicate when:
- **Brief inline references** (1-2 lines)
- **Context-specific interpretation** (applying general rule to specific case)
- **Cross-project boundaries** (external dependency, copy for stability)

**Example of Acceptable Inline**:
```markdown
Use snake_case for identifiers (as defined in naming-spec.md).
```

### When in Doubt

**Default**: Reference, don't duplicate.

### No 'Related' Sections (Critical Rule)

**REGRA DOGMÁTICA**: Never create manual cross-reference sections.

**Prohibited section names**:
- "Related Specifications"
- "Related Documents"
- "Related Guides"
- "See Also"
- "For More Information"
- "Application to [Project Name]"
- "Further Reading"
- Any variant of manual navigation/reference lists

**Why all are forbidden**: They violate SSOT by creating manual cross-reference lists that:
- Duplicate load workflow's responsibility
- Require maintenance in multiple places
- Become stale when files are added/removed
- Add noise without value
- Create hidden dependencies

#### Common Disguises

Cross-references often hide as "helpful navigation":

```markdown
❌ WRONG - Classic "Related":
## Related Specifications
- @./spec/file1.md
- @./spec/file2.md

❌ WRONG - "See Also" variant:
## See Also
For more context, see:
- @./context/guide.md

❌ WRONG - "Application" disguise:
---

## Application to [Architecture Name]

For guidance on applying these principles to [Architecture]:

@./project/context/some-file.md

❌ WRONG - "Further Reading":
## Further Reading
- @./spec/advanced.md
- @./context/examples.md

✅ CORRECT:
[Spec ends without cross-references]

[Load workflows handle all connections]
```

#### The Right Way: Load Workflows

**Universal specs must be pure** - zero cross-references to applications or projects.

**If user needs context**:
1. Load workflows connect SPECS + CONTEXT automatically
2. User runs: `/project:load-context`
3. Load workflow loads: universal specs + project-specific context
4. No manual cross-references needed

**Example**:
```markdown
<!-- prompts/load-context.md -->
@./spec/anti-duplication.md       # Universal principles
@./context/project-application.md  # Project-specific guidance

<!-- NO cross-reference in anti-duplication.md itself -->
```

#### Why This Rule Exists

**Real example of what we almost did**:
```markdown
❌ In anti-duplication.md (universal spec):
---

## Application to Gradient Architecture

For guidance on applying SSOT to Gradient's layers:

@./context/gradient-layers-compliance.md
```

This violates Rule 4 because:
- Universal spec now knows about specific project (Gradient)
- Creates manual cross-reference that load workflows already handle
- Reduces reusability (other projects don't care about Gradient)
- Is literally a "Related Sections" disguise

**Correct approach**:
- `anti-duplication.md` stays pure (universal)
- `gradient-layers-compliance.md` exists in CONTEXT
- Load workflow connects both
- Zero cross-references between them

#### Validation

**Manual check**:
```bash
# Should return ZERO matches in specs
grep -rn "^## Related\|^## See Also\|^## Application to\|^## Further" \
  spec/ --include="*.md"
```

**Self-test**: Can I remove this section without breaking workflows?
- If YES → Section is noise, delete it
- If NO → You've created hidden dependency, refactor to load workflow

---

## Refactoring: Eliminating Duplication

### Step 1: Identify SSOT

For duplicated content, determine:
- Which file is the **authoritative source**?
- Is it normative (SPECS) or applied (CONTEXT)?

**Decision tree**:
```
Is it a rule/definition?
├─ YES → SSOT is in SPECS
└─ NO → Is it an example/pattern?
          ├─ YES → SSOT is in CONTEXT
          └─ NO → Is it orchestration?
                    └─ YES → SSOT is in PROMPTS
```

### Step 2: Consolidate

Move all content to the SSOT location:
- Keep **most complete** version
- Merge **unique insights** from copies
- Preserve **best examples**

### Step 3: Replace with References

In all other locations:
```markdown
<!-- Before (duplicated) -->
Detailed explanation of concept XYZ...
(50 lines repeated)

<!-- After (referenced) -->
For details on concept XYZ:
@./bundle-name/specs/xyz-spec.md
```

### Step 4: Validate

Check that:
- All references resolve
- No information was lost
- Each concept has ONE authoritative location
- References are clear and helpful

---

## Validation Checklist

### For Any File

- [ ] Does this content exist elsewhere?
- [ ] Am I explaining something already defined in SPECS?
- [ ] Am I showing an example already in CONTEXT?
- [ ] Could this be a reference instead?
- [ ] Is this the authoritative source for this information?

### For SPECS Files

- [ ] No working examples (only minimal illustrations)
- [ ] No implementation guides
- [ ] No repeated content from other specs
- [ ] All content is normative

### For CONTEXT Files

- [ ] No syntax definitions (reference SPECS instead)
- [ ] No repeated examples
- [ ] Each example provides unique value
- [ ] References specs for rules

### For PROMPTS Files

- [ ] Mostly `@` references
- [ ] <5 lines of inline content per section
- [ ] No duplicated instructions
- [ ] Orchestration only

---

## Common Anti-Patterns

### Anti-Pattern 1: Spec Repetition

**Problem**:
```markdown
<!-- specs/format.md -->
YMD files must have meta section with id, kind, version, title.

<!-- context/guide.md -->
YMD files must have a meta section containing:
- id: unique identifier
- kind: type
- version: semver
- title: description
```

**Solution**:
```markdown
<!-- context/guide.md -->
For YMD metadata requirements:
@./bundle-name/specs/format.md

Example metadata:
```yaml
meta:
  id: example
  kind: task
  version: 1.0.0
  title: Example
```
```

### Anti-Pattern 2: Example Duplication

**Problem**:
```markdown
<!-- context/examples.md -->
Example: Simple YMD
(50 lines)

<!-- context/guide.md -->
Here's a simple YMD example:
(same 50 lines with minor changes)
```

**Solution**:
```markdown
<!-- context/guide.md -->
For complete examples:
@./examples.md

Quick reference:
```yaml
meta:
  id: ...
```
(5 lines, essential only)
```

### Anti-Pattern 3: Verbose Prompts

**Problem**:
```markdown
<!-- prompts/load-context.md -->
YMD Format Overview:
(100 lines explaining YMD format)

PMD Format Overview:
(80 lines explaining PMD format)

Composition Rules:
(120 lines explaining composition)
```

**Solution**:
```markdown
<!-- prompts/load-context.md -->
## Format Specifications

@~/.claude/ymd-spec/spec/ymd-spec.md
@~/.claude/ymd-spec/spec/pmd-spec.md
@~/.claude/ymd-spec/spec/composition-spec.md

## Your Task

With these specs loaded, you can now...
```

### Anti-Pattern 4: Quick Reference Files

**Problem**:
```markdown
<!-- context/quick-reference.md -->
(Summarizes all specs in shorter form)
(Still 200 lines of duplication)
```

**Rationale for removal**:
- For LLMs: No value (can process full specs equally fast)
- Creates duplication
- Maintenance burden
- Quick ≠ Better for machines

**Solution**:
Eliminate "quick reference" files entirely.

---

## For LLMs: Implementation Guidelines

### When Generating Content

**Before writing**, ask:
1. Does this information exist in SPECS?
   - YES → Reference it with `@`, don't duplicate
2. Does this example exist in CONTEXT?
   - YES → Reference it, don't recreate
3. Is this a new, unique contribution?
   - YES → Place in appropriate layer

### When Reviewing Content

**Check for**:
- Syntax explanations in non-SPEC files
- Repeated examples
- Paraphrased rules
- Verbose prompts with inline content

**Action**: Flag and suggest refactoring to references.

### When Refactoring

**Process**:
1. Identify SSOT (SPECS > CONTEXT > PROMPTS)
2. Consolidate all content there
3. Replace duplicates with `@` references
4. Validate all references resolve

---

## For Humans: Practical Checklist

### Before Creating New File

- [ ] What layer does this belong to?
- [ ] Does similar content exist?
- [ ] Am I about to duplicate something?
- [ ] Could I reference instead?

### While Writing

- [ ] Am I explaining syntax (should be in SPECS)?
- [ ] Am I showing examples (should be in CONTEXT)?
- [ ] Am I orchestrating (should be in PROMPTS)?
- [ ] Is this line unique or duplicated?

### After Writing

- [ ] Run duplication check (search for similar content)
- [ ] Verify all references resolve
- [ ] Confirm SSOT for each concept
- [ ] Test that removing file doesn't lose information

---

## Metrics: Measuring Duplication

### Quantitative

**Duplication Ratio**:
```
Total Lines / Unique Information Lines = Duplication Ratio

Target: ≤ 1.1 (10% acceptable overlap for context)
Danger: > 1.3 (30% duplication indicates problems)
```

**Reference Density** (for PROMPTS):
```
@ References / Total Lines

Target: > 0.5 (majority should be references)
Danger: < 0.2 (too much inline content)
```

### Qualitative

**Red Flags**:
- Can't determine SSOT for a concept
- Multiple files "explain" the same thing
- Changes require updates in >2 places
- Difficult to locate authoritative information

**Green Flags**:
- Clear SSOT for every concept
- References feel natural
- Changes propagate automatically via references
- Easy to find authoritative source

---

## Evolution and Maintenance

### Handling Changes

**When spec changes**:
```
1. Update SSOT (specs file)
2. References automatically reflect change
3. No need to update referencing files
```

**When context changes**:
```
1. Update SSOT (context file)
2. References automatically reflect change
3. No duplication to sync
```

### Preventing Decay

**Regular audits**:
- Monthly: Scan for new duplication
- After major changes: Validate references
- Before releases: Run duplication metrics

**Tools** (potential):
- `find-duplicates.sh` - Detects similar content
- `validate-references.sh` - Checks @ links resolve
- `calculate-metrics.sh` - Measures duplication ratio

---

## Validation

@~/.claude/arche/spec/_spec-framework.md (universal checklist)

**Anti-duplication specific:**
- [ ] Does this content exist elsewhere?
- [ ] Could I reference instead of repeating?
- [ ] Is this the SSOT for this information?

---

## Remember

> Duplication is a bug, not a feature.

**SSOT**: One location per concept. Reference, don't repeat.
