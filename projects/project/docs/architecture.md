```markdown
# Arquitetura - Compliance Checker API

## Visão Geral
O Compliance Checker é um sistema completo de análise de compliance financeiro com três camadas: API REST, pipeline RAG e agente autônomo. As análises são baseadas em documentos oficiais de política, garantindo rastreabilidade e auditabilidade.

## Fluxo Completo do Sistema

### Via API (modo interativo)
```
Cliente → POST /analyze
    → Busca semântica no banco vetorial (Azure Embeddings)
    → Re-ranking por relevância
    → Prompt enriquecido com contexto das políticas
    → Azure OpenAI (gpt-4o)
    → AnalysisResponse com fontes e chunk IDs
```

### Via Agente (modo autônomo)
```
data/input/recomendacao.txt
    → read_document
    → analyze_document (RAG + LLM)
    → decide_action (is_compliant?)
        → approved: data/output/approved/
        → rejected: data/output/rejected_for_review/ + alerta em data/logs/

```

## Pipeline de Ingestão
```
knowledge_base/*.txt + *.pdf
    → load_documents
    → chunk_text (500 chars, overlap 50)
    → get_embedding (Azure text-embedding-ada-002)
    → salva embeddings.npy + chunks.pkl
```

## Grafo de Estados do Agente (LangGraph)
```
(START)
    → read_document
    → analyze_document
    → [decide_action]
        → "approve"       → approve_document → (END)
        → "reject"        → reject_document  → (END)
        → "handle_error"  → handle_error     → (END)
```

## Camadas

### API Layer (`src/api/`)
Recebe e valida requisições HTTP. Schemas Pydantic em `src/api/schemas/analysis.py` definem os contratos de dados incluindo `source_documents`, `source_chunk_id` e `rerank_score`.

### Service Layer (`src/services/`)
Orquestra o fluxo RAG: recupera chunks, aplica re-ranking, monta prompt enriquecido e chama o LLM.

### RAG Layer (`src/rag/`)
- `ingestion.py` — lê documentos, divide em chunks e gera embeddings semânticos via Azure
- `retrieval.py` — busca por similaridade cosseno usando embeddings pré-calculados
- `reranker.py` — re-ranking por palavras-chave em comum com a query

### Agents Layer (`src/agents/`)
- `compliance_agent.py` — grafo LangGraph com os nós de processamento
- `monitor.py` — monitora `data/input/` com watchdog e dispara o agente
- `metrics.py` — registra e calcula métricas de automação

### Core Layer (`src/core/`)
Cliente Azure OpenAI (`llm_client.py`) e exceções customizadas (`exceptions.py`).

## Componentes
| Componente | Responsabilidade |
|---|---|
| `main.py` | Endpoints da API + endpoints do agente |
| `api/schemas/analysis.py` | Contratos de request e response |
| `services/compliance_service.py` | Orquestra RAG + LLM |
| `rag/ingestion.py` | Pipeline de ingestão de documentos |
| `rag/retrieval.py` | Busca semântica por similaridade cosseno |
| `rag/reranker.py` | Re-ranking por palavras-chave |
| `agents/compliance_agent.py` | Agente autônomo LangGraph |
| `agents/monitor.py` | Monitor de pasta com watchdog |
| `agents/metrics.py` | Métricas de automação |
| `core/llm_client.py` | Conexão com Azure OpenAI |
| `core/exceptions.py` | Exceções customizadas |

## Base de Conhecimento
| Documento | Conteúdo |
|---|---|
| `analise_de_perfil_do_investidor.txt` | Perfis de risco dos clientes |
| `email_analise_cliente_01.txt` | Template de análise de cliente |
| `manual_comunicacao_cliente_v1.0.txt` | Regras de comunicação |
| `politica_adequacao_investimento_v1.2.txt` | Política de adequação de produtos |
| `politica_investimento_agressivo_v1.0.txt` | Política para perfil agressivo |
| `anbima_codigo_distribuicao_produtos_Investimento.pdf` | Código ANBIMA de distribuição |
```

---
