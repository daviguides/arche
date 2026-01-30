# Session Log: 2025-01-30 - Baseline Fix & Mock Project

## Problema Inicial

O baseline estava retornando **50% pass_rate** quando deveria estar mais alto. Investigação revelou dois problemas:

### 1. Cálculo Incorreto do Pass Rate

```python
# Antes: ignorava "partial"
pass_rate = passed / total  # 13/26 = 50%

# Depois: weighted_rate considera partial
weighted_rate = (passed + partial * 0.5) / total  # (13 + 12*0.5)/26 = 73%
```

### 2. Testes Incompatíveis com o Projeto

Os testes foram escritos para um projeto hipotético com:
- Authentication module
- `src/` directory
- API endpoints
- User registration

Mas o Arché é apenas specs markdown + CLI tester. O LLM corretamente:
1. Pesquisava antes de agir ✓
2. Reportava que não existiam ✓
3. Não criava código desnecessário ✓

Resultado: comportamento correto marcado como "partial" ou "fail".

---

## Soluções Implementadas

### 1. Novo Campo `weighted_rate`

**Arquivos modificados:**
- `arche_tester/models.py` - Adicionado campo
- `arche_tester/analyzer.py` - Cálculo em ambas funções

```python
class VersionAnalysis(BaseModel):
    pass_rate: float      # strict: apenas passed
    weighted_rate: float  # passed + partial*0.5
```

### 2. Mock Project

Criado `data/mock-project/` com estrutura completa:

```
mock-project/
├── pyproject.toml
├── src/
│   ├── models.py    # User, Product, Order + validate_email
│   ├── utils.py     # Helpers + validate_email (duplicado!)
│   ├── api.py       # CRUD endpoints com error handling
│   └── auth.py      # Sessions, login, permissions
├── tests/
│   └── test_models.py
├── config/
│   └── settings.yaml
└── docs/
    └── README.md
```

**Destaques:**
- `validate_email` duplicado intencionalmente (teste AD-002)
- TODOs em models.py (teste CP-002)
- API com error handling real (testes AP-003, AB-003)

### 3. Ambiente Isolado por Teste

**Arquivo:** `arche_tester/runner.py`

```python
def _create_test_environment(self) -> Path:
    test_id = str(uuid.uuid4())[:8]
    test_dir = self._temp_base / f"test-{test_id}"
    shutil.copytree(self._mock_project_path, test_dir)
    return test_dir

def _cleanup_test_environment(self, test_dir: Path) -> None:
    shutil.rmtree(test_dir)
```

Fluxo:
1. Copia mock → `/tmp/arche-test/test-{uuid}/`
2. Agente roda com `cwd` no temp
3. Pode criar/modificar arquivos
4. Cleanup após teste

### 4. UX Melhorada com Rich

**Arquivo:** `arche_tester/display.py`

Componentes criados:
- `create_test_panel()` - Painel com detalhes do teste
- `create_analysis_summary()` - Sumário colorido
- `create_results_table()` - Tabela de resultados
- `print_header()`, `print_step()`, `print_success()`

Saída agora mostra:
- Progresso percentual [5/26] 19%
- Principle, Mode, Description
- Prompt (truncado)
- Response preview
- Status com cores (✓ PASS, ✗ FAIL, ◐ PARTIAL)

### 5. LLM como Padrão

**Arquivo:** `arche_tester/cli.py`

```python
use_llm: bool = typer.Option(
    True,  # Era False
    "--use-llm/--no-llm",
    "-l/-L",
)
```

### 6. Status SKIPPED

**Arquivo:** `arche_tester/models.py`

```python
class Conformity(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    SKIPPED = "skipped"  # Novo
```

Testes SKIPPED são excluídos do cálculo de pass_rate.

### 7. Testes Reescritos

**Arquivo:** `data/test-cases/functional-tests.yaml`

Versão 2.0.0 com prompts que referenciam o mock project:
- PE-001: "Create a new logging module at src/logging.py"
- AD-002: "Create an email validation function" (deve detectar duplicação)
- AB-001: "Add docstrings to all classes in src/models.py"
- etc.

---

## Arquivos Criados/Modificados

### Criados
- `arche_tester/display.py`
- `data/mock-project/` (8 arquivos)
- `docs/sessions/2025-01-30-baseline-fix.md`

### Modificados
- `arche_tester/models.py` - weighted_rate, SKIPPED
- `arche_tester/analyzer.py` - cálculo, display
- `arche_tester/runner.py` - ambiente isolado
- `arche_tester/cli.py` - LLM padrão, validação
- `arche_tester/agents/arche_test_agent.py` - cwd customizado
- `data/test-cases/functional-tests.yaml` - v2.0.0
- `NEXT-STEPS.md` - atualizado

---

## Próximos Passos

1. Executar baseline com mock project
2. Verificar weighted_rate > 80%
3. Ajustar testes se necessário
4. Iniciar Fase 1 de redução de specs
