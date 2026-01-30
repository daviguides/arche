# Plan: BaseAgent Implementation for arche-tester

**Status**: ✅ IMPLEMENTADO

## Objetivo

Criar `BaseAgent` abstrato para suportar múltiplos agentes no arche-tester.

---

## Estrutura de Diretórios

```
arche-tester/
├── arche_tester/
│   ├── agents/                   # NEW
│   │   ├── __init__.py
│   │   ├── base_agent.py        # Abstract base
│   │   └── arche_test_agent.py  # Refactored
│   ├── agent.py                  # Backward compat
│   └── runner.py                 # Update import
```

---

## Arquivos a Criar/Modificar

### 1. `agents/base_agent.py` (NEW)

**Elementos:**
- ABC com `@abstractmethod`
- Propriedade abstrata: `agent_name`
- Propriedade opcional: `allowed_tools` (default: Read, Glob, Grep)
- `_check_claude_cli()` - estático
- `connect()` / `disconnect()` - async
- `_call_agent(prompt)` - streaming response
- `_log()` - verbose logging
- Constante: `MAX_RETRIES = 3`
- Exception: `DependencyError`

### 2. `agents/arche_test_agent.py` (NEW)

**Herda de BaseAgent, adiciona:**
- `_arche_path` - específico do domínio
- `agent_name` → `"arche-test-agent"`
- `load_arche_principles()` - carrega contexto
- `run_test(prompt, context)` → `tuple[str, int]`

### 3. `agents/__init__.py` (NEW)

```python
from arche_tester.agents.base_agent import BaseAgent, DependencyError, MAX_RETRIES
from arche_tester.agents.arche_test_agent import ArcheTestAgent

__all__ = ["BaseAgent", "ArcheTestAgent", "DependencyError", "MAX_RETRIES"]
```

### 4. `agent.py` (MODIFY - backward compat)

```python
"""Backward compatibility - import from agents."""
from arche_tester.agents import ArcheTestAgent, BaseAgent, DependencyError, MAX_RETRIES

__all__ = ["ArcheTestAgent", "BaseAgent", "DependencyError", "MAX_RETRIES"]
```

### 5. `runner.py` (MODIFY)

```python
# Change from:
from arche_tester.agent import ArcheTestAgent

# To:
from arche_tester.agents import ArcheTestAgent
```

---

## Decisões de Design

| Decisão | Justificativa |
|---------|---------------|
| `agent_name` abstrato | Identifica agent em logs, segue padrão zen-review |
| `allowed_tools` override | Default cobre maioria, subclasses customizam |
| Sem `prompt_path` | arche-tester não usa prompts estáticos |
| `_arche_path` na subclasse | Específico do domínio |
| Backward compat | Zero breaking changes |

---

## Implementação

### Passo 1: Criar diretório agents
```bash
mkdir arche_tester/agents
```

### Passo 2: Criar base_agent.py
- Extrair funcionalidade comum de agent.py
- Adicionar ABC, abstract properties

### Passo 3: Criar arche_test_agent.py
- Mover ArcheTestAgent
- Implementar `agent_name`
- Manter métodos específicos

### Passo 4: Criar agents/__init__.py
- Exportar classes públicas

### Passo 5: Atualizar agent.py
- Converter para re-export

### Passo 6: Atualizar runner.py
- Mudar import path

---

## Verificação

```bash
# 1. Testes existentes
cd arche-tester && uv run pytest

# 2. Compatibilidade de import
python -c "from arche_tester.agent import ArcheTestAgent"
python -c "from arche_tester.agents import BaseAgent, ArcheTestAgent"

# 3. CLI
uv run arche-test run 0.1.0 --skip-cli-check
```

---

## Arquivos Críticos

| Arquivo | Ação |
|---------|------|
| `arche_tester/agents/base_agent.py` | Criar |
| `arche_tester/agents/arche_test_agent.py` | Criar |
| `arche_tester/agents/__init__.py` | Criar |
| `arche_tester/agent.py` | Modificar |
| `arche_tester/runner.py` | Modificar |

---

## Implementado: AnalyzerAgent

```python
# arche_tester/agents/analyzer_agent.py
class AnalyzerAgent(BaseAgent):
    """Agent para análise semântica de respostas via LLM."""

    @property
    def agent_name(self) -> str:
        return "analyzer-agent"

    async def analyze_response(
        self,
        response: str,
        must_behaviors: list[str],
        must_not_behaviors: list[str],
    ) -> list[BehaviorCheck]:
        ...
```

## Uso via CLI

```bash
# Análise com keywords (rápido, menos preciso)
uv run arche-test analyze 0.1.0

# Análise com LLM (lento, mais preciso)
uv run arche-test analyze 0.1.0 --use-llm
```
