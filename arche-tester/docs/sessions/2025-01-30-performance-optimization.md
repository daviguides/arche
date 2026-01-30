# Session Log: 2025-01-30 - Performance Optimization

## Problema Inicial

Bateria de testes funcional muito lenta: **13m 29s** (809,118 ms) para 26 testes.

**Causa:** Cada teste fazia 2 chamadas LLM:
1. `load_arche_principles()` - carregar princípios
2. `run_test()` - executar o teste

Total: 52 chamadas LLM (26 testes × 2)

---

## Otimizações Implementadas

### 1. Configuração de Modelo por Agente

**Arquivo:** `arche_tester/config.py` (novo)

```python
class ClaudeModel(StrEnum):
    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"

class TestAgentSettings(BaseSettings):
    model: ClaudeModel = ClaudeModel.SONNET
    permission_mode: str = "bypassPermissions"

class AnalyzerAgentSettings(BaseSettings):
    model: ClaudeModel = ClaudeModel.HAIKU  # Mais rápido para classificação
    permission_mode: str = "bypassPermissions"
```

**Impacto:** Analyzer usa Haiku (mais rápido), testes usam Sonnet.

### 2. Modo bypassPermissions

**Arquivos:** `config.py`, `base_agent.py`

Alterado de `acceptEdits` para `bypassPermissions` - sem confirmações durante execução.

### 3. Prompts Simplificados

**Arquivo:** `data/test-cases/functional-tests.yaml` (v2.2.0)

| Antes | Depois |
|-------|--------|
| 26 testes | 22 testes |
| Prompts longos | Prompts curtos |
| "Add docstrings to all classes in src/models.py: User, Product, Order, OrderItem" | "Add docstring to User class" |

**Impacto:** Respostas mais curtas, menos tokens.

### 4. Testes Ordenados por Modo Cognitivo

```yaml
# Ordem: EXPLORING → RESEARCHING → PLANNING → IMPLEMENTING
test_cases:
  # EXPLORING (4 testes)
  - id: AP-001
  - id: AP-005
  - id: LC-001
  - id: MT-001

  # RESEARCHING (6 testes)
  - id: PE-003
  - id: AD-003
  ...

  # PLANNING (2 testes)
  - id: AP-004
  - id: MT-003

  # IMPLEMENTING (10 testes)
  - id: PE-001
  ...
```

### 5. fork_session Optimization

**Problema inicial:** Fork não funcionava porque mudava o `cwd` entre sessões.

**Solução (Opção C):** Workspace fixo com reset entre testes.

**Arquivo:** `arche_tester/runner.py`

```python
# Antes: diretório único por teste
test_dir = self._temp_base / f"test-{uuid}"  # /tmp/arche-test/test-abc123/

# Depois: workspace fixo, reset entre testes
self._workspace = self._temp_base / "workspace"  # /tmp/arche-test/workspace/

def _setup_workspace(self) -> Path:
    shutil.copytree(self._mock_project_path, self._workspace)
    return self._workspace

def _reset_workspace(self) -> None:
    shutil.rmtree(self._workspace)
    shutil.copytree(self._mock_project_path, self._workspace)
```

**Fluxo otimizado:**
```
1. Setup workspace com mock-project
2. Criar sessão base + load_principles (1x)
3. Para cada teste:
   a. Reset workspace (fresh copy)
   b. Fork da sessão base (mesmo cwd!)
   c. Rodar teste
4. Cleanup workspace
```

**Impacto:** De 52 chamadas LLM para 23 (1 load + 22 testes).

### 6. Tempo Total no Output

**Arquivos:** `runner.py`, `analyzer.py`, `models.py`

```python
# models.py
class TestResponses(BaseModel):
    total_duration_ms: int | None = None

# runner.py
start_time = time.time()
# ... testes ...
total_duration_ms = int((time.time() - start_time) * 1000)
print(f"Total time: {minutes}m {seconds}s")
```

---

## Comparação de Performance

| Métrica | Baseline | Otimizado | Redução |
|---------|----------|-----------|---------|
| Testes | 26 | 22 | 15% |
| Chamadas LLM | 52 | 23 | 56% |
| Tempo estimado | 13m 29s | ~5-6m | ~55% |

---

## Arquivos Criados/Modificados

### Criados
- `arche_tester/config.py` - Configuração de modelos
- `data/versions/0.1.0/responses-baseline-no-optimization.yaml` - Backup

### Modificados
- `arche_tester/agents/base_agent.py` - resume, fork_session, session_id
- `arche_tester/agents/arche_test_agent.py` - Suporte a fork
- `arche_tester/agents/analyzer_agent.py` - Usa settings
- `arche_tester/runner.py` - Workspace fixo, fork_session
- `arche_tester/analyzer.py` - Tempo total
- `arche_tester/models.py` - total_duration_ms
- `arche_tester/cli.py` - Mantido
- `data/test-cases/functional-tests.yaml` - v2.2.0, prompts simples
- `pyproject.toml` - pydantic-settings
- `.gitignore` - __pycache__

---

## Commits

```
feat(arche-tester): add model configuration per agent
feat(arche-tester): use bypassPermissions mode for agents
perf(arche-tester): simplify test prompts for faster execution
feat(arche-tester): show and save total duration in run command
feat(arche-tester): fix fork_session with fixed workspace
```

---

## Próximos Passos

1. ✅ Rodar bateria otimizada
2. Comparar tempo real vs baseline (13m 29s)
3. Validar que resultados são consistentes
4. Documentar ganho final
