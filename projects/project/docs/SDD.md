# Solution Design Document - Compliance Checker API

## 1. Objetivo
Construir um serviço especialista em formato de API REST que simula um analista de compliance financeiro, fornecendo análise automatizada de recomendações de investimento usando LLM com RAG (Retrieval-Augmented Generation).

## 2. Escopo
Este documento cobre os Projetos 1 e 2 do programa. O Projeto 1 entregou a API base com LLM. O Projeto 2 evoluiu para um sistema RAG com base de conhecimento auditável.

## 3. Requisitos Funcionais
- **RF01**: A API deve receber um texto de recomendação de investimento via POST `/analyze`
- **RF02**: A API deve buscar chunks relevantes da knowledge base antes de chamar o LLM
- **RF03**: A API deve aplicar re-ranking nos chunks recuperados
- **RF04**: A API deve retornar se a recomendação está em conformidade (`is_compliant`)
- **RF05**: A API deve retornar uma justificativa detalhada (`reason`)
- **RF06**: A API deve retornar os documentos usados como fonte (`source_documents`)
- **RF07**: A API deve expor um endpoint de health check via GET `/health`

## 4. Requisitos Não Funcionais
- **RNF01**: A API deve validar os dados de entrada com Pydantic
- **RNF02**: As credenciais não devem ser versionadas no repositório
- **RNF03**: A aplicação deve ser containerizável via Docker
- **RNF04**: O sistema RAG deve funcionar sem dependências externas de rede
- **RNF05**: O código deve ter cobertura de testes unitários e de integração

## 5. Tecnologias Utilizadas
| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework da API |
| Pydantic | Validação de dados |
| Azure OpenAI | LLM para análise de compliance |
| ChromaDB | Banco de dados vetorial local |
| Instructor | Extração de dados estruturados |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| pytest | Testes automatizados |

## 6. Fluxo RAG
1. Cliente envia texto via POST `/analyze`
2. `compliance_service` chama `retrieve()` com a query
3. `retrieval.py` converte query em embedding e busca no ChromaDB
4. `reranker.py` reordena os chunks por relevância
5. Prompt é montado com os chunks como contexto
6. LLM analisa com base nos documentos reais
7. Resposta retorna com `is_compliant`, `reason` e `source_documents`

## 7. Endpoints

### GET /health
- **Descrição**: Verifica se a API está online
- **Response**: `{"status": "ok"}`
- **Status Code**: 200

### POST /analyze
- **Descrição**: Analisa uma recomendação de investimento
- **Request Body**:
```json
{
  "text_to_analyze": "string (min 10 caracteres)"
}
response

{"is_compliant" :false
  "reason": "string",
  "mentioned_products":[]
  "source_documents":["politica_adequada_investimento_v1.2.txt"]
}
tratamento de erros
200 - sucesso
422 - dados de entrada invalidos
504 - falha na conexão com o azure OpenAI
500 - erro interno não esperado