# LLM Conciseness Principles

**Dogmatic principles for token economy and information density in LLM-optimized content.**

**Purpose**: Guidelines for creating SPECS, CONTEXT, and PROMPTS optimized for LLM processing, not human reading.

---

## Core Philosophy

### Information Density Principle

**Maximize signal. Minimize noise.**

Information density = unique concepts / total tokens. Every token must carry semantic value.

**REGRA DOGMÁTICA**: If removing a word doesn't change meaning, the word doesn't belong.

### LLM-Optimized Expression

LLMs process contextual prose better than fragmented structures.

**Key insight**: Human-readable ≠ LLM-readable. Optimize for LLM processing, not visual aesthetics.

Scannable prose with strategic line breaks > bullet sprawl.

### Token Economy as Virtue

> "Brevity is the soul of wit." — Applies 10x more to LLM contexts.

Tokens are currency. Spend wisely. Every wasted token is:
- Lost context window space
- Reduced information density
- Increased processing cost
- Degraded signal-to-noise ratio

**Goal**: Maximum meaning per token.

---

## Mandatory Rules (Dogmático)

### Rule 1: Eliminate Filler Words

**REGRA DOGMÁTICA**: Remove all filler words that carry zero semantic value.

**Prohibited list**:
- basically, actually, really, very, quite, rather
- simply, just, fairly, somewhat, essentially
- generally, typically, usually (when not adding precision)
- in order to (use "to")
- it is important to note that (delete entirely)
- should be noted that (delete entirely)

**Examples**:

```markdown
❌ VERBOSE:
It is important to note that users should basically just use the validation
command in order to ensure that files are actually correct.

✅ CONCISE:
Use validation to ensure files are correct.
```

**Validation**:
```bash
# Automated detection (should return empty)
grep -rn "basically\|actually\|just\|simply\|really\|very\|quite\|rather" \
  --include="*.md" --exclude-dir=docs --exclude-dir=.git \
  --exclude="llm-conciseness.md"
```

**Exceção permitida**: Literal quotations in examples where authenticity matters.

### Rule 2: Active Voice Imperative

**REGRA DOGMÁTICA**: Use active voice with imperative mood.

**Pattern**:
- ✅ **ALWAYS**: "Use X", "Write Y", "Avoid Z"
- ❌ **NEVER**: "X should be used", "It is recommended that Y be written", "Z should be avoided"

**Examples**:

```markdown
❌ PASSIVE:
The file should be read by the LLM.
It is recommended that validation be performed.
References should be used instead of duplication.

✅ ACTIVE:
LLM reads the file.
Perform validation.
Use references instead of duplication.
```

**Exceção permitida**: When passive voice genuinely obscures an irrelevant agent.

### Rule 3: Scannable Prose over Bullet Sprawl

**REGRA DOGMÁTICA**: Use lists ONLY for real options. Use scannable prose for explanations.

LLMs process connected prose contextually. Fragmenting paragraphs into bullets for aesthetics _reduces_ comprehension.

**When to use lists**:
- Enumeration of distinct options (A or B or C)
- Checklists of actions
- Structural comparisons

**When NOT to use lists**:
- Explanation of a single concept artificially fragmented
- "Points" that form continuous thought
- Making text "look pretty"

**Examples**:

```markdown
❌ BULLET SPRAWL (one concept fragmented):
To write well:
- Be clear
- Be concise
- Avoid verbosity
- Go straight to the point

✅ SCANNABLE PROSE:
Write with clarity and conciseness. Go straight to the point.

Avoid detours. Each sentence carries meaning. No filler words.

---

✅ APPROPRIATE LIST (real options):
Choose loading strategy:
- Monolithic: single context, cohesive project
- Modular: independent contexts, composable
```

### Rule 4: Paragraph Length Limits

**REGRA DOGMÁTICA**: Max 2-3 sentences per chunk. Add line breaks between thought blocks.

Long paragraphs are hard to scan. Break into digestible chunks.

**Pattern**:
- 1-3 sentences → Single paragraph OK
- 4-6 sentences → Add line break at logical split
- 7+ sentences → Refactor into multiple paragraphs

**Examples**:

```markdown
❌ UNSCANNABLE WALL:
The system loads specs via @ references which are processed by the LLM which then extracts relevant context applying anti-duplication principles maintaining SSOT and ensuring consistency through automated validation that checks for duplicates and verifies reference integrity across all files.

✅ SCANNABLE CHUNKS:
The system loads specs via @ references. LLM processes and extracts relevant context.

Anti-duplication principles maintain SSOT. Automated validation ensures consistency.

Validation checks for duplicates and verifies reference integrity.
```

**Validation**: Paragraphs >6 lines without breaks → refactor.

### Rule 5: Show Code, Don't Describe Code

**REGRA DOGMÁTICA**: Use code blocks for code. Never describe code in prose when code is self-explanatory.

**Pattern**:
- ✅ Code block + minimal comment
- ❌ Verbose prose describing what code does

**Examples**:

```markdown
❌ VERBOSE DESCRIPTION:
To check the status of the repository, you would execute the git status
command in your terminal, which will show you the current state of your
working directory and staging area.

✅ CONCISE CODE:
Check repository status:
```bash
git status
```

---

❌ OVER-EXPLAINED:
The following command searches recursively through all markdown files,
excluding the docs directory and git directory, looking for the pattern
"@~/.claude/gradient/" and counts the number of matches found.

✅ MINIMAL COMMENT:
Count relative references:
```bash
grep -r "@\./gradient/" --include="*.md" --exclude-dir=docs | wc -l
```
```

### Rule 6: Emoji Semantics Only

**REGRA DOGMÁTICA**: Use emojis ONLY when they carry clear semantic meaning for LLMs.

**Allowed (semantic)**:
- ✅ / ❌ : Correct vs Incorrect (high semantic clarity)
- 🔴 / 🟡 / 🟢 : Severity levels (ERROR / WARNING / OK)
- ⚠️ : Warning/Attention

**Prohibited (decorative)**:
- 🚀 💡 ✨ 🎯 🔥 etc. (zero semantic value, pure "flavor")

**Validation test**: "If I remove emoji, does meaning change?"
- YES → Allowed
- NO → Prohibited

**Preference**: Always prefer semantic markdown over emoji.

```markdown
Prefer: **IMPORTANT**: ...
Avoid:  📌 IMPORTANT: ...

Allow:  ✅ CORRECT / ❌ WRONG (high clarity)
```

### Rule 7: Semantic Markdown for LLMs

**REGRA DOGMÁTICA**: Use markdown semantically, not aesthetically.

LLMs process markdown structure. Use it to signal meaning, not to "make pretty."

#### Bold (`**word**`)
**Use for**:
- Key concepts, rules, anti-patterns
- First mention of critical terms
- Emphasis on inviolable principles

**Don't use for**:
- Aesthetics or "highlighting"
- Entire sentences (use structure instead)

#### Italic (`_term_`)
**Use for**:
- First mention of technical terms
- Contextual emphasis within sentence
- Foreign terms or special vocabulary

**Don't use for**:
- Duplicating bold
- Highlighting entire phrases

#### Blockquote (`> phrase`)
**Use for**:
- Core philosophical principles
- TL;DR summaries
- Pull quotes of key insights

**Don't use for**:
- Visual separators
- Arbitrary highlighting

#### Horizontal Rule (`---`)
**REGRA DOGMÁTICA**: Use `---` ONLY for major topic transitions.

**Use when**:
- Transitioning between major sections (`##` level)
- Major conceptual shift
- Target: **<3 HRs per document**

**Don't use when**:
- Between related subsections (`###`)
- As visual decoration
- Before/after code blocks
- Between consecutive examples

**Why**: LLMs use hierarchical structure (`#`, `##`, `###`), not horizontal lines. Overuse adds noise.

**Examples**:

```markdown
❌ OVERUSE:
---
## Section 1
---
**This is very important.**
---
## Section 2
---

✅ DISCIPLINED USE:
## Section 1

**SSOT**: Each piece of information exists in _exactly_ one place.

Duplication causes inconsistency. SPECS define, CONTEXT applies, PROMPTS orchestrate.

---

## Section 2: Detection (Major Topic Shift)

Symptoms of duplication include...
```

---

## Guidelines (Orientativo)

### Guideline 1: Progressive Disclosure

Start with essence. Expand if necessary.

Don't bury the lead. Put conclusions first, justifications second.

**Pattern**:

```markdown
✅ ESSENCE FIRST:
**SSOT**: Each piece of information exists in exactly one place.

Duplication causes inconsistency, maintenance burden, token waste.

❌ BURIED LEAD:
In this document we will explore the concept of Single Source of Truth,
also known as SSOT, which is a fundamental principle that addresses
the challenges of maintaining consistency across large documentation sets...
```

### Guideline 2: Tables for Multi-Dimensional Comparison

Use tables when comparing 3+ dimensions. Use prose for simple comparisons.

**Appropriate**:

| Approach | When Use | Pros | Cons |
|----------|----------|------|------|
| Direct @ | 1-2 files | Explicit | Duplication |
| Command | 3+ files | DRY | Indirection |

**Inappropriate** (prose would be better):

| Term | Definition |
|------|------------|
| SSOT | Single Source of Truth |
| DRY | Don't Repeat Yourself |

Better as:
```markdown
**SSOT** (Single Source of Truth): Each piece of information exists once.
**DRY** (Don't Repeat Yourself): Avoid duplication.
```

### Guideline 3: Front-Load Code Blocks

When showing examples, lead with code, follow with minimal explanation if needed.

```markdown
✅ CODE FIRST:
```bash
make dev
```
Converts references to relative paths for local development.

❌ EXPLANATION FIRST:
To convert all references to relative paths for local development,
you would use the following command...
```bash
make dev
```
```

---

## Detection: Symptoms of Verbosity

### Red Flags

Scan your content for these warning signs:

**Filler words**: basically, actually, just, simply, really, very
**Passive constructions**: "should be", "can be", "is recommended"
**Bullet sprawl**: Lists of sentences forming single thought
**Buried leads**: Important info after 3+ paragraphs of setup
**Paragraph bloat**: >6 lines without line breaks
**Description > code**: Prose explaining what code shows
**Over-explanation**: Explaining the obvious
**Redundant repetition**: Saying same thing 3 different ways
**Academic verbosity**: "In this section we will...", "It should be noted that..."
**HR overuse**: More than 3 `---` separators in single document

### Self-Assessment Questions

Before finalizing content:
- [ ] Could I remove any word without losing meaning?
- [ ] Am I using passive voice without good reason?
- [ ] Are my lists real options or fragmented prose?
- [ ] Could I show code instead of describing it?
- [ ] Does every paragraph justify its existence?
- [ ] Am I front-loading key information?
- [ ] Is markdown adding semantic value or just aesthetics?

---

## Refactoring: Making Content Concise

### Step 1: Eliminate Filler Words

**Scan**:
```bash
grep -rn "basically\|actually\|just\|simply\|really\|very" file.md
```

**Delete all matches** unless in literal quotations.

### Step 2: Convert Passive to Active

**Pattern**: Find "should be", "can be", "is recommended"

**Transform**:
- "File should be read" → "Read file"
- "Can be used" → "Use"
- "Is recommended" → "Recommendation:"

### Step 3: Add Line Breaks to Long Paragraphs

**Scan**: Find paragraphs >4 sentences

**Refactor**: Break into 2-3 sentence chunks at logical thought boundaries.

### Step 4: Audit Bullet Lists

**For each list**: "Are these real options or fragmented prose?"

**If fragmented prose**: Consolidate into scannable paragraphs.

### Step 5: Lead with Code

**Scan**: Find prose descriptions of commands/syntax

**Refactor**: Show code block first, minimal comment after (if needed).

### Step 6: Remove Redundant HRs

**Scan**: Count `---` occurrences

**Target**: <3 per document. Remove decorative separators, keep only major transitions.

---

## Validation Checklist

### Content Audit

- [ ] Zero filler words (except literal quotes)?
- [ ] Active voice in 90%+ sentences?
- [ ] Lists only for real options (not fragmented prose)?
- [ ] Paragraphs <6 lines or broken at thought boundaries?
- [ ] Code blocks for code (not prose descriptions)?
- [ ] Each paragraph justifies existence?
- [ ] Lead buried? (Important info first?)
- [ ] Information density >1 concept per 10 tokens?

### Markdown Audit

- [ ] Bold used semantically (concepts, rules)?
- [ ] Italic used for technical terms, emphasis?
- [ ] Blockquotes for principles/TL;DR only?
- [ ] Horizontal rules <3 per document?
- [ ] Emojis only semantic (✅❌⚠️)?
- [ ] No decorative emojis (🚀✨💡)?

---

## Metrics

### Token Density

**Target**: 1+ unique concept per 10 tokens

**Measurement** (manual):
1. Count unique concepts introduced
2. Count total tokens (rough estimate: words × 1.3)
3. Ratio should be >0.1

**Example**:
- Bad: 100 tokens, 5 concepts = 0.05 density
- Good: 100 tokens, 15 concepts = 0.15 density

### Paragraph Length

**Target**: <6 lines per paragraph OR line breaks every 2-3 sentences

**Validation**: Manual scan for paragraph bloat.

### Filler Word Count

**Target**: Zero (except literal quotations)

**Script**: `gradient/scripts/detect-filler-words.sh`

### Horizontal Rule Count

**Target**: <3 per document

**Validation**: `grep -c "^---" file.md`

---

## Common Anti-Patterns

### Anti-Pattern 1: Bullet Sprawl

**Problem**: Fragmenting continuous thought into artificial list.

```markdown
❌ BULLET SPRAWL:
Benefits of SSOT:
- Eliminates maintenance burden
- Prevents inconsistencies
- Reduces cognitive load
- Minimizes token waste

✅ SCANNABLE PROSE:
**SSOT benefits**: Eliminates maintenance burden, prevents inconsistencies, reduces cognitive load, minimizes token waste.

Or with line breaks:
**SSOT eliminates** maintenance burden and prevents inconsistencies.

It reduces cognitive load and minimizes token waste.
```

### Anti-Pattern 2: Buried Lead

**Problem**: Important information after paragraphs of preamble.

```markdown
❌ BURIED LEAD:
In this document we will explore various aspects of conciseness as it
relates to writing documentation for LLM consumption, taking into account
the unique processing characteristics of modern language models and how
they differ from human readers. The key principle is token economy.

✅ LEAD FIRST:
**Token economy**: Every token must carry semantic value.

LLMs process differently than humans. Optimize for token density.
```

### Anti-Pattern 3: Redundant Repetition

**Problem**: Saying the same thing multiple ways without adding meaning.

```markdown
❌ REDUNDANT:
Use active voice. Don't use passive constructions. Avoid passive phrasing.
Write with active verbs instead of passive voice.

✅ CONCISE:
Use active voice. Avoid passive constructions.
```

### Anti-Pattern 4: Academic Verbosity

**Problem**: Formal academic phrasing that adds zero value.

```markdown
❌ ACADEMIC:
It should be noted that in order to achieve optimal results, it is
highly recommended that one should consider utilizing the validation
procedure, which has been designed to ensure correctness.

✅ DIRECT:
Use validation to ensure correctness.
```

### Anti-Pattern 5: Passive Voice Overuse

**Problem**: Hiding actors with passive constructions.

```markdown
❌ PASSIVE:
The file should be read by the LLM.
References can be used instead of duplication.
Validation should be performed regularly.

✅ ACTIVE:
LLM reads the file.
Use references instead of duplication.
Perform validation regularly.
```

### Anti-Pattern 6: Description Instead of Code

**Problem**: Verbosely describing what code clearly shows.

```markdown
❌ VERBOSE:
To check for filler words, you would use the grep command with the -r
flag for recursive search, the -n flag to show line numbers, and then
provide a pattern that matches common filler words like "basically" or
"actually" separated by the pipe character...

✅ CONCISE:
Detect filler words:
```bash
grep -rn "basically\|actually\|just" --include="*.md" .
```
```

### Anti-Pattern 7: HR Overuse

**Problem**: Horizontal rules as visual decoration instead of semantic separators.

```markdown
❌ HR SPAM:
---
## Section 1
---
Content here
---
## Subsection
---
More content
---

✅ DISCIPLINED:
## Section 1

Content here

### Subsection

More content

---

## Section 2 (Major Shift)
```

---

## Validation

@~/.claude/arche/spec/_spec-framework.md (universal checklist)

**Conciseness specific:**
- [ ] Zero filler words?
- [ ] Active voice 90%+?
- [ ] Code blocks for code (not prose)?
- [ ] HRs < 3 per document?

---

## Remember

> Every word must justify existence. If it doesn't add meaning, delete it.

**Token economy is virtue**. Code > prose. Show, don't tell.
