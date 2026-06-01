import sys 
sys.path.insert(0,'.')

from src.rag.retrieval import retrieve

results = retrieve("recomendação de investimento para perfil conservador")
print(f"TIpo: {type(results)}")
print(f"Valor: {results}")
for r in results:
    print(f"Fonte: {r['source']}")
    print(f"chunk ID: {r['chunk_id']}")
    print(f"Distancia: {r['distance']:.4f}")
    print(f"Conteúdo: {r['content'][:150]}")
    print("---")