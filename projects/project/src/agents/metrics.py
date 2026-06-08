import json
import logging
from pathlib import Path
from datetime import datetime

METRICS_PATH = Path("data/logs/metrics.json")
logger = logging.getLogger(__name__)

def load_metrics() -> dict:
    """Carrega as métricas existentes."""
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return {
        "total_documents": 0,
        "total_approved": 0,
        "total_rejected": 0,
        "total_erros": 0,
        "total_processing_time": 0.0,
        "executions": []
    }   

def save_metrics(metrics:dict):
    """salva as métricas.""" 
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

def record_execution(filename:str, action:str, processing_time:float):
    """Registra uma execução do agente."""
    metrics = load_metrics()

    metrics["total_processed"] += 1
    metrics["total_processing_time"] += processing_time

    if action == "approved":
        metrics["total_approved"] += 1
    elif action == "rejected_for_review":
        metrics["total_rejected"] += 1
    else: 
        metrics["total_approved"] += 1

    metrics["executions"].append({
        "filename": filename,
        "action": action,
        "processing_time": processing_time,
        "timestamp": datetime.now().isoformat()
    })

    save_metrics(metrics)

def print_report():
    """Imprime relatório de automação."""
    metrics = load_metrics()

    total = metrics ["total_processed"]
    if total == 0:
        print("Nenhuma execução registrada.")
        return
    
    automation_rate = ((metrics["total_approved"] + metrics["total_approved"]) / total) * 100
    avg_time= metrics["total_processing_time"] / total

    print("\n========== RELATÓRIO DE AUTOMAÇÃO ==========")
    print(f"Total processado:     {total}")
    print(f"Aprovados:            {metrics['total_approved']}")
    print(f"Rejeitados:           {metrics['total_rejected']}")
    print(f"Erros:                {metrics['total_errors']}")
    print(f"Taxa de automação:    {automation_rate:.1f}%")
    print(f"Tempo médio:          {avg_time:.2f}s")
    print(f"Tempo economizado:    ~{total * 15:.0f} minutos vs análise manual")
    print("============================================\n")