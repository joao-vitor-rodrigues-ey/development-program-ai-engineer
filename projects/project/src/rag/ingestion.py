import os
import pickle
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import time

from pypdf import PdfReader 

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Caminhos base do projeto
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent / "knowledge_base"
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

# pegar os documentos novos
def load_documents() -> list[dict]:
    """Lê todos os TXTs e PDFsa pasta knowledge_base e retorna lista de documentos."""
    documents = []
    for txt_file in KNOWLEDGE_BASE_PATH.glob("*.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read()
        documents.append({
            "filename": txt_file.name,
            "content": text
        })
        print(f"Carregado: {txt_file.name}")

    for pdf_file in KNOWLEDGE_BASE_PATH.glob("*.pdf"):    
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        documents.append({
            "filename": pdf_file.name,
            "content": text
        })
        print(f"Carregado: {pdf_file.name}")

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Divide o texto em chunks com sobreposição para não perder contexto nas bordas."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # Avança menos que o chunk_size pra garantir sobreposição
        start += chunk_size - overlap
    return chunks


def ingest():
    """Pipeline completo de ingestão — lê, divide, gera embeddings semânticos e salva."""
    print("Iniciando processo de ingestão...")
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    documents = load_documents()

    all_chunks = []
    metadata = []
    embeddings = []

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            print(f"Gerando embedding para chunk {i} de {doc['filename']}...")
            
            try:
            # Gera embedding semântico via Azure OpenAI
                embedding = get_embedding(chunk)
            except Exception as e:
                print(f"rate limite, aguardando 60 segundos...")
                time.sleep(60)
                embedding = get_embedding(chunk)

            all_chunks.append(chunk)
            embeddings.append(embedding)
            metadata.append({
                "source": doc["filename"],
                "chunk_id": i,
                "content": chunk
            })

    # Salva os chunks e metadados em pickle
    with open(DATA_PATH / "chunks.pkl", "wb") as f:
        pickle.dump({"chunks": all_chunks, "metadata": metadata}, f)

    # Salva os embeddings em formato numpy para busca eficiente
    np.save(str(DATA_PATH / "embeddings.npy"), np.array(embeddings))

    print(f"Ingestão concluída! {len(all_chunks)} chunks armazenados.")


if __name__ == "__main__":
    ingest()