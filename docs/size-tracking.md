# Arché Size Tracking

## Current (v0.4.2) - 2025-01-31

| Arquivo | Bytes | KB | Status |
|---------|-------|-----|--------|
| essential-cognitive-modes.md | 6,942 | 6.8 | ✅ carregado |
| anti-babysitting.md | 4,151 | 4.1 | ✅ carregado |
| principle-enforcement.md | 3,354 | 3.3 | ✅ carregado |
| llm-conciseness.md | 3,140 | 3.1 | ✅ carregado |
| mode-transitions.md | 3,068 | 3.0 | ✅ carregado |
| mode-execution-guide.md | 3,061 | 3.0 | ✅ carregado |
| anti-precocity.md | 2,999 | 2.9 | ✅ carregado |
| anti-duplication.md | 2,964 | 2.9 | ✅ carregado |
| _spec-framework.md | 1,764 | 1.7 | ✅ carregado |
| pre-create-checkpoint.md | 1,564 | 1.5 | ✅ carregado |
| recovery-strategies.md | 1,399 | 1.4 | ✅ carregado |
| **Total Carregado** | **34,406** | **33.6** | |

### Removido
- debugging-mode.md (5,674 bytes) — modo opcional, pertence ao Dao

---

## Evolução de Tamanho

| Versão | Total (KB) | Delta | Pass Rate |
|--------|------------|-------|-----------|
| v0.1.0 (baseline) | 89.7 | — | 90.9% |
| v0.2.0 | 64.9 | -27.6% | — |
| v0.3.6 | ~40 | -38.4% | 86-100% |
| v0.4.0 | ~35 | -14% | 100% |
| v0.4.1 | ~34 | -3% | 100% |
| v0.4.2 | **33.6** | -1% | 100% |

**Redução total: 89.7 KB → 33.6 KB (-62.5%)**

---

## Por Arquivo - Histórico Completo

### Specs (spec/)

| Arquivo | v0.1.0 | v0.4.2 | Redução |
|---------|--------|--------|---------|
| anti-babysitting.md | 24.2 KB | 4.1 KB | -83% |
| llm-conciseness.md | 16.8 KB | 3.1 KB | -81% |
| anti-precocity.md | 15.8 KB | 3.0 KB | -81% |
| principle-enforcement.md | 15.2 KB | 3.3 KB | -78% |
| anti-duplication.md | 12.7 KB | 3.0 KB | -76% |
| essential-cognitive-modes.md | 7.9 KB | 6.8 KB | -14% |
| debugging-mode.md | 5.7 KB | **REMOVIDO** | -100% |
| _spec-framework.md | — | 1.8 KB | +novo |

### Context (context/)

| Arquivo | v0.1.0 | v0.4.2 | Notas |
|---------|--------|--------|-------|
| mode-transitions.md | — | 3.0 KB | extraído de anti-precocity |
| mode-execution-guide.md | — | 3.0 KB | extraído de modes |
| recovery-strategies.md | — | 1.4 KB | extraído de anti-babysitting |
| pre-create-checkpoint.md | — | 1.5 KB | extraído de principle-enforcement |
| validation-flow.md | — | **REMOVIDO** | redundante |

---

## Mudanças por Versão

### v0.4.0
- Consolidou Mode Signal Vocabulary (-50 linhas)
- Removeu seção Extensibility

### v0.4.1
- Deletou validation-flow.md (redundante)
- Consolidou mode-transitions.md: 7→4 anti-patterns
- Consolidou recovery-strategies.md: formato tabela
- context/examples: 13.1KB → 4.5KB (-66%)

### v0.4.2
- Removeu debugging-mode.md (modo opcional, não essencial)

---

## Meta vs Realidade

| Métrica | Meta Original | Alcançado |
|---------|---------------|-----------|
| Tamanho | ≤50 KB | 33.6 KB ✅ |
| Pass rate | ≥85% | 100% ✅ |
| Arquivos carregados | 11 | 11 ✅ |
