import os 
from pathlib import Path
import chromadb
from pypdf import PdfReader

# Caminho para a knowledge base
KNOWLEDGE_BASE_PATH = Path("knowledge_base")
CHROMA_DB_PATH = Path("chroma_db")

def load_pdfs() ->list[dict]:
    """ Le todos os PDFs da pasta KNOWLEDGE_BASE e extrai o texto para uma lista de dicionários."""
    documents =[]

    for pdf_file in KNOWLEDGE_BASE_PATH.glob("*.pdf"):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        documents.append({
            "filename": pdf_file.name,
            "content": text
        })
    return documents
def chunk_text(text:str, chunk_size:int = 500,overlap: int = 59) -> list[str]:
    """ divide o texto em chunks com sobreposição. """
    chunks = []
    start = 0

    while start <len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
def ingest():
    """Pipeline completo de ingestão - lê, divide e armazena no chromaDB."""
    print("iniciando ingestão. . .")
    #inicializa o chromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

    # Apaga a coleção se ja existir (idempotente)
    try:
        client.delete_collection("compliance_docs")
    except:
        pass

    collection = client.create_collection("compliance_docs")

    # carrega os PDFs
    documents = load_pdfs()

    # Processa cada documento
    for doc in documents:
        chunks= chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": doc["filename"], "chunk_id": i}],
                ids=[f"{doc['filename']}_{i}"]   
            )
    print(f" Ingestão concluída! {collection.count()} chunks armazenados no ChromaDB.")

if __name__ == "__main__":   
    ingest()