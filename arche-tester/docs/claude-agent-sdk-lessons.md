# Claude Agent SDK - Lições Aprendidas

Documentação das descobertas ao integrar o Claude Agent SDK no arche-tester.

---

## 1. Plugins Locais

O SDK **não carrega automaticamente** plugins instalados em `~/.claude/`. Plugins devem ser configurados explicitamente:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # ...
    plugins=[{"type": "local", "path": "/path/to/plugin"}],
)
```

**Estrutura do plugin config:**
```python
class SdkPluginConfig(TypedDict):
    type: Literal["local"]
    path: str
```

---

## 2. Skills vs File Paths

Skills (`/plugin:skill-name`) **funcionam** quando o plugin está configurado via `plugins` option.

```python
# Funciona (com plugin configurado)
await agent._call_agent("/arche:load-essential")

# Alternativa sem plugin
await agent._call_agent(f"Load principles from: {absolute_path}")
```

---

## 3. Setting Sources

Para carregar settings do usuário/projeto/local:

```python
options = ClaudeAgentOptions(
    setting_sources=["user", "project", "local"],
)
```

---

## 4. Fork Session e CWD

Quando `fork_session=True`:
- O `cwd` é **herdado** da sessão base
- Não pode ser alterado no fork
- Todos os forks compartilham o mesmo `cwd`

**Implicação:** Criar subdiretórios para isolamento de testes.

```python
# Base session
base_agent = Agent(cwd="/tmp/arche-test")

# Forked session (mesmo cwd)
forked_agent = Agent(
    cwd="/tmp/arche-test",  # Ignorado, herda da base
    resume=base_session_id,
    fork_session=True,
)

# Isolamento via prompt
prompt = f"Work in the `test-{test_id}/` directory.\n\n{actual_prompt}"
```

---

## 5. Allowed Tools

Ferramentas devem ser explicitamente listadas:

```python
allowed_tools=["Skill", "Read", "Glob", "Grep", "Write", "Edit", "Bash"]
```

**Nota:** `"Skill"` é necessário para invocar skills de plugins.

---

## 6. Erro "Unknown skill"

```
result='Unknown skill: plugin:skill-name'
```

**Causas:**
1. Plugin não configurado em `plugins` option
2. Path do plugin incorreto
3. Skill não existe no plugin

**Solução:** Verificar `plugins` config com path absoluto correto.

---

## 7. Erro "No text in agent response"

```python
if not text_blocks:
    raise ValueError("No text in agent response")
```

**Causas:**
1. Skill retornou erro (ver `ResultMessage.result`)
2. Processo interrompido (standby, SIGTERM)
3. Timeout

**Debug:** Verificar `ResultMessage` para detalhes do erro.

---

## 8. Configuração Completa

```python
from pathlib import Path
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

PLUGIN_PATH = Path.home() / "work" / "sources" / "gradients" / "arche"

options = ClaudeAgentOptions(
    model="sonnet",
    allowed_tools=["Skill", "Read", "Glob", "Grep"],
    permission_mode="bypassPermissions",
    include_partial_messages=True,
    cwd="/tmp/workspace",
    setting_sources=["user", "project", "local"],
    plugins=[{"type": "local", "path": str(PLUGIN_PATH)}],
)

client = ClaudeSDKClient(options=options)
await client.connect()
await client.query("/arche:load-essential")
```

---

## Referências

- https://platform.claude.com/docs/en/agent-sdk/skills
- https://platform.claude.com/docs/en/agent-sdk/slash-commands
- https://platform.claude.com/docs/en/agent-sdk/plugins
