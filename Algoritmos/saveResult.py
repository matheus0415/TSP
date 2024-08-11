import os
from datetime import datetime

def salvar_resultado(metodo_utilizado, melhor_percurso, melhor_distancia, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_arquivo = os.path.join(pasta_destino, f"resultado_tsp_{timestamp}.txt")
    
    with open(caminho_arquivo, "w") as f:
        f.write(f"Metodo: {metodo_utilizado}\n")
        f.write("Melhor percurso encontrado:\n")
        f.write(" -> ".join(map(str, melhor_percurso)) + "\n")
        f.write(f"Distância total: {melhor_distancia}\n")
    
    print(f"Resultado salvo em {caminho_arquivo}")