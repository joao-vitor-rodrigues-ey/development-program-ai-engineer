from pydantic import BaseModel, Field
from typing import List

class AnalysisRequest(BaseModel):
    text_to_analyze: str = Field(...,min_length=10,description="Texto da recomendação a ser analisado.")

class AnalysisResponse(BaseModel):
    is_compliant: bool= Field(...,description="Indica se a recomendação está em conformidade.")
    reason:     str = Field(...,description="Justificativa detalhada da análise.")
    mentioned_products: List[str] = Field(...,description="Lista de produtos mencionados .")