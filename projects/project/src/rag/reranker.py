import re
from typing import List

   # Re-rankeia os chunks por relevância baseado em palavras-chave em comum com a query.
def simple_rerank(query: str, chunks: List[dict]) -> List[dict]:
    
    query_words = set(re.findall(r'\w+', query.lower()))
    
    reranked = []
    for chunk in chunks:
        content_words = set(re.findall(r'\w+', chunk['content'].lower()))
        common_words = query_words.intersection(content_words)
        new_chunk = dict(chunk)
        new_chunk['rerank_score'] = len(common_words)
        reranked.append(new_chunk)
    
    return sorted(reranked, key=lambda x: x['rerank_score'], reverse=True)