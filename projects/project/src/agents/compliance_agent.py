import os
import shutil
import logging
import time
from pathlib import Path
from typing import TypedDict
from datetime import datetime

from langgraph.graph import StateGraph, END
from src.services.compliance_service import analyze_text

Path("data/logs").mkdir(parents=True, exist_ok=True)

# Configuração de logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/logs/agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Caminhos
INPUT_PATH = Path("data/input")
APPROVED_PATH = Path("data/output/approved")
REJECTED_PATH = Path("data/output/rejected_for_review")

# Garante que as pastas existem
for path in [INPUT_PATH, APPROVED_PATH, REJECTED_PATH, Path("data/logs")]:
    path.mkdir(parents=True, exist_ok=True)

class AgentState(TypedDict):
    filename: str
    content: str
    is_compliant: bool
    reason: str
    source_document: list
    action_taken: str
    processing_time: float
    error: str

def read_document(state: AgentState) -> AgentState:
    start = time.time()
    filename = state["filename"]
    filepath = INPUT_PATH / filename

    logger.info(f"[{filename}] Iniciando leitura do documento...")

    try:
        # Tenta UTF-8 primeiro, depois UTF-16
        for encoding in ["utf-8", "utf-16", "latin-1"]:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        logger.info(f"[{filename}] Documento lido com sucesso ({len(content)} caracteres)")
        return {**state, "content": content, "processing_time": time.time() - start}
    except Exception as e:
        logger.error(f"[{filename}] Erro ao ler o documento: {e}")
        return {**state, "error": str(e)}
   
def analyze_document(state: AgentState) -> AgentState:
    """Analisa o documento usando o RAG + LLM."""
    filename = state["filename"]
    content = state["content"]

    logger.info(f"[{filename}] Iniciando análise de compliance")

    try: 
        result = analyze_text(content)
        logger.info(f"[{filename}] Análise concluída - is compliant: {result.is_compliant}")
        logger.info(f"[{filename}] Fontes usadas: {result.source_documents}")

        return {
            **state,
            "is_compliant": result.is_compliant,
            "reason": result.reason,
            "source_document": result.source_documents
        }
    except Exception as e:
        logger.error(f"[{filename}] Erro durante a análise: {e}")
        return {**state, "error": str(e)}
def decide_action(state: AgentState) -> str:
    """Decide o próximo passo baseado no resultado da análise."""
    if state.get("error"):
        return "handle_error"
    if state["is_compliant"]:
        return "approve"
    return "reject"

def approve_document(state: AgentState) -> AgentState:
    """Move o documento para a pasta de aprovados."""
    filename = state["filename"]
    src = INPUT_PATH / filename
    dst = APPROVED_PATH / filename

    shutil.move(str(src), str(dst))
    logger.info(f"[{filename}] aprovado - movido para {APPROVED_PATH}")
    return {**state, "action_taken": "approved"}

def reject_document(state: AgentState) -> AgentState:
    """Move o documento para revisão e cria alerta."""
    filename = state["filename"]
    src = INPUT_PATH / filename
    dst = REJECTED_PATH / filename

    shutil.move(str(src), str(dst))
    # Cria alerta em arquivo de log
    alert_path = Path("data/logs") / f"alert_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(alert_path, "w", encoding="utf-8") as f:
        f.write(f"ALERTA DE NÃO CONFORMIDADE\n")
        f.write(f"Arquivo: {filename}\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Motivo: {state['reason']}\n")
        f.write(f"Fontes: {state['source_document']}\n")
    logger.warning(f"[{filename}] rejeitado - movido para {REJECTED_PATH} e alerta criado em {alert_path}")

    return {**state, "action_taken": "rejected_for_review"}

def handle_error(state: AgentState) -> AgentState:
    """Lida com erros durante o processamento."""
    filename = state["filename"]
    logger.error(f"[{filename}] Erro durante o processamento: {state.get('error')}")
    return {**state, "action_taken": "error"}

def build_agent():
    """Constrói o agente de compliance usando um grafo de estados."""
    graph = StateGraph(AgentState)

    # Adiciona os nos
    graph.add_node("read_document", read_document)
    graph.add_node("analyze_document", analyze_document)
    graph.add_node("approve_document", approve_document)
    graph.add_node("reject_document", reject_document)
    graph.add_node("handle_error", handle_error)

    # Define o fluxo
    graph.set_entry_point("read_document")
    graph.add_edge("read_document", "analyze_document")
    graph.add_conditional_edges(
        "analyze_document",
        decide_action,
        {
            "approve": "approve_document",
            "reject": "reject_document",
            "handle_error": "handle_error"
        }
    )
    graph.add_edge("approve_document", END)
    graph.add_edge("reject_document", END)
    graph.add_edge("handle_error", END)

    return graph.compile()

def run_agent(filename:str):
    """executa o agente para um arquivo específico"""
    agent = build_agent()
    initial_state = AgentState(
        filename=filename,
        content="",
        is_compliant=False,
        reason="",
        source_document=[],
        action_taken="",
        processing_time=0.0,
        error=""
    )
    result = agent.invoke(initial_state)
    return result