from pathlib import Path
import chromadb
import numpy as np

BASE_PATH = Path(__file__).parent.parent
CHROMA_DB_PATH = Path(__file__).parent.parent.parent / "data" / "chroma_db"

def text_to_vector(text: str, dim: int = 128) -> list[float]:
    """Converte texto em vetor numérico sem modelo externo."""
    vec = np.zeros(dim, dtype=np.float32)
    for i, char in enumerate(text):
        vec[i % dim] += ord(char)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()

def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """Busca os chunks mais relevantes para a query no ChromaDB."""
    
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    collection = client.get_collection("compliance_docs")
    
    query_embedding = text_to_vector(query)
    
    print(f"caminho do banco: {CHROMA_DB_PATH.absolute()}")
    print(f"Banco existe: {CHROMA_DB_PATH.exists()}")
    print(f"total de chunks no banco: {collection.count()}")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": results["distances"][0][i]
        })
    
    return chunks