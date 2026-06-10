from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class PerfilCliente(str, Enum):
    conservador = "conservador"
    moderado = "moderado"
    agressivo = "agressivo"

class AnalysisRequest(BaseModel):
    text_to_analyze: str = Field(..., min_length=10, description="Texto da recomendação a ser analisada.")
    perfil_cliente: PerfilCliente = Field(..., description="Perfil de risco do cliente.")

class AnalysisResponse(BaseModel):
    is_compliant: bool = Field(..., description="Indica se a recomendação está em conformidade.")
    reason: str = Field(..., description="Justificativa detalhada da análise.")
    mentioned_products: List[str] = Field([], description="Lista de produtos de investimento mencionados.")
    source_documents: List[str] = Field([], description="Documentos usados como base para a análise.")
    source_chunk_id: List[int] = Field([], description="IDs dos chunks usados na análise.")
    rerank_score: List[int] = Field([], description="Score de relevância de cada chunk.")
    perfil_cliente: str = Field(..., description="Perfil do cliente analisado.")