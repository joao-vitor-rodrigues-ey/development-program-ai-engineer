from fastapi.testclient import TestClient
from src.main import app

# Cliente de teste que simula requisições HTTP sem subir o servidor

client = TestClient(app)
def test_health():
    # Verifica se o endpoint de health retorna 200 e o status correto
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok" }

# Verifica se o endpoint /analyze retorna 200 e os campos esperados
def test_analyze():
    response = client.post("/analyze", json={
        "text_to_analyze" : "Recomendo investir em ações de alto risco para perfil conservador"
    })
    assert response.status_code == 200
    assert "is_compliant" in response.json()
    assert "reason" in response.json()
    assert "mentioned_products" in response.json()