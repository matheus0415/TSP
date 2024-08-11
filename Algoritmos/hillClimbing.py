import numpy as np
import random
from loadFile import carregar_matriz_distancias 

def calcular_distancia_total(matriz_distancias, percurso):
    """
    Calcula a distância total para um percurso específico no TSP.
    
    :param matriz_distancias: Matriz numpy 2D representando as distâncias entre as cidades.
    :param percurso: Lista representando a ordem em que as cidades são visitadas.
    :return: A distância total do percurso.
    """
    distancia_total = 0
    num_cidades = len(percurso)
    
    for i in range(num_cidades - 1):
        distancia_total += matriz_distancias[percurso[i], percurso[i+1]]
    # Adiciona a distância para retornar à cidade inicial
    distancia_total += matriz_distancias[percurso[-1], percurso[0]]
    
    return distancia_total

def gerar_solucao_inicial(num_cidades):
    """
    Gera uma solução inicial aleatória para o TSP.
    
    :param num_cidades: Número total de cidades.
    :return: Uma lista representando uma solução inicial (percurso).
    """
    percurso = list(range(num_cidades))
    random.shuffle(percurso)
    return percurso

def gerar_vizinhos(percurso):
    """
    Gera vizinhos da solução atual trocando a ordem de dois vértices.
    
    :param percurso: Lista representando o percurso atual.
    :return: Uma lista de percursos vizinhos.
    """
    vizinhos = []
    num_cidades = len(percurso)
    
    for i in range(num_cidades):
        for j in range(i + 1, num_cidades):
            vizinho = percurso.copy()
            # Troca a posição de duas cidades
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
    
    return vizinhos

def hill_climbing(matriz_distancias):
    """
    Aplica o algoritmo Hill Climbing para otimizar a solução do TSP.
    
    :param matriz_distancias: Matriz numpy 2D representando as distâncias entre as cidades.
    :return: O melhor percurso encontrado e sua distância total.
    """
    num_cidades = len(matriz_distancias)
    solucao_atual = gerar_solucao_inicial(num_cidades)
    melhor_distancia = calcular_distancia_total(matriz_distancias, solucao_atual)
    
    while True:
        vizinhos = gerar_vizinhos(solucao_atual)
        encontrou_melhor_vizinho = False
        
        for vizinho in vizinhos:
            distancia_vizinho = calcular_distancia_total(matriz_distancias, vizinho)
            if distancia_vizinho < melhor_distancia:
                solucao_atual = vizinho
                melhor_distancia = distancia_vizinho
                encontrou_melhor_vizinho = True
        
        if not encontrou_melhor_vizinho:
            break
    
    return solucao_atual, melhor_distancia

# Exemplo de uso
arquivo_matriz = 'files/five_d.txt'
matriz_distancias = carregar_matriz_distancias(arquivo_matriz)

if matriz_distancias is not None:
    melhor_percurso, melhor_distancia = hill_climbing(matriz_distancias)
    print("Melhor percurso encontrado:")
    print(melhor_percurso)
    print(f"Distância total: {melhor_distancia}")
else:
    print("Não foi possível carregar a matriz de distâncias.")
