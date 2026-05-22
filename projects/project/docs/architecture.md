# Arquitetura

*Esta documentação descreverá a arquitetura de alto nível da solução.*
## Visão Geral 
O compliance Checker é uma API REST que recebe recomendações de investimento e utiliza um LLM (Azure OpenAI) para analisar se estão em conformidade com as politicas de investimento 

## Fluxo de dados
Cliente -> POST/analyze -> main.py ->compliance_service.py ->AzureModel(LLM) -> AnalysisResponse -> Client

## Camadas

### API Layer ('src/api/')
Responsavel por receber as requisições http,validar os dados de entrada e retornas as respostas. Os schemas Pydantic em 'src/api/schemas/analysis.py' definem os contratos de dados.

### Service Layer('src/services/')
Contém a lógica do negócio isolada da camada http. A função 'analyze_text' monta o prompt, chama o LLM e retorna o resultado estruturado.

### Core Layer ('src/core/')
Centraliza a configuração do cliente Azure OpenAi ('llm_client.py)e as exceções customizadas('exceptions.py').

## Componentes
│ Componente │  Responsabilidade
│  --- │ ---- │ 
│ 'main.py' │  Ponto de entrada da API, define os endpoints │ 
│ 'api/schemas/analysis.py │ Contratos de request e response │   
│ 'services/compliance_service.py' │ Lógica de analise de compliance │ 
│ 'core/llm_client.py' │ Conexão com Azure OpenAI │
│ 'core/exceptions.py' │ Exceções Customizadas │