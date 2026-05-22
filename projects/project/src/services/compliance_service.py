from src.core.llm_client import AzureModel
from src.core.exceptions import APIConectionError
from src.api.schemas.analysis import AnalysisRequest, AnalysisResponse

def analyze_text(text_to_analyze:str) -> AnalysisResponse:
    llm_client = AzureModel()

    prompt = f"""
    Analise a seguinte recomendação de investimento :'{text_to_analyze}'.
    Verifique se ela está em conformidade com as regulamentações de compliance.
    retorne sua análise explicando o motivo e cite os produtos mencionados.
    """ 
    try:
        response = llm_client.invoke(prompt=prompt)
        raw_content = response.choices[0].message.content

        return AnalysisResponse(
            is_compliant="não" not in raw_content.lower(),
            reason=raw_content,
            mentioned_products=[]
        )
    except Exception as e:
        raise APIConectionError(f"Falha ao conectar com o serviço de análise: (e)")
    