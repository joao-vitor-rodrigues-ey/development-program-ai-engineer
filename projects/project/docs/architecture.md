# Arquitetura

*Esta documentação descreverá a arquitetura de alto nível da solução.*
## Visão Geral 
O compliance Checker é uma API REST que recebe recomendações de investimento e utiliza um LLM (Azure OpenAI) para analisar se estão em conformidade com as politicas de investimento 

## Fluxo de dados
Cliente → POST /analyze -> main.py -> compliance_service.py 
-> retrieve() busca chunks no ChromaDB
-> simple_rerank() reordena por relevância
-> prompt enriquecido com contexto
-> AzureModel (LLM)
-> AnalysisResponse com fontes
-> Cliente

## Pipeline de ingestão
knowledge_base/*.txt -> ingestion.py -> chunking-> embeddings -> ChromaDB

## Camadas

## API Layer (`src/api/`)
Recebe e valida as requisições HTTP. Os schemas Pydantic em `src/api/schemas/analysis.py` definem os contratos de dados, agora incluindo `source_documents`.

## Service Layer (`src/services/`)
Orquestra o fluxo RAG: recupera chunks relevantes, aplica re-ranking e monta o prompt enriquecido antes de chamar o LLM.

## RAG Layer (`src/rag/`)
Responsável por toda a lógica de recuperação de informação.
- `ingestion.py` — lê os documentos, divide em chunks e armazena no ChromaDB
- `retrieval.py` — converte a query em embedding e busca os chunks mais próximos
- `reranker.py` — reordena os chunks por relevância usando palavras-chave

## Core Layer (`src/core/`)
Centraliza a configuração do cliente Azure OpenAI e as exceções customizadas.

## Componentes
| Componente | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada da API |
| `api/schemas/analysis.py` | Contratos de request e response |
| `services/compliance_service.py` | Orquestra RAG + LLM |
| `rag/ingestion.py` | Pipeline de ingestão de documentos |
| `rag/retrieval.py` | Busca vetorial no ChromaDB |
| `rag/reranker.py` | Re-ranking por relevância |
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