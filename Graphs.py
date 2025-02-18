import math

# Definição dos aeroportos
AeroPortos = {
    1: {"nome": "Guarulhos", "codigo": "GRU", "latitude": -23.4356, "longitude": -46.4731},
    2: {"nome": "Galeão", "codigo": "GIG", "latitude": -22.8089, "longitude": -43.2437},
    3: {"nome": "Brasília", "codigo": "BSB", "latitude": -15.869, "longitude": -47.9292},
    4: {"nome": "Salvador", "codigo": "SSA", "latitude": -12.9115, "longitude": -38.322},
    5: {"nome": "Confins", "codigo": "CNF", "latitude": -19.6339, "longitude": -43.9692}
}
# Definição das conexões diretas (arestas do grafo)
Rotas = {
    1: [2, 3, 5],   # Guarulhos (GRU) tem voos diretos para Galeão, Brasília e Confins
    2: [1, 4],      # Galeão (GIG) tem voos diretos para Guarulhos e Salvador
    3: [1, 4, 5],   # Brasília (BSB) tem voos diretos para Guarulhos, Salvador e Confins
    4: [2, 3, 5],   # Salvador (SSA) tem voos diretos para Galeão, Brasília e Confins
    5: [1, 3, 4]    # Confins (CNF) tem voos diretos para Guarulhos, Brasília e Salvador
}

# Função de cálculo da distância usando Haversine
def calculo_haversine(id1, id2):
    Raio_Terra = 6371  # Raio médio da Terra em km
    lat1, lon1 = math.radians(AeroPortos[id1]["latitude"]), math.radians(AeroPortos[id1]["longitude"])
    lat2, lon2 = math.radians(AeroPortos[id2]["latitude"]), math.radians(AeroPortos[id2]["longitude"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return Raio_Terra * c  # Distância em km

# Construção da matriz de adjacência considerando apenas conexões diretas
def construir_matriz_adjacencia():
    ids = list(AeroPortos.keys())
    n = len(ids)
    matriz = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        matriz[i][i] = 0  # Distância de um aeroporto para ele mesmo é 0

    for origem in Rotas:
        for destino in Rotas[origem]:
            matriz[origem - 1][destino - 1] = calculo_haversine(origem, destino)

    return matriz

# Algoritmo de Dijkstra para encontrar o caminho mais curto
def dijkstra(matriz, origem, destino):
    ids = list(AeroPortos.keys())
    origem_idx, destino_idx = ids.index(origem), ids.index(destino)
    
    n = len(ids)
    distancias = [float('inf')] * n
    distancias[origem_idx] = 0
    nao_visitados = set(range(n))
    antecessores = [-1] * n

    while nao_visitados:
        nodo_atual = min(nao_visitados, key=lambda idx: distancias[idx])

        if nodo_atual == destino_idx:
            caminho, idx = [], destino_idx
            while idx != -1:
                caminho.insert(0, ids[idx])
                idx = antecessores[idx]
            return caminho, distancias[destino_idx]

        nao_visitados.remove(nodo_atual)

        for vizinho in nao_visitados:
            if matriz[nodo_atual][vizinho] < float('inf'):  # Apenas para conexões existentes
                nova_distancia = distancias[nodo_atual] + matriz[nodo_atual][vizinho]
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    antecessores[vizinho] = nodo_atual

    return None, float('inf')

# Bloco principal
if __name__ == "__main__":
    matriz_adjacencia = construir_matriz_adjacencia()
    origem, destino =  4,1  # Exemplo: Guarulhos (GRU) para Salvador (SSA)
    caminho, distancia_total = dijkstra(matriz_adjacencia, origem, destino)

    if caminho:
        print("Melhor rota:")
        for i, aeroporto_id in enumerate(caminho):
            nome_aeroporto, codigo = AeroPortos[aeroporto_id]["nome"], AeroPortos[aeroporto_id]["codigo"]
            print(f"{i+1}. {nome_aeroporto} ({codigo})")
        print(f"Distância total: {distancia_total:.2f} km")
    else:
        print("Nenhuma rota encontrada.")
