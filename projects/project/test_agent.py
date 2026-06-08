from src.agents.compliance_agent import run_agent

arquiv0s = [
    "recomendacao_01_nao_conforme.txt",
    "recomendacao_02_conforme.txt",
    "recomendacao_03_nao_conforme.txt",
    "recomendacao_04_conforme.txt",
]
for arquivo in arquiv0s:
    print(f"\n{'=' * 50}")
    print(f"Processando arquivo: {arquivo}")
    result = run_agent(arquivo)
    print(f"ação tomada: {result['action_taken']}")
    print(f"Compliant: {result['is_compliant']}")
