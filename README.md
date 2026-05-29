# Development Program AI Engineer

API REST de análise de compliance financeiro com RAG (Retrieval-Augmented Generation), construída como parte do programa de desenvolvimento interno da EY.

## Sobre o Projeto

O sistema simula um analista de compliance financeiro. Ele recebe uma recomendação de investimento, busca trechos relevantes da base de conhecimento oficial e usa um LLM (Azure OpenAI) para analisar se a recomendação está em conformidade com as políticas internas.

## Arquitetura

```
Cliente → POST /analyze
    → Busca chunks relevantes no ChromaDB
    → Re-ranking por relevância
    → Prompt enriquecido com contexto das políticas
    → Azure OpenAI analisa
    → Resposta com conformidade + fontes citadas
```

## Estrutura do Repositório

```
development-program-ai-engineer/
├── projects/
│   └── project/
│       ├── .env                          # Credenciais Azure OpenAI (não versionado)
│       ├── .gitignore
│       ├── Dockerfile
│       ├── README.md
│       ├── requirements.txt
│       ├── knowledge_base/
│       │   ├── analise_de_perfil_do_investidor.txt
│       │   ├── email_analise_cliente_01.txt
│       │   ├── manual_comunicacao_cliente_v1.0.txt
│       │   ├── politica_adequacao_investimento_v1.2.txt
│       │   └── politica_investimento_agressivo_v1.0.txt
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
│       │   └── services/
│       │       └── compliance_service.py
│       ├── tests/
│       │   ├── test_api.py
│       │   └── test_services.py
│       └── docs/
│           ├── architecture.md
│           ├── decisions.md
│           └── SDD.md
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
AZURE_DEPLOYMENT_NAME="seu-deployment"
```

### 3. Rodar a ingestão
```bash
python projects/project/src/rag/ingestion.py
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
  "reason": "A recomendação não está em conformidade com as políticas...",
  "mentioned_products": ["politica_adequacao_investimento_v1.2.txt"],
  "source_documents": ["politica_adequacao_investimento_v1.2.txt"]
}
```

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

## Tecnologias
| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework da API |
| Pydantic | Validação de dados |
| Azure OpenAI | LLM para análise de compliance |
| ChromaDB | Banco de dados vetorial local |
| Instructor | Extração de dados estruturados |
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
