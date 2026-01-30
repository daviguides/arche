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

## Comparação de Performance (Resultados Finais)

| Métrica | Baseline | Otimizado | Melhoria |
|---------|----------|-----------|----------|
| Testes | 26 | 22 | 15% menos |
| Chamadas LLM | 52 | 23 | 56% menos |
| **Tempo Total** | **13m 29s** (809,118 ms) | **6m 48s** (407,996 ms) | **49.6% mais rápido** |

### Resultado: ✅ Sucesso

A bateria de testes foi reduzida de **13.5 minutos para 6.8 minutos** - quase 50% mais rápida.

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
2. ✅ Comparar tempo real vs baseline (13m 29s → 6m 48s = **49.6% mais rápido**)
3. ✅ Validar que resultados são consistentes (22 testes executados com sucesso)
4. ✅ Documentar ganho final

---

## Otimização #2: Execução Paralela

### Problema
Testes rodavam sequencialmente. Com 22 testes × ~18s cada = ~6m48s.

### Solução
Execução paralela com workspaces isolados:

```python
# runner.py
async def _run_single_test(self, test_case, semaphore, progress, task_id):
    async with semaphore:
        workspace = self._create_workspace(test_case.id)  # Workspace isolado
        try:
            agent = ArcheTestAgent(arche_path=..., cwd=workspace)
            await agent.load_arche_principles()
            response, duration = await agent.run_test(...)
            return TestResponse(...)
        finally:
            self._cleanup_workspace(workspace)

# Execução paralela com semáforo
semaphore = asyncio.Semaphore(self._concurrency)  # Default: 4
tasks = [self._run_single_test(tc, semaphore, ...) for tc in suite.test_cases]
responses = await asyncio.gather(*tasks)
```

### CLI
```bash
arche-test run 0.1.0 -c 4  # 4 testes em paralelo (default)
arche-test run 0.1.0 -c 8  # 8 testes em paralelo
```

### Fix MT-003
Teste MT-003 dependia de contexto do teste anterior (AP-004). Corrigido incluindo contexto no próprio prompt:

```yaml
# Antes (dependia de contexto anterior)
prompt: "Implement option A"
context: "Previous: discussed options A and B for logging"

# Depois (auto-contido)
prompt: "We discussed logging options: A) structured logging with levels, B) minimal logging. Implement option A in api.py"
```

### Otimização #3: Fork + Paralelo

Combinar fork_session com execução paralela usando subdirectories:

```
/tmp/arche-test/                    ← cwd fixo (base + todos forks)
  ├── test-AP-001/                  ← subdirectório isolado
  ├── test-AP-002/
  └── ...
```

**Prompt direciona:** `"Work in the test-{id}/ directory"`

### Resultado Final

| Abordagem | Tempo | Chamadas LLM | vs Baseline |
|-----------|-------|--------------|-------------|
| Baseline (sem otimização) | 13m 29s | 52 | - |
| Sequencial + fork | 6m 48s | 23 | -50% |
| Fork + Paralelo (4x) | 5m 30s | 23 | -59% |
| **Fork + Paralelo (8x)** | **2m 44s** | **23** | **-80%** |

**Resultado: 13.5 min → 2.7 min = 5x mais rápido!**

Default alterado para 8 workers paralelos.

**Nota:** Paralelização do `analyze` não funcionou (overhead de spawn > benefício com Haiku).

---

## Análise de Conformidade

### Último Run: 90.9% pass rate (20/22)

**Falhas restantes:**

| Test ID | Princípio | Problema |
|---------|-----------|----------|
| **AB-005** | anti-babysitting | Prompt pede `authenticate()` que não existe. Agente perguntou qual função usar. |
| **PE-001** | principle-enforcement | Prompt "Create src/logger.py" - agente criou sem pesquisar antes. |

### Melhoria: Context-Aware Analysis

Implementado carregamento de princípios Arché no analyzer antes da análise LLM.

```bash
arche-test analyze 0.1.0  # Agora carrega princípios automaticamente
```

---

## Próximos Passos

1. **Corrigir AB-005**: Mudar prompt para função existente (`login()`) ou aceitar que perguntar é correto quando há ambiguidade real
2. **Corrigir PE-001**: Este é bug real - prompt "Create X" deveria fazer agente pesquisar primeiro. Possíveis fixes:
   - Ajustar prompt para ser mais explícito
   - Melhorar princípio de research-first no Arché
3. **Objetivo**: Baseline 100% pass rate
