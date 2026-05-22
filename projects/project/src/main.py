from fastapi import FastAPI, HTTPException
from src.api.schemas.analysis import AnalysisRequest, AnalysisResponse
from src.services.compliance_service import analyze_text
from src.core.exceptions import APIConectionError
 
app= FastAPI()

@app.get("/health")
def health():
    return {"status":"ok"}
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_recomendation(request: AnalysisRequest):
    try:
        result = analyze_text(request.text_to_analyze)
        if not result:
            raise APIConectionError("Falha ao conectar com o serviço de análise.")
        return result
    except APIConectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno no servidor.")
    