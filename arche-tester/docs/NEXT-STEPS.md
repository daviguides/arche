# Arché Tester - Próximos Passos

## Pendente

### 1. Validar v0.3.0 com Nova Arquitetura
- Rodar testes completos com plugin configurado
- Comparar resultados com baseline
- Verificar estabilidade do fork_session

### 2. Fase 5 (Opcional)
- Simplificar `essential-cognitive-modes.md` se necessário
- Economia estimada: ~4.7 KB adicional

---

## Concluído

### Sessão 2025-01-31

- [x] **Refatorado SDK integration**: Removido `arche_path`, usa plugin local
- [x] **Configurado plugin**: `plugins=[{"type": "local", "path": ...}]`
- [x] **Adicionado setting_sources**: `["user", "project", "local"]`
- [x] **Corrigido skill loading**: `/arche:load-essential` funciona com plugin config
- [x] **Adicionado "Skill" aos allowed_tools**
- [x] **Documentado lições**: `docs/claude-agent-sdk-lessons.md`
- [x] **Fase 4 concluída**: Specs comprimidos 76-81%

### Sessão 2025-01-30

- [x] **Corrigido cálculo do pass_rate**: Adicionado `weighted_rate` que conta partial como 0.5
- [x] **Reescritos testes funcionais**: Prompts agora referenciam arquivos reais do mock project
- [x] **Criado mock project**: `data/mock-project/` com estrutura completa
- [x] **Implementado ambiente isolado**: fork_session + parallel execution
- [x] **Melhorada UX do CLI**: Rich panels com progresso
- [x] **Performance**: 5x mais rápido com fork_session parallel

### Anteriores

- [x] Estrutura do projeto arche-tester
- [x] Modelos Pydantic (TestCase, TestResponse, Analysis)
- [x] Agent com Claude Agent SDK
- [x] Runner de testes (parallel, fork_session)
- [x] Analyzer (keywords + LLM semântico)
- [x] Comparator de versões
- [x] CLI (typer + rich)
- [x] 22 casos de teste funcionais
- [x] BaseAgent abstrato para múltiplos agentes
- [x] AnalyzerAgent com avaliação semântica LLM

---

## Arquitetura Atual

```
arche-tester/
├── arche_tester/
│   ├── agents/
│   │   ├── base_agent.py       # SDK integration, plugin config
│   │   ├── arche_test_agent.py # Executa testes
│   │   └── analyzer_agent.py   # Análise semântica
│   ├── config.py               # Settings, ARCHE_PLUGIN_PATH
│   ├── analyzer.py             # Avalia conformidade
│   ├── comparator.py           # Compara versões
│   ├── display.py              # Componentes Rich
│   ├── models.py               # Pydantic schemas
│   ├── runner.py               # fork_session + parallel
│   └── cli.py                  # Comandos
├── data/
│   ├── mock-project/           # Template para testes
│   ├── test-cases/
│   │   └── functional-tests.yaml
│   └── versions/
│       ├── 0.1.0/              # Baseline
│       ├── 0.2.0/
│       └── 0.3.0/
└── docs/
    ├── claude-agent-sdk-lessons.md  # SDK lessons learned
    └── sessions/
```

---

## Comandos

```bash
# Executar testes (parallel com fork_session)
uv run arche-test run 0.3.0 -c 11

# Analisar respostas (LLM por padrão)
uv run arche-test analyze 0.3.0

# Comparar versões
uv run arche-test compare 0.1.0 0.3.0

# Report de fase
uv run arche-test report 1
```
