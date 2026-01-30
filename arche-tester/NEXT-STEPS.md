# Arché Tester - Próximos Passos

## Pendente

### 1. Executar Baseline com Mock Project
- Rodar `uv run arche-test run 0.1.0` com o novo mock project
- Rodar `uv run arche-test analyze 0.1.0` para avaliar conformidade
- Verificar se weighted_rate > 80%

### 2. Ajustar Testes Conforme Resultados
- Revisar testes que ainda falham
- Ajustar prompts ou expected behaviors se necessário
- Garantir que testes são justos e verificáveis

### 3. Fase 1 de Redução de Specs
- Aplicar reduções planejadas em `size-reduction-plan.md`
- Rodar testes na versão 0.2.0
- Comparar com baseline para verificar degradação < 5%

---

## Concluído

### Sessão 2025-01-30

- [x] **Corrigido cálculo do pass_rate**: Adicionado `weighted_rate` que conta partial como 0.5
- [x] **Reescritos testes funcionais**: Prompts agora referenciam arquivos reais do mock project
- [x] **Criado mock project**: `data/mock-project/` com estrutura completa (models, api, auth, utils, tests, config, docs)
- [x] **Implementado ambiente isolado**: Cada teste copia mock para `/tmp/arche-test/test-{uuid}/` e limpa após
- [x] **Melhorada UX do CLI**: Rich panels com progresso, detalhes do teste, e resposta
- [x] **LLM como padrão**: `--use-llm` agora é default, `--no-llm` para keyword matching
- [x] **Adicionado SKIPPED status**: Para testes que não podem ser avaliados
- [x] **Validação de entrada no CLI**: Verifica se version dir e responses.yaml existem

### Anteriores

- [x] Estrutura do projeto arche-tester
- [x] Modelos Pydantic (TestCase, TestResponse, Analysis)
- [x] Agent com Claude Agent SDK
- [x] Runner de testes
- [x] Analyzer (keywords + LLM semântico)
- [x] Comparator de versões
- [x] CLI (typer + rich)
- [x] 26 casos de teste funcionais
- [x] BaseAgent abstrato para múltiplos agentes
- [x] AnalyzerAgent com avaliação semântica LLM

---

## Arquitetura Atual

```
arche-tester/
├── arche_tester/
│   ├── agents/
│   │   ├── base_agent.py      # Abstração comum
│   │   ├── arche_test_agent.py # Executa testes
│   │   └── analyzer_agent.py   # Análise semântica
│   ├── analyzer.py            # Avalia conformidade
│   ├── comparator.py          # Compara versões
│   ├── display.py             # Componentes Rich
│   ├── models.py              # Pydantic schemas
│   ├── runner.py              # Executa suite
│   └── cli.py                 # Comandos
├── data/
│   ├── mock-project/          # Template para testes
│   ├── test-cases/
│   │   └── functional-tests.yaml
│   └── versions/
│       └── 0.1.0/
│           ├── responses.yaml
│           └── analysis.yaml
```

---

## Comandos

```bash
# Executar testes (usa mock project isolado)
uv run arche-test run 0.1.0

# Analisar respostas (LLM por padrão)
uv run arche-test analyze 0.1.0

# Analisar com keyword matching (rápido)
uv run arche-test analyze 0.1.0 --no-llm

# Baseline completo (run + analyze)
uv run arche-test baseline

# Comparar versões
uv run arche-test compare 0.1.0 0.2.0
```
