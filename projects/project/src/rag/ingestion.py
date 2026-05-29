import ssl 
import os 
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"

from chromadb import EmbeddingFunction

class SimpleEmbedding(EmbeddingFunction):
    def __call__(self, input):
        import numpy as np
        result = []
        for text in input:
            vec = np.zeros(128, dtype=np.float32)
            for i, char in enumerate(text):
                vec[i % 128] += ord(char)
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            result.append(vec.tolist())
        return result

# Caminho para a knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent / "knowledge_base"
CHROMA_DB_PATH = Path(__file__).parent.parent.parent / "data" / "chroma_db"

def load_documents() ->list[dict]:
    """ Le todos os TXTs da pasta KNOWLEDGE_BASE e extrai o texto para uma lista de dicionários."""
    documents =[]
    print(f"Procurando em: {KNOWLEDGE_BASE_PATH.absolute()}")
    for txt_file in KNOWLEDGE_BASE_PATH.glob("*.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "filename": txt_file.name,
            "content": text
        })
        print(f"Carregado {txt_file.name}")
    return documents

def chunk_text(text:str, chunk_size:int = 500,overlap: int = 59) -> list[str]:
    """ divide o texto em chunks com sobreposição. """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest():
    """ Pipeline completo de ingestão - lê os documentos, divide em chunks e armazena no chromaDB"""
    print("Iniciando processo de ingestão...")
    # Usa embedding simples sem precisar baixar modelo
    ef = embedding_functions.DefaultEmbeddingFunction()

    # Inicializa o ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    #Apaga a coleção antiga se existir
    try:
        client.delete_collection("compliance_docs")
    except:
        pass

    collection =client.create_collection("compliance_docs",embedding_function=SimpleEmbedding())

    #carrega os documentos 
    documents = load_documents()

    #processa cada documento 
    for doc in documents:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": doc["filename"], "chunk_id": i}],
                ids= [f"{doc['filename']}_{i}"]
            )
    print(f"Ingestão concluída com sucesso.{collection.count()}chunks armazenados.")
if __name__ == "__main__":   
    ingest()  