import re
from src.core.llm_client import AzureModel
from src.core.exceptions import APIConectionError
from src.api.schemas.analysis import AnalysisResponse
from src.rag.retrieval import retrieve

def analyze_text(text_to_analyze :str) -> AnalysisResponse:
    """Analisa uma recomendação de investimento usando RAG + LLM."""

    #busca os chunks mais relevantes da knowledge base
    
    relevant_chunks = retrieve(text_to_analyze, n_results=2)

    print (f"Chunks relevantes encontrados: {len(relevant_chunks)}")
    for chunk in relevant_chunks:
        print(f"Fonte: {chunk['source']} - Conteúdo: {chunk['content'][:50]}")    # Monta o contexto com os documentos recuperados
    context = "\n\n".join([
        f"Fonte: {chunk['source']} \n{chunk['content'][:300]}"
        for chunk in relevant_chunks
    ])

    # Extrai as fontes usadas
    sources = list(set({chunk['source'] for chunk in relevant_chunks}))

    #instancia o cliente LLM
    llm_client = AzureModel()

    # Prompt enriquecido com contexto das politicas
    prompt = f"""
    Você é um analista de compliance financeiro.
    Com base nos seguintes documentos de política:
    {context}

    analisa a seguinte recomendação de investimento: '{text_to_analyze}'.
    Verifique se ela est[a em conformidade com as politicas acima.
    retorne sua análise explicando o motivo e cite os produtos mencionados.
    """

    try: 
        response = llm_client.invoke(prompt=prompt)
        raw_content = response.choices[0].message.content
        clean_content = raw_content
        clean_content = re.sub(r'\*+','', clean_content) #remove ** e *
        clean_content = re.sub(r'#{1,6}\s','',clean_content) #remove markdown headers
        clean_content = re.sub(r'\n-{3,}', '\n\n', clean_content) #remove linhas de --- ou mais
        clean_content= clean_content.strip()


        return AnalysisResponse(
        is_compliant= "não" not in raw_content.lower(),
        reason=clean_content,
        mentioned_products=sources
        )

    except Exception as e:
        raise APIConectionError(f"Falha ao conectar com o serviço de análise {e}")