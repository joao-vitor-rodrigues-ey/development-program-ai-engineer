from pydantic import BaseModel, Field
from typing import List

# Schema de entrada, define o que a Api aceita no post /analyze
class AnalysisRequest(BaseModel):
    text_to_analyze: str = Field(...,min_length=10,description="Texto da recomendação a ser analisado.")

# Schema de saida, define o que a API devolve após a análise
class AnalysisResponse(BaseModel):
    is_compliant: bool= Field(...,description="Indica se a recomendação está em conformidade.")
    reason:     str = Field(...,description="Justificativa detalhada da análise.")
    mentioned_products: List[str] = Field(...,description="Lista de produtos mencionados .")