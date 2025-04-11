import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

def crear_grafo(matriz_def, matriz_detalle, ruta_guardado):
    
    """
    Crea un grafo bidimensional donde:
    - matriz_def[i][j] = True/False (indica si el nodo existe)
    - matriz_detalle[i][j] = [tipo, subtipo] (define el color y detalles)
    """
    matriz_def = np.array(matriz_def)
    matriz_detalle = np.array(matriz_detalle, dtype=object)  # Para manejar listas anidadas

    filas, columnas = matriz_def.shape

    # Crear grafo
    G = nx.Graph()
    fig, ax = plt.subplots(figsize=(10, 8))

    # Mapeo de tipos a colores (basado en el primer elemento de matriz_detalle[i][j])
    tipo_a_color = {
        0: "red",     # tomate
        1: "green",   # pimiento
        2: "blue",    # patata
        3: "yellow"   # desconocido
    }

    # Añadir nodo "Inicio" (centrado en la parte superior)
    G.add_node("Inicio", pos=(columnas // 2, filas + 1))

    # Añadir nodos de la matriz y conexiones
    node_colors = []
    node_labels = {}  # Para etiquetas personalizadas (opcional)
    for i in range(filas):
        for j in range(columnas):
            if matriz_def[i][j]:
                node_name = f"({i},{j})"
                pos = (j, -i)  # Coordenadas (x, y)
                G.add_node(node_name, pos=pos)
                
                # Asignar color según el primer elemento de matriz_detalle[i][j]
                tipo = matriz_detalle[i][j][0]  # Primer valor de la lista
                node_colors.append(tipo_a_color.get(tipo, "yellow"))
                
                # Opcional: Usar el segundo valor para etiquetas
                subtipo = matriz_detalle[i][j][1]
                node_labels[node_name] = f"{tipo},{subtipo}"  # Ej: "2,2"

                # Conectar con Inicio (distancia euclidiana)
                distancia = math.hypot(j - columnas/2, i + 1)
                G.add_edge("Inicio", node_name, weight=distancia)

    # Conectar nodos adyacentes (horizontal y vertical)
    for i in range(filas):
        for j in range(columnas):
            if matriz_def[i][j]:
                node_name = f"({i},{j})"
                # Vecinos: arriba, abajo, izquierda, derecha
                vecinos = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in vecinos:
                    if 0 <= ni < filas and 0 <= nj < columnas and matriz_def[ni][nj]:
                        vecino_name = f"({ni},{nj})"
                        distancia = 1  # Distancia entre adyacentes
                        G.add_edge(node_name, vecino_name, weight=distancia)

    # Dibujar el grafo
    pos = nx.get_node_attributes(G, 'pos')
    default_labels = {node: node if node != "Inicio" else "Inicio" for node in G.nodes()}
    
    # Combinar etiquetas personalizadas (opcional)
    labels = {**default_labels, **node_labels}
    
    # Asegurar que "Inicio" tenga color gris
    node_colors_with_start = ["gray"] + node_colors
    
    nx.draw(
        G, pos, labels=labels, ax=ax,
        node_size=800,
        node_color=node_colors_with_start,
        font_size=8,
        font_weight="bold"
    )

    # Calcular rutas más cortas desde Inicio
    try:
        caminos = nx.single_source_dijkstra_path(G, "Inicio")
        distancias = nx.single_source_dijkstra_path_length(G, "Inicio")
        print("\nRutas más cortas desde Inicio:")
        distancia = []
        for nodo, camino in caminos.items():
            print(f"{nodo}: {camino} (Distancia: {distancias[nodo]:.2f})")
            distancia.append(distancias[nodo])
    except nx.NodeNotFound:
        print("El nodo 'Inicio' no existe en el grafo.")

    plt.title("Grafo de cultivos (3D)")
    plt.tight_layout()
    fig.patch.set_facecolor('#4A6350') 
    plt.savefig(f"{ruta_guardado}/grafo_cultivos.png")
    return distancia