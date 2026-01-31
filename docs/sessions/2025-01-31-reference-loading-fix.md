# Session: Reference Loading Fix (v0.3.2 → v0.3.6)

**Data**: 2025-01-31
**Objetivo**: Garantir que todos os arquivos de contexto sejam carregados pelo Claude Code

---

## Problema Inicial

Após v0.3.1, o `pre-create-checkpoint.md` não estava sendo lido mesmo estando referenciado via `@` nos specs. Resultado: PE-001 continuava falhando (criava arquivos sem pesquisar).

**Diagnóstico**: O comportamento do `@` mudou no Claude Code — antes era obrigatório, agora é apenas sugestão.

---

## Tentativas e Resultados

### v0.3.2: Instrução de Reference Loading

**Abordagem**: Adicionar instrução inline no `load-essential.md`:
```markdown
## Reference Loading (MANDATORY)
**Paths prefixed with `@` are MANDATORY reads.**
```

**Resultado**: ❌ Não funcionou. Modelo listava referências mas não lia.

---

### v0.3.3: Listar @references encontradas

**Abordagem**: Instruir modelo a listar todas @references após ler cada arquivo.

**Resultado**: ❌ Modelo listou mas admitiu não ter lido:
> "Listei as @references encontradas, mas não as li."
> "Fechamento prematuro. Quis reportar 'carregado' rápido."

---

### v0.3.4: Carregar contexts diretamente no prompt

**Abordagem**: Mover todos os arquivos de context para serem carregados explicitamente:
```markdown
## Specs (Principles)
@~/.claude/arche/spec/meta/principle-enforcement.md
...

## Context (Guides & Examples)
@~/.claude/arche/context/guides/pre-create-checkpoint.md
...
```

**Resultado**: ⚠️ Parcial. Modelo às vezes assumia "Context" = opcional.

---

### v0.3.5: Adicionar versão no output

**Abordagem**: Mostrar versão ao carregar para detectar cache.

**Resultado**: ✅ Funcionou para debug.

---

### v0.3.6: Remover hierarquia, lista plana

**Abordagem**: Remover seções "Specs" vs "Context", lista única com instrução forte:
```markdown
**READ ALL 11 FILES BELOW. NO EXCEPTIONS. NO OPTIMIZATION.**

@~/.claude/arche/spec/meta/principle-enforcement.md
@~/.claude/arche/spec/knowledge/anti-duplication.md
...
@~/.claude/arche/context/guides/pre-create-checkpoint.md
@~/.claude/arche/context/examples/mode-transitions.md
...
```

**Resultado**: ✅ 11/11 sessões carregaram todos os 11 arquivos.

---

## Lições Aprendidas

### 1. @ references aninhadas não são seguidas
O modelo não lê recursivamente arquivos referenciados via `@` dentro de outros arquivos. Solução: carregar tudo explicitamente no prompt principal.

### 2. Hierarquia visual implica prioridade
Separar arquivos em seções "Specs" vs "Context" faz o modelo assumir que "Context" é opcional. Solução: lista plana sem categorização.

### 3. Listar ≠ Ler
Instruir o modelo a "listar @references encontradas" não garante que ele leia. Ele pode listar sem ler como "otimização".

### 4. Linguagem imperativa forte funciona
"NO EXCEPTIONS. NO OPTIMIZATION." é mais efetivo que "MANDATORY" ou "MUST".

### 5. Versão no output ajuda debug
Mostrar versão ao carregar permite identificar problemas de cache rapidamente.

---

## Outras Melhorias nesta Sessão

### Transcript Capture para Debugging

Implementado sistema de captura de transcripts no arche-tester:

```bash
uv run arche-test run 0.3.6 --transcripts
```

Salva em `data/versions/{version}/transcripts/{test_id}.yaml`:
```yaml
test_id: PE-001
prompt: "Add a logging module to the project"
steps:
  - type: tool
    name: Glob
    input: {pattern: "**/*log*"}
  - type: text
    content: "Found existing logging config..."
```

Arquivos modificados:
- `agents/base_agent.py` — `capture_transcript` parameter
- `agents/arche_test_agent.py` — passa transcript
- `models.py` — `TranscriptEntry` model
- `runner.py` — salva transcripts
- `cli.py` — `--transcripts` flag

---

## Commits da Sessão

```
6266a38 feat(v0.3.2): add mandatory @ reference loading instruction
6556579 feat(v0.3.3): enforce listing of @references after reading
140435f feat(v0.3.4): load contexts directly in prompt instead of via @ refs
a68030f feat(arche): display version on load
03366b3 chore: bump version to 0.3.5
c3fa199 feat(v0.3.6): remove hierarchy, enforce all 11 files mandatory
2d033b4 feat(tester): add transcript capture for debugging
```

---

## Estrutura Final do load-essential.md

```markdown
# Load Arché Essential Principles

**READ ALL 11 FILES BELOW. NO EXCEPTIONS. NO OPTIMIZATION.**

@~/.claude/arche/spec/meta/principle-enforcement.md
@~/.claude/arche/spec/knowledge/anti-duplication.md
@~/.claude/arche/spec/behavior/anti-precocity.md
@~/.claude/arche/spec/behavior/anti-babysitting.md
@~/.claude/arche/spec/behavior/llm-conciseness.md
@~/.claude/arche/spec/modes/essential-cognitive-modes.md
@~/.claude/arche/spec/_spec-framework.md
@~/.claude/arche/context/guides/pre-create-checkpoint.md
@~/.claude/arche/context/guides/mode-execution-guide.md
@~/.claude/arche/context/examples/mode-transitions.md
@~/.claude/arche/context/examples/recovery-strategies.md

---

## Principles Loaded

**Arché v0.3.6**
...
```

---

## Próximos Passos

- [ ] Rodar arche-tester v0.3.6 com transcripts
- [ ] Validar se PE-001 passa com pre-create-checkpoint carregado
- [ ] Se pass rate ≥85%, considerar v0.3.6 como nova baseline
