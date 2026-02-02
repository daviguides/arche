# Arché Size Reduction Plan

## Diagnóstico

**Total atual**: 104KB (3,451 linhas)

### Distribuição por arquivo

| Arquivo | Tamanho | Linhas | Bloat Principal |
|---------|---------|--------|-----------------|
| anti-babysitting.md | 24KB | 863 | 449 linhas de few-shot examples (52%) |
| llm-conciseness.md | 20KB | 654 | 48 code blocks, exemplos redundantes |
| principle-enforcement.md | 16KB | 480 | 161 linhas de checkpoints verbosos |
| anti-duplication.md | 16KB | 570 | 54 code blocks, muitos "❌ WRONG" |
| anti-precocity.md | 16KB | 499 | 226 linhas de anti-patterns (45%) |
| essential-cognitive-modes.md | 8KB | 340 | Mais eficiente |

### Métricas de bloat

| Métrica | Total |
|---------|-------|
| Seções de exemplo/anti-pattern | 47 |
| Marcadores ❌/✅ | 184 |
| Code blocks | 266 |
| Few-shot examples (anti-babysitting) | 10 |
| Anti-patterns (anti-precocity) | 7 |

### Ironia detectada

Os specs violam o próprio `llm-conciseness.md`:
- Rule 3: "Scannable prose over bullet sprawl" → specs cheios de bullets
- Rule 4: "Max 2-3 sentences per chunk" → parágrafos enormes
- "Show code, don't describe" → muita descrição antes de código

---

## Prognóstico

**Redução potencial**: 50-60% (104KB → ~45KB)

### Cortes seguros (baixo risco)

| Seção | Economia | Risco |
|-------|----------|-------|
| Few-shot examples: 10 → 3 | ~300 linhas | Baixo |
| Anti-patterns: 7 → 3 | ~150 linhas | Baixo |
| "Validation Commands" sections | ~50 linhas | Nenhum |
| "For Humans" sections | ~80 linhas | Nenhum |
| Code blocks duplicados | ~100 linhas | Baixo |

### Preservar (essencial)

- Statements REGRA DOGMÁTICA (core de cada princípio)
- Vocabulário de detecção de modo
- HALT conditions (comprimir templates)
- 2-3 exemplos-chave por princípio
- Diagrama ASCII do fluxo de modos

---

## Estratégia de Implementação

### Fase 1: Cortes óbvios (104KB → ~70KB) → v0.2.0

- Remover examples 4-10 de anti-babysitting
- Remover anti-patterns 4-7 de anti-precocity
- Remover "Validation Commands" e "For Humans"

### Fase 2: Consolidação (70KB → ~50KB) → v0.3.0

- Mesclar templates HALT em um único
- Converter bullets em prosa escaneável
- Aplicar llm-conciseness aos próprios specs

### Fase 3: Refinamento (50KB → ~45KB) → v0.4.0

- Remover explicações redundantes
- Comprimir code blocks similares

---

## Estratégia de Validação

### Abordagem escolhida: Validação Funcional com Agent SDK

Usar Claude Agent SDK para executar bateria de testes funcionais que validam cada princípio.

### Fluxo de validação

```
1. Definir casos de teste em YAML
2. Rodar baseline (v0.1.0)
3. Salvar respostas e análise
4. Aplicar fase de redução
5. Rodar testes na nova versão
6. Comparar com baseline
7. Calcular % degradação
8. Gerar report
```

### Estrutura de dados

```
data/
├── test-cases/
│   └── functional-tests.yaml    # Casos de teste
├── versions/
│   ├── 0.1.0/                   # Baseline
│   │   ├── responses.yaml
│   │   └── analysis.yaml
│   ├── 0.2.0/                   # Fase 1
│   ├── 0.3.0/                   # Fase 2
│   └── 0.4.0/                   # Fase 3
├── comparisons/
│   ├── 0.1.0-0.2.0/
│   ├── 0.1.0-0.3.0/
│   └── 0.1.0-0.4.0/
└── reports/
    ├── phase-1-report.md
    ├── phase-2-report.md
    └── phase-3-report.md
```

### Critérios de sucesso

- Degradação < 5%: Aceitável
- Degradação 5-10%: Revisar mudanças
- Degradação > 10%: Reverter fase

---

## Referências

- Agent SDK: https://github.com/anthropics/claude-agent-sdk-python
- Docs: https://platform.claude.com/docs/en/agent-sdk/overview
