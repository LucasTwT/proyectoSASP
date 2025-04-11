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
    
    # Crear etiquetas sin la etiqueta de "Inicio" (para evitar la "letra rara")
    labels = {node: node_labels.get(node, node) for node in G.nodes() if node != "Inicio"}

    # Asegurar que "Inicio" tenga color gris
    node_colors_with_start = ["gray"] + node_colors
    
    # Dibujar los nodos
    nx.draw_networkx_nodes(
        G, pos, nodelist=[node for node in G.nodes if node != "Inicio"],
        node_size=800, node_color=node_colors_with_start[1:]
    )
    
    # Dibujar el nodo de inicio con tamaño y color personalizado
    nx.draw_networkx_nodes(
        G, pos, nodelist=["Inicio"],
        node_size=2000, node_color="gray"  # Nodo de inicio con tamaño mayor y color rojo
    )

    # Dibujar las aristas (líneas)
    nx.draw_networkx_edges(
        G, pos, edge_color="#FFB74D"  # Línea de color naranja claro
    )

    # Etiquetas de los nodos, con "Inicio" en un tamaño y color diferente
    nx.draw_networkx_labels(
        G, pos, labels=labels,
        font_size=8, font_color="white", font_weight="bold"
    )
    
    # Etiqueta especial para "Inicio"
    nx.draw_networkx_labels(
        G, pos, labels={"Inicio": "Inicio"},
        font_size=12, font_color="white", font_weight="bold"  # Etiqueta con tamaño mayor y color amarillo
    )

    # Fondo oscuro
    fig.patch.set_facecolor('#0F1B12') 
    ax.set_facecolor('#0F1B12')  # Asegurar que el fondo del gráfico también sea oscuro
    plt.axis("off")
    
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

    # Mostrar título
    plt.title("Grafo de cultivos (3D)", weight='bold', color="white", style='italic', fontsize=20)
    plt.tight_layout()

    # Guardar la imagen
    plt.savefig(f"{ruta_guardado}/grafo_cultivos.png")
    return distancia
