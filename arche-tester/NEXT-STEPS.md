# Arché Tester - Próximos Passos

## Pendente

### 1. Testes com Codebase Real

**Problema atual**: Testes rodam contra o próprio arche que não tem auth, users, etc.

**Solução**: Criar contexto simulado ou apontar para codebase real durante testes.

---

## Concluído

- [x] Estrutura do projeto arche-tester
- [x] Modelos Pydantic (TestCase, TestResponse, Analysis)
- [x] Agent com Claude Agent SDK
- [x] Runner de testes
- [x] Analyzer básico (keywords)
- [x] Comparator de versões
- [x] CLI (typer)
- [x] 26 casos de teste funcionais
- [x] Baseline v0.1.0 executado
- [x] Respostas e análise salvos em YAML
- [x] BaseAgent abstrato para múltiplos agentes
- [x] AnalyzerAgent com avaliação semântica LLM
- [x] CLI `--use-llm` flag para análise semântica

---

## Ordem de Prioridade

1. ~~**Analyzer LLM-based**~~ ✅ Implementado
2. **Fase 1 de redução** - Pode prosseguir com avaliação qualitativa
3. **Contexto simulado** - Nice to have
