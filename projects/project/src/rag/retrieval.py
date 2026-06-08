import os
import pickle
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Caminho base dos dados gerados pela ingestão
DATA_PATH = Path(__file__).parent.parent.parent / "data"

# Inicializa o cliente Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# Nome do deployment de embedding
EMBEDDING_MODEL = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")


def get_embedding(text: str) -> list:
    """Gera o embedding semântico de um texto usando o Azure OpenAI."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    """Calcula a similaridade cosseno entre dois vetores."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """Busca os chunks mais relevantes para a query usando similaridade semântica."""
    try:
        print(f"Procurando em: {DATA_PATH.absolute()}")
        print(f"chunks.pkl existe: {(DATA_PATH / 'chunks.pkl').exists()}")
        print(f"embeddings.npy existe: {(DATA_PATH / 'embeddings.npy').exists()}")

        # Carrega os chunks e metadados salvos pela ingestão
        with open(DATA_PATH / "chunks.pkl", "rb") as f:
            data = pickle.load(f)

        # Carrega os embeddings pré-calculados
        embeddings = np.load(str(DATA_PATH / "embeddings.npy"))

        # Gera o embedding da query em tempo real
        query_embedding = np.array(get_embedding(query))

        # Calcula a similaridade da query com cada chunk
        similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]

        # Ordena e pega os N chunks mais similares
        top_indices = np.argsort(similarities)[::-1][:n_results]

        chunks = []
        for i in top_indices:
            chunk = data["metadata"][i].copy()
            chunk["distance"] = float(1 - similarities[i])
            chunks.append(chunk)

        return chunks

    except Exception as e:
        print(f"Erro no retrieve: {e}")
        import traceback
        traceback.print_exc()
        return []