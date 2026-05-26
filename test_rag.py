import sys
sys.path.append("projects/project")

from src.rag.retrieval import retrieve

results = retrieve("recomendação de investimento para perfil conservador")
for r in results:
    print(f"Fonte:{r['source']}")
    print(f"chunk id:{r['chunk_id']}")
    print(f"Distance:{r['distance']:.4f}")
    print(f"conteudo:{r['content'][:100]}...")
    print(f"Fonte:{r['source']}")
    print("---")

