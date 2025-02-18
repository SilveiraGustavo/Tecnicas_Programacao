import math  # Importa a biblioteca para cálculos matemáticos

# Definição dos aeroportos com seus respectivos nomes, códigos e coordenadas geográficas
AeroPortos = {
    1: {"nome": "Guarulhos", "codigo": "GRU", "latitude": -23.4356, "longitude": -46.4731},
    2: {"nome": "Galeão", "codigo": "GIG", "latitude": -22.8089, "longitude": -43.2437},
    3: {"nome": "Brasília", "codigo": "BSB", "latitude": -15.869, "longitude": -47.9292},
    4: {"nome": "Salvador", "codigo": "SSA", "latitude": -12.9115, "longitude": -38.322},
    5: {"nome": "Confins", "codigo": "CNF", "latitude": -19.6339, "longitude": -43.9692}
}

# Definição das conexões diretas entre os aeroportos (arestas do grafo)
Rotas = {
    1: [2, 3, 5],  # Guarulhos tem voos diretos para Galeão, Brasília e Confins
    2: [1, 4],     # Galeão tem voos diretos para Guarulhos e Salvador
    3: [1, 4, 5],  # Brasília tem voos diretos para Guarulhos, Salvador e Confins
    4: [2, 3, 5],  # Salvador tem voos diretos para Galeão, Brasília e Confins
    5: [1, 3, 4]   # Confins tem voos diretos para Guarulhos, Brasília e Salvador
}

# Função para calcular a distância entre dois aeroportos usando a fórmula de Haversine
def calculo_haversine(id1, id2):
    Raio_Terra = 6371  # Raio médio da Terra em quilômetros

    # Converte as coordenadas dos aeroportos para radianos
    lat1, lon1 = math.radians(AeroPortos[id1]["latitude"]), math.radians(AeroPortos[id1]["longitude"])
    lat2, lon2 = math.radians(AeroPortos[id2]["latitude"]), math.radians(AeroPortos[id2]["longitude"])

    # Diferença entre as coordenadas geográficas
    dlat, dlon = lat2 - lat1, lon2 - lon1

    # Aplicação da fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return Raio_Terra * c  # Retorna a distância em quilômetros

# Função para construir a matriz de adjacência do grafo, considerando apenas conexões diretas
def construir_matriz_adjacencia():
    ids = list(AeroPortos.keys())  # Lista com os IDs dos aeroportos
    n = len(ids)  # Quantidade de aeroportos

    # Inicializa a matriz com infinito, indicando que não há conexão entre os aeroportos
    matriz = [[float('inf')] * n for _ in range(n)]

    # Define a distância de um aeroporto para ele mesmo como zero
    for i in range(n):
        matriz[i][i] = 0

    # Preenche a matriz com as distâncias entre os aeroportos conectados diretamente
    for origem in Rotas:
        for destino in Rotas[origem]:
            matriz[origem - 1][destino - 1] = calculo_haversine(origem, destino)

    return matriz  # Retorna a matriz de adjacência

# Função para calcular a centralidade de grau de cada aeroporto
def calcular_centralidade_grau():
    centralidade = {}
    for aeroporto_id in AeroPortos:
        # A centralidade de grau é simplesmente o número de conexões diretas de um aeroporto
        grau = len(Rotas[aeroporto_id])
        centralidade[aeroporto_id] = grau
    return centralidade

# Implementação do Algoritmo de Dijkstra para encontrar o menor caminho entre dois aeroportos
def dijkstra(matriz, origem, destino):
    ids = list(AeroPortos.keys())  # Lista de IDs dos aeroportos
    origem_idx, destino_idx = ids.index(origem), ids.index(destino)  # Índices da origem e destino na matriz

    n = len(ids)  # Número total de aeroportos
    distancias = [float('inf')] * n  # Inicializa todas as distâncias como infinito
    distancias[origem_idx] = 0  # A distância da origem para ela mesma é zero

    nao_visitados = set(range(n))  # Conjunto de nós ainda não visitados
    antecessores = [-1] * n  # Lista para armazenar os predecessores no menor caminho

    while nao_visitados:
        # Encontra o nó com a menor distância ainda não visitado
        nodo_atual = min(nao_visitados, key=lambda idx: distancias[idx])

        # Se chegamos ao destino, reconstruímos o caminho
        if nodo_atual == destino_idx:
            caminho, idx = [], destino_idx
            while idx != -1:
                caminho.insert(0, ids[idx])  # Adiciona o aeroporto ao caminho
                idx = antecessores[idx]  # Retrocede para o nó anterior
            return caminho, distancias[destino_idx]  # Retorna o caminho encontrado e a distância total

        nao_visitados.remove(nodo_atual)  # Remove o nó atual do conjunto de nós não visitados

        # Atualiza as distâncias para os vizinhos do nó atual
        for vizinho in nao_visitados:
            if matriz[nodo_atual][vizinho] < float('inf'):  # Apenas se houver conexão direta
                nova_distancia = distancias[nodo_atual] + matriz[nodo_atual][vizinho]
                if nova_distancia < distancias[vizinho]:  # Se a nova distância for menor, atualiza
                    distancias[vizinho] = nova_distancia
                    antecessores[vizinho] = nodo_atual  # Define o nodo atual como antecessor

    return None, float('inf')  # Retorna None se não houver caminho e distância infinita

# Bloco principal do código
if __name__ == "__main__":
    matriz_adjacencia = construir_matriz_adjacencia()  # Gera a matriz de adjacência com as distâncias reais

    # Cálculo da centralidade de grau dos aeroportos
    centralidade = calcular_centralidade_grau()

    # Exibe as centralidades
    print("Centralidade de Grau dos Aeroportos:")
    for aeroporto_id, grau in centralidade.items():
        nome_aeroporto = AeroPortos[aeroporto_id]["nome"]
        codigo = AeroPortos[aeroporto_id]["codigo"]
        print(f"{nome_aeroporto} ({codigo}): {grau} conexões")

    origem, destino = 4, 1  # Exemplo: Salvador (SSA) para Guarulhos (GRU)
    caminho, distancia_total = dijkstra(matriz_adjacencia, origem, destino)  # Executa o algoritmo de Dijkstra

    if caminho:
        print("\nMelhor rota:")
        for i, aeroporto_id in enumerate(caminho):
            nome_aeroporto, codigo = AeroPortos[aeroporto_id]["nome"], AeroPortos[aeroporto_id]["codigo"]
            print(f"{i+1}. {nome_aeroporto} ({codigo})")  # Exibe a sequência de aeroportos na melhor rota
        print(f"Distância total: {distancia_total:.2f} km")  # Exibe a distância total do trajeto
    else:
        print("Nenhuma rota encontrada.")  # Exibe mensagem caso não haja rota disponível
