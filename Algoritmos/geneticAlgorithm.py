import numpy as np
import random
from loadFile import carregar_matriz_distancias
from saveResult import salvar_resultado

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

def inicializar_populacao(tamanho_populacao, num_cidades):
    """
    Inicializa uma população de soluções aleatórias.
    
    :param tamanho_populacao: Número de soluções na população.
    :param num_cidades: Número total de cidades.
    :return: Uma lista de percursos representando a população.
    """
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(gerar_solucao_inicial(num_cidades))
    return populacao

def selecao_roleta(populacao, fitness):
    """
    Realiza a seleção dos indivíduos usando a roleta viciada (seleção proporcional ao fitness).
    
    :param populacao: A população de percursos.
    :param fitness: Lista de valores de fitness correspondentes à população.
    :return: Um percurso selecionado.
    """
    max_fitness = sum(fitness)
    pick = random.uniform(0, max_fitness)
    current = 0
    
    for i, f in enumerate(fitness):
        current += f
        if current > pick:
            return populacao[i]

def crossover_ox(pai1, pai2):
    """
    Realiza o crossover Ordered Crossover (OX) para gerar um novo percurso (filho).
    
    :param pai1: O primeiro percurso.
    :param pai2: O segundo percurso.
    :return: Um novo percurso gerado a partir dos pais.
    """
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    
    filho = [None] * tamanho
    filho[inicio:fim] = pai1[inicio:fim]
    
    idx = fim
    for cidade in pai2:
        if cidade not in filho:
            if idx >= tamanho:
                idx = 0
            filho[idx] = cidade
            idx += 1
    
    return filho

def mutacao(percurso, taxa_mutacao):
    """
    Aplica mutação a um percurso trocando duas cidades de posição.
    
    :param percurso: O percurso a ser mutado.
    :param taxa_mutacao: A probabilidade de realizar a mutação.
    :return: O percurso possivelmente mutado.
    """
    for i in range(len(percurso)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(percurso) - 1)
            percurso[i], percurso[j] = percurso[j], percurso[i]
    return percurso

def algoritmo_genetico(matriz_distancias, tamanho_populacao=100, num_geracoes=500, taxa_mutacao=0.01):
    """
    Aplica o algoritmo genético para otimizar a solução do TSP.
    
    :param matriz_distancias: Matriz numpy 2D representando as distâncias entre as cidades.
    :param tamanho_populacao: Número de indivíduos na população.
    :param num_geracoes: Número de gerações a serem evoluídas.
    :param taxa_mutacao: A probabilidade de mutação em cada indivíduo.
    :return: O melhor percurso encontrado e sua distância total.
    """
    num_cidades = len(matriz_distancias)
    populacao = inicializar_populacao(tamanho_populacao, num_cidades)
    
    for geracao in range(num_geracoes):
        fitness = [1 / calcular_distancia_total(matriz_distancias, percurso) for percurso in populacao]
        nova_populacao = []
        
        for _ in range(tamanho_populacao):
            pai1 = selecao_roleta(populacao, fitness)
            pai2 = selecao_roleta(populacao, fitness)
            filho = crossover_ox(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
        
        populacao = nova_populacao
    
    melhor_percurso = min(populacao, key=lambda p: calcular_distancia_total(matriz_distancias, p))
    melhor_distancia = calcular_distancia_total(matriz_distancias, melhor_percurso)
    
    return melhor_percurso, melhor_distancia

# Exemplo de uso
arquivo_matriz = 'files/five_d.txt'
matriz_distancias = carregar_matriz_distancias(arquivo_matriz)

if matriz_distancias is not None:
    melhor_percurso, melhor_distancia = algoritmo_genetico(matriz_distancias)
    print("Melhor percurso encontrado:")
    print(melhor_percurso)
    print(f"Distância total: {melhor_distancia}")
    pasta_destino = 'Resultados'
    salvar_resultado( 'Algoritmo genético',melhor_percurso, melhor_distancia, pasta_destino)
else:
    print("Não foi possível carregar a matriz de distâncias.")
