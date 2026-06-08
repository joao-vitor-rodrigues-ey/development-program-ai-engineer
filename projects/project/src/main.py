import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from src.api.schemas.analysis import AnalysisRequest, AnalysisResponse
from src.services.compliance_service import analyze_text
from src.core.exceptions import APIConectionError
from src.agents.compliance_agent import run_agent
from src.agents.metrics import print_report, load_metrics

app = FastAPI()

logger = logging.getLogger(__name__)


@app.get("/health")
def health():
    """Verifica se a API está no ar."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_recommendation(request: AnalysisRequest):
    """Analisa uma recomendação de investimento via RAG + LLM."""
    try:
        result = analyze_text(request.text_to_analyze)
        if not result:
            raise APIConectionError("Falha ao conectar com o serviço de análise.")
        return result
    except APIConectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")


@app.post("/agent/process/{filename}")
async def process_document(filename: str, background_tasks: BackgroundTasks):
    """Dispara o agente para processar um arquivo da pasta data/input/."""
    background_tasks.add_task(run_agent, filename)
    return {"message": f"Processamento de '{filename}' iniciado em background."}


@app.get("/agent/metrics")
def get_metrics():
    """Retorna as métricas de automação do agente."""
    return load_metrics()