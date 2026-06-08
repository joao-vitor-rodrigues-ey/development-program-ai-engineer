# Development Program AI Engineer

API REST de análise de compliance financeiro com RAG (Retrieval-Augmented Generation) e agente autônomo, construída como parte do programa de desenvolvimento interno da EY.

## Sobre o Projeto

O sistema simula um analista de compliance financeiro. Ele recebe uma recomendação de investimento, busca trechos relevantes da base de conhecimento oficial usando embeddings semânticos do Azure OpenAI, e usa um LLM para analisar se a recomendação está em conformidade com as políticas internas.

## Arquitetura

### Via API (modo interativo)
```
Cliente → POST /analyze
    → Busca semântica (Azure Embeddings)
    → Re-ranking por relevância
    → Prompt enriquecido com contexto
    → Azure OpenAI (gpt-4o)
    → Resposta com conformidade + fontes citadas
```

### Via Agente (modo autônomo)
```
data/input/recomendacao.txt
    → Leitura do documento
    → Análise RAG + LLM
    → Decisão (compliant?)
        → Sim: data/output/approved/
        → Não: data/output/rejected_for_review/ + alerta
```

## Estrutura do Repositório

```
development-program-ai-engineer/
├── projects/
│   └── project/
│       ├── .env
│       ├── .gitignore
│       ├── Dockerfile
│       ├── README.md
│       ├── requirements.txt
│       ├── knowledge_base/
│       │   ├── analise_de_perfil_do_investidor.txt
│       │   ├── email_analise_cliente_01.txt
│       │   ├── manual_comunicacao_cliente_v1.0.txt
│       │   ├── politica_adequacao_investimento_v1.2.txt
│       │   ├── politica_investimento_agressivo_v1.0.txt
│       │   └── anbima_codigo_distribuicao_produtos_Investimento.pdf
│       ├── data/
│       │   ├── input/               ← coloca arquivos aqui para o agente processar
│       │   ├── output/
│       │   │   ├── approved/        ← documentos conformes
│       │   │   └── rejected_for_review/  ← documentos para revisão
│       │   └── logs/                ← logs e métricas do agente
│       ├── notebooks/
│       │   └── rag_evaluation.ipynb
│       ├── src/
│       │   ├── main.py
│       │   ├── api/schemas/analysis.py
│       │   ├── core/
│       │   │   ├── llm_client.py
│       │   │   └── exceptions.py
│       │   ├── rag/
│       │   │   ├── ingestion.py
│       │   │   ├── retrieval.py
│       │   │   └── reranker.py
│       │   ├── agents/
│       │   │   ├── compliance_agent.py
│       │   │   ├── monitor.py
│       │   │   └── metrics.py
│       │   └── services/
│       │       └── compliance_service.py
│       └── tests/
│           ├── test_api.py
│           └── test_services.py
└── apresentation/
```

## Como Rodar

### Pré-requisitos
- Python 3.11
- Docker
- Credenciais Azure OpenAI no `.env`

### 1. Instalar dependências
```bash
cd projects/project
pip install -r requirements.txt
```

### 2. Configurar o `.env`
```
AZURE_OPENAI_ENDPOINT="seu-endpoint"
AZURE_OPENAI_KEY="sua-chave"
AZURE_OPENAI_API_VERSION="2024-06-01"
AZURE_DEPLOYMENT_NAME="gpt-4o"
AZURE_EMBEDDING_DEPLOYMENT="text-embedding-ada-002"
```

### 3. Rodar a ingestão
```bash
python src/rag/ingestion.py
```

### 4. Subir a API
```bash
cd projects/project
uvicorn src.main:app --reload
```

Acesse a documentação em: http://127.0.0.1:8000/docs

### 5. Com Docker
```bash
cd projects/project
docker build -t compliance-checker .
docker run -p 8000:8000 --env-file .env compliance-checker
```

## Endpoints

### GET /health
```json
{"status": "ok"}
```

### POST /analyze
**Request:**
```json
{
  "text_to_analyze": "Recomendo investir em ações de alto risco para perfil conservador."
}
```

**Response:**
```json
{
  "is_compliant": false,
  "reason": "A recomendação não está em conformidade...",
  "mentioned_products": ["ações de alto risco"],
  "source_documents": ["politica_adequacao_investimento_v1.2.txt"],
  "source_chunk_id": [0, 2, 1],
  "rerank_score": [6, 5, 4]
}
```

### POST /agent/process/{filename}
Dispara o agente para processar um arquivo da pasta `data/input/`.

### GET /agent/metrics
Retorna métricas de automação do agente.

## Agente Autônomo

### Processar um arquivo específico
```bash
python -c "from src.agents.compliance_agent import run_agent; run_agent('recomendacao.txt')"
```

### Iniciar o monitor automático
```bash
python src/agents/monitor.py
```

### Fluxo do agente (LangGraph)
```
(START) → read_document → analyze_document → [decide_action]
    → approve  → approve_document  → (END)
    → reject   → reject_document   → (END)
    → error    → handle_error      → (END)
```

## Indicador de Automação

| Métrica | Antes | Depois |
|---|---|---|
| Processo de análise | 100% manual | 95% automatizado |
| Tempo por recomendação | ~15 min | ~30 segundos |
| Capacidade diária | ~30 análises | ~960 análises |
| Intervenção humana | 100% dos casos | apenas casos rejeitados |

Estimativa: redução de **~6 horas de trabalho manual por dia** para equipes que processam 30 recomendações diárias.

## Testes
```bash
cd projects/project
python -m pytest tests/ -v
```

## Avaliação do Re-ranking
```bash
cd projects/project
python -m jupyter notebook
```

Abre o notebook `notebooks/rag_evaluation.ipynb`.

**Resultados obtidos com embedding semântico Azure:**
- MRR antes do re-ranking: 0.444
- MRR depois do re-ranking: 0.833
- Melhoria: **87.5%**

## Tecnologias
| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework da API |
| Pydantic | Validação de dados |
| Azure OpenAI (gpt-4o) | LLM para análise de compliance |
| Azure OpenAI (text-embedding-ada-002) | Embeddings semânticos |
| ChromaDB | Banco de dados vetorial (ingestão) |
| LangGraph | Orquestração do agente autônomo |
| watchdog | Monitoramento de pasta |
| pytest | Testes automatizados |
| Docker | Containerização |

## Padrão de Commits
Seguimos o padrão Conventional Commits:
- `feat` — nova funcionalidade
- `fix` — correção de bug
- `docs` — documentação
- `refactor` — refatoração
- `test` — testes
- `chore` — tarefas de manutenção
