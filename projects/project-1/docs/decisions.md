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