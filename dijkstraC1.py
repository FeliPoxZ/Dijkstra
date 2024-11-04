import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

# Tempo de transmissão são os pesos das arestas em ms de 30ms até 1500ms

G = nx.Graph()

dispositivos = {
    1: "roteador",
    2: "switch 1",
    3: "switch 2",
    4: "servidor 1",
    5: "servidor 2",
    6: "servidor 3",
    7: "servidor 4",
    8: "servidor 5",
    9: "servidor 6",
}

for id, nome in dispositivos.items():
    G.add_node(id, name=nome)

arestas = []

for i in range(2, len(dispositivos) + 1):
    # Adiciona uma aresta entre o nó atual e um nó anterior aleatório
    arestas.append((random.choice(range(1, i)), i))

for aresta in arestas:
    peso = random.randint(30, 1500)
    G.add_edge(aresta[0], aresta[1], weight=peso)


arestas_existentes = set()

# Gera arestas adicionais aleatórias 
num_arestas_aleatorias = len(dispositivos) * 2

while num_arestas_aleatorias > 0:
    u = random.choice(list(G.nodes()))
    v = random.choice(list(G.nodes()))

    # Verifica se u e v são diferentes e se a aresta não existe
    if u != v:
        # Cria uma tupla ordenada para a aresta
        aresta = (min(u, v), max(u, v))
        if aresta not in arestas_existentes:

            peso = random.randint(30, 1500)

            G.add_edge(u, v, weight=peso)

            arestas_existentes.add(aresta)  # Adiciona a aresta ao conjunto

            num_arestas_aleatorias -= 1

rotulos = nx.get_node_attributes(G, 'name')
rotulos_pesos = nx.get_edge_attributes(G, 'weight')




origem = int(input('Informe o dispotivo de origem dos dados: '))

if (origem > 9 or origem < 1):
    print("Não há este dispositivo na rede")
    sys.exit()


destino = int(input('Informe o dispotivo de destino dos dados: '))

if (destino > 9 or origem < 1):
    print("Não há este dispositivo na rede")
    sys.exit()


caminho_mais_curto = nx.dijkstra_path(G, origem, destino)
tamaho_caminho_mais_curto = nx.dijkstra_path_length(G, origem, destino)

print(f"Caminho mais curto de {rotulos[origem]} para {rotulos[destino]}: {caminho_mais_curto}")
print(f"Tempo total da transferencia de dados foi de: {tamaho_caminho_mais_curto}ms")

pos = nx.spring_layout(G, k=2.5)  # Aumente o valor de k para mais espaçamento

cores_arestas = ['blue'] * G.number_of_edges()
larguras = [1] * G.number_of_edges()

for u, v in zip(caminho_mais_curto[:-1], caminho_mais_curto[1:]):
    if G.has_edge(u, v):
        index = list(G.edges()).index((min(u, v), max(u, v)))
        cores_arestas[index] = 'red'  # Cor do caminho mais curto
        larguras[index] = 3  # Largura do caminho mais curto

cores_nos = ['green'] * G.number_of_nodes()
for node in caminho_mais_curto:
    cores_nos[node - 1] = 'red'

plt.figure(figsize=(12, 8))  # Largura de 12 polegadas e altura de 8 polegadas

nx.draw(G, pos, with_labels=True, labels=rotulos, node_size=2000, node_color=cores_nos, font_color='black', font_size=8)
nx.draw_networkx_edges(G, pos, edge_color=cores_arestas, width=larguras)

# Ajustar a posição dos rótulos das arestas
edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=rotulos_pesos)

# Ajustar a posição vertical dos rótulos
for (u, v), label in edge_labels.items():
    x = (pos [u][0] + pos[v][0]) / 2
    y = (pos[u][1] + pos[v][1]) / 2
    label.set_position((x, y + 0.01))  # Aumentar a altura do rótulo

plt.text(0, -1.1, "As arestas representam o tempo de transmissão de dados em ms.", ha='center', va='top', fontsize=10)
plt.text(0, -1.2, f"O total de tempo necessário do caminho mais curto escolhido foi: {tamaho_caminho_mais_curto}ms", ha='center', va='top', fontsize=10)

# Ajustar limites para garantir que o texto apareça
plt.ylim(-1.3, 1.5)  # Aumente a parte inferior para dar espaço ao texto


print(G.edges)

plt.show()