import re
from src.core.llm_client import AzureModel
from src.core.exceptions import APIConectionError
from src.api.schemas.analysis import AnalysisResponse
from src.rag.retrieval import retrieve
from src.rag.reranker import simple_rerank


def analyze_text(text_to_analyze: str) -> AnalysisResponse:
    """Analisa uma recomendação de investimento usando RAG + LLM."""

    # Busca os chunks mais relevantes da knowledge base
    relevant_chunks = retrieve(text_to_analyze, n_results=5)
    
    # Reordena por relevância
    relevant_chunks = simple_rerank(text_to_analyze, relevant_chunks)

    # Monta o contexto com os documentos recuperados
    context = "\n\n".join([
        f"Fonte: {chunk['source']}\n{chunk['content'][:300]}"
        for chunk in relevant_chunks
    ])

    # Extrai as fontes usadas
    sources = list({chunk['source'] for chunk in relevant_chunks})

    # Instancia o cliente LLM
    llm_client = AzureModel()

    # Prompt enriquecido com contexto das políticas
    prompt = f"""
    Você é um analista de compliance financeiro.
    Com base nos seguintes documentos de política:
    {context}

    Analise a seguinte recomendação de investimento: '{text_to_analyze}'.
    Verifique se ela está em conformidade com as políticas acima.
    Retorne sua análise explicando o motivo e cite os produtos mencionados.
    Seja objetivo e conciso.
    Ao final da análise, liste expllicitamente os produtos financeiros mencionados na recomendação no formato:
    PRODUTOS: produto1, produto2, produto3
    """

    try:
        response = llm_client.invoke(prompt=prompt)
        raw_content = response.choices[0].message.content

        # Limpa formatação markdown da resposta
        clean_content = raw_content
        clean_content = re.sub(r'\*+', '', clean_content)
        clean_content = re.sub(r'#{1,6}\s', '', clean_content)
        clean_content = re.sub(r'-{3,}', '', clean_content)
        clean_content = re.sub(r'\n{3,}', '\n\n', clean_content)
        clean_content = clean_content.strip()

        products = re.findall(r'PRODUTOS:\s*(.*)', clean_content)
        print(f"Produtos extraídos: {products}")
        mentioned = [p.strip() for p in products[0].split(',')]if products else []
        
        return AnalysisResponse(
            is_compliant="não" not in clean_content.lower(),
            reason=clean_content,
            mentioned_products=mentioned,
            source_documents=sources,
            source_chunk_id=[chunk['chunk_id'] for chunk in relevant_chunks],
            rerank_score=[chunk.get('rerank_score', 0) for chunk in relevant_chunks]

        )

    except Exception as e:
        raise APIConectionError(f"Falha ao conectar com o serviço de análise: {e}")