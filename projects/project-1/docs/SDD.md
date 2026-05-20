# Solution Design Document (SDD)

*Este documento detalhará o design da solução para cada projeto.*

## Objetivo
 Construir um serviço especialista em formato de API REST que simula um analista de compliance, fornecendo análise automatizada de recomendações de investimento usando LLM.

## Escopo 
 Este documento cobre o projeto 1 do programa, O objetivo é entregar uma API funcional que recebe recomendações de investimento e retorne uma análise de confromidade estruturada.

#### 3. Requisitos Funcionais
 RF01: A API deve receber um texto de recomendação de investimento via POST `/analyze`
 RF02: A API deve retornar se a recomendação está em conformidade (`is_compliant`)
 RF03: A API deve retornar uma justificativa detalhada (`reason`) 
 RF04: A API deve retornar os produtos mencionados (`mentioned_products`) 
 RF05: A API deve expor um endpoint de health check via GET `/health`

## 4. Requisitos Não Funcionais- 
 RNF01: A API deve validar os dados de entrada com Pydantic- 
 RNF02: As credenciais não devem ser versionadas no repositório- 
 RNF03: A aplicação deve ser containerizável via Docker- 
 RNF04: O código deve ter cobertura de testes unitários e de integração

## 5. Tecnologias Utilizadas
 | Tecnologia | Uso |
 |---|---|
 | Python 3.11 | Linguagem principal |
 | FastAPI | Framework da API || Pydantic | Validação de dados |
 | Azure OpenAI | LLM para análise de compliance || Instructor | Extração de dados estruturados |
 | python-dotenv | Gerenciamento de variáveis de ambiente |
 | pytest | Testes automatizados |
 
## 6. Endpoints
 
### GET /health
Descrição: Verifica se a API está online
Response: `{"status": "ok"}`
  Status Code: 200### POST /analyze
  Descrição: Analisa uma recomendação de investimento
  Request Body:```json{ "text_to_analyze": "string (min 10 caracteres)"}```
  Response:```json{ "is_compliant": true, "reason": "string", "mentioned_products": []}```
  Status Codes: 200, 422, 500, 503
 
 ## 7. Tratamento de Erros
 | Código | Situação |
 |---|---|
 | 200 | Sucesso |
 | 422 | Dados de entrada inválidos (Pydantic) |
 | 503 | Falha na conexão com o Azure OpenAI |
 | 500 | Erro interno não esperado |