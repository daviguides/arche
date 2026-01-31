# Session: SDK Plugin Refactor

**Data**: 2025-01-31
**Objetivo**: Corrigir integração do Claude Agent SDK com plugin Arché

---

## Problema

O arche-tester usava `arche_path` para carregar princípios via file path. Isso causava:
1. Confusão entre path do bundle e cwd do workspace
2. Fallback perigoso `arche_path.parent` que enviava agente para diretório errado
3. Diretórios de teste criados no lugar errado (`arche/test-CP-001/` ao invés de `/tmp/arche-test/`)

---

## Descobertas

### 1. SDK não carrega plugins automaticamente

Plugins em `~/.claude/` não são visíveis para o SDK. Precisam ser configurados:

```python
plugins=[{"type": "local", "path": str(PLUGIN_PATH)}]
```

### 2. Skills requerem "Skill" em allowed_tools

```python
allowed_tools=["Skill", "Read", "Glob", "Grep"]
```

### 3. setting_sources para carregar settings

```python
setting_sources=["user", "project", "local"]
```

---

## Mudanças

| Arquivo | Mudança |
|---------|---------|
| config.py | + `ARCHE_PLUGIN_PATH`, + `ClaudeOptions`, - `arche_path` |
| base_agent.py | + `plugins`, + `setting_sources` |
| arche_test_agent.py | Usa `/arche:load-essential` |
| analyzer_agent.py | Usa `/arche:load-essential` |
| cli.py | Remove `--arche-path` option |
| runner.py | Remove `arche_path` param |

---

## Resultado

- `/arche:load-essential` funciona corretamente
- Testes executam no diretório correto (`/tmp/arche-test/`)
- Documentação criada: `docs/claude-agent-sdk-lessons.md`

---

## Commits

- `refactor(arche-tester): remove arche_path, use plugin command`
- `fix(arche-tester): add arche plugin to SDK options`
- `fix(config): use absolute path for arche plugin from home`
- `docs: add Claude Agent SDK lessons learned`
