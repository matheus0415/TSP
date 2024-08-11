import numpy as np

arquivo_matriz = 'files/att48_d.txt'

def carregar_matriz_distancias(arquivo):
    """
    Carrega uma matriz de distâncias a partir de um arquivo de texto.
    
    :param arquivo: Caminho para o arquivo que contém a matriz de distâncias.
    :return: Uma matriz numpy 2D representando as distâncias entre as cidades.
    """
    try:
        matriz = np.loadtxt(arquivo, dtype=float)
        return matriz
    except Exception as e:
        print(f"Erro ao carregar a matriz de distâncias: {e}")
        return None

matriz_distancias = carregar_matriz_distancias(arquivo_matriz)

if matriz_distancias is not None:
    print("Matriz de Distâncias Carregada:")
    print(matriz_distancias)
else:
    print("Não foi possível carregar a matriz de distâncias.")
