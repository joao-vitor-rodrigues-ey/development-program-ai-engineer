# Compliance Checker API

API REST que simula um analista de compliance financeiro, analisando recomendações de investimento e verificando sua conformidade com as políticas de risco do cliente.

## Contexto de Negócio

Analistas de compliance gastam um tempo enorme revisando manualmente comunicações para garantir a adequação ao perfil de risco do cliente. Esta API automatiza essa análise inicial, identificando potenciais violações e liberando os analistas para focar nos casos que realmente exigem atenção humana.

## Arquitetura

```
Cliente → POST /analyze → API Layer → Service Layer → Azure OpenAI (LLM) → Resposta estruturada
```

## Estrutura do Projeto

```
project-1/
├── .env # Credenciais Azure OpenAI (não versionado)
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│ ├── main.py # Ponto de entrada da API
│ ├── api/
│ │ └── schemas/
│ │ └── analysis.py # Contratos de request e response
│ ├── core/
│ │ ├── llm_client.py # Cliente Azure OpenAI
│ │ └── exceptions.py # Exceções customizadas
│ └── services/
│ └── compliance_service.py # Lógica de análise de compliance
└── tests/
    ├── test_api.py # Testes de integração
    └── test_services.py # Testes unitários
```

## Endpoints

### GET /health
Verifica se a API está online.

**Response:**
```json
{"status": "ok"}
```

### POST /analyze
Analisa uma recomendação de investimento.

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
  "reason": "A recomendação não está adequada ao perfil conservador do cliente...",
  "mentioned_products": []
}
```

## Como Rodar

### Localmente

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1 # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env com suas credenciais Azure OpenAI
# Suba a API
uvicorn src.main:app --reload
```

Acesse a documentação interativa em: http://127.0.0.1:8000/docs

### Com Docker

```bash
docker build -t compliance-checker .
docker run -p 8000:8000 --env-file .env compliance-checker
```

## Testes

```bash
python -m pytest tests/ -v
```

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| FastAPI | Framework da API |
| Pydantic | Validação de dados |
| Azure OpenAI | LLM para análise de compliance |
| Instructor | Extração de dados estruturados |
| pytest | Testes automatizados |
| Docker | Containerização |
```

