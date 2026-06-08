import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.agents.compliance_agent import run_agent

logger = logging.getLogger(__name__)

INPUT_PATH = Path("data/input")


class RecommendationHandler(FileSystemEventHandler):
    """Monitora novos arquivos na pasta de input."""

    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # Só processa arquivos .txt
        if filepath.suffix != ".txt":
            return

        filename = filepath.name
        logger.info(f"Novo arquivo detectado: {filename}")
        
        # Pequena pausa pra garantir que o arquivo foi completamente escrito
        time.sleep(1)
        
        try:
            result = run_agent(filename)
            logger.info(f"Processamento concluído: {filename} -> {result['action_taken']}")
        except Exception as e:
            logger.error(f"Erro ao processar {filename}: {e}")


def start_monitor():
    """Inicia o monitoramento da pasta de input."""
    logger.info(f"Monitorando pasta: {INPUT_PATH.absolute()}")
    
    event_handler = RecommendationHandler()
    observer = Observer()
    observer.schedule(event_handler, str(INPUT_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitor encerrado.")
    
    observer.join()


if __name__ == "__main__":
    start_monitor()