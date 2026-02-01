# LLM Conciseness Principles

**Dogmatic principles for token economy in LLM-optimized content.**


## Core Philosophy

**Maximize signal. Minimize noise.**

Information density = unique concepts / total tokens.

**REGRA DOGMÁTICA**: If removing a word doesn't change meaning, the word doesn't belong.

Token economy is virtue. Every wasted token = lost context window space.


## Mandatory Rules

### Rule 1: Eliminate Filler Words

**Prohibited**: basically, actually, really, very, quite, rather, simply, just, fairly, somewhat, essentially, "in order to", "it is important to note that"

```markdown
❌ It is important to note that users should basically just use validation.
✅ Use validation.
```

### Rule 2: Active Voice Imperative

✅ "Use X", "Write Y", "Avoid Z"
❌ "X should be used", "It is recommended that Y"

```markdown
❌ The file should be read by the LLM.
✅ LLM reads the file.
```

### Rule 3: Scannable Prose over Bullet Sprawl

Use lists ONLY for real options. Use prose for explanations.

```markdown
❌ BULLET SPRAWL:
- Be clear
- Be concise
- Go to point

✅ PROSE:
Write with clarity. Go straight to the point.
```

### Rule 4: Paragraph Length

Max 2-3 sentences per chunk. Add line breaks between thought blocks.

### Rule 5: Show Code, Don't Describe

```markdown
❌ To check status, execute git status command in terminal...
✅ Check status:
```bash
git status
```
```

### Rule 6: Emoji Semantics Only

**Allowed**: ✅ ❌ ⚠️ 🔴 🟡 🟢 (semantic)
**Prohibited**: 🚀 💡 ✨ 🎯 🔥 (decorative)

Test: "If I remove emoji, does meaning change?" NO → Prohibited.

### Rule 7: Semantic Markdown

- **Bold**: Key concepts, rules
- *Italic*: Technical terms, emphasis
- `>` Blockquote: Core principles, TL;DR
- `---`: ONLY major topic transitions (< 3 per doc)


## Detection: Red Flags

- Filler words (basically, actually, just)
- Passive voice ("should be", "can be")
- Bullet sprawl (fragmented single thought)
- Buried leads (important info after preamble)
- Paragraph bloat (> 6 lines)
- Prose describing code
- HR overuse (> 3 per doc)


## Anti-Patterns

### Bullet Sprawl
```markdown
❌ Benefits:
- Eliminates burden
- Prevents issues
- Reduces load

✅ **Benefits**: Eliminates burden, prevents issues, reduces load.
```

### Buried Lead
```markdown
❌ In this document we explore conciseness... The key principle is token economy.
✅ **Token economy**: Every token must carry semantic value.
```

### Redundant Repetition
```markdown
❌ Use active voice. Don't use passive. Avoid passive phrasing.
✅ Use active voice. Avoid passive.
```

### Academic Verbosity
```markdown
❌ It should be noted that in order to achieve optimal results...
✅ Use validation.
```


## Validation

@~/.claude/arche/spec/_spec-framework.md

**Conciseness specific:**
- [ ] Zero filler words?
- [ ] Active voice 90%+?
- [ ] Code blocks for code?
- [ ] HRs < 3 per document?
- [ ] Lists only for real options?


## Remember

> Every word must justify existence. If it doesn't add meaning, delete it.

**Token economy is virtue**. Code > prose. Show, don't tell.
