# Registro de Decisões Arquiteturais (ADRs)

## FastAPI como framework da API
Escolhemos FastAPI por sua performance, suporte nativo a tipagem Python e geração automatica de documentação via OpenAPI/Swagger, Facilitando o teste e a validação dos endpoints

## Pydantic para validação de dados
Pydantic garante que os contratos de request e response sejam validados automaticamenteevitando dados malformados e tornando erros mais claros e previsiveis

## Biblioteca Instructor
 Usamos Instructor em conjunto com o cliente Azure OpenAI para facilitar a extração de dados estruturados a partir das respostas do LLm, garantindo que o output sempre respeite o schema definido

## Separação em camadas (API / Services / Core)
 A lógica de negócio foiisolada em 'services/', desacoplada da camada HTTP. Isso facilita teste unitários com mock e torna o código mais reutilizável para os próximos projetos.

## Variáveis de ambiente via.env
 As credenciais do Azure OpenAI são carregadas via 'python-dotenv', evitando que informações sensiveis sejam versionadas no repositório.

## Testes com Pytest
 Implementamos testes de integração com 'TestClient'.

 ## ChromaDB como banco vetorial 
 Escolhemos ChromaDB por ser uma solução local, sem necessidade de serviços externos. Como a rede corporativa da EY bloqueia downloads de modelos externos via SSL, implementamos uma função de embedding customizada  baseada em hash de caracteres, eliminando dependencias externas.

 ## Re-ranking por palavras-chave
 Implementamos um re-ranker simples baseado em contagem de palavras-chave em comum entre a query e o chunk, Essa abordagem nao requer modelo externo e demonstra o conceito de re-ranking de forma auditável e transparente.

 ##Stritct Grounding 
 O prompt foi estruturado para forçar o LLM a basear sua análise exclusivamente nos documentos recuperados, garantindo que as decisões sejam sempre rastreáveis às politicas oficiais.a