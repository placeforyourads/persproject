from algorhythms import *
def choose_next_edge(graph: Graph, vehicle: Vehicle):
    current = vehicle.current_node
    prev = vehicle.previous_node

    candidates = []

    for edge in graph.edges.values():

        if edge.directed:
            if edge.v1_id == current:
                candidates.append(edge)

        else:
            if edge.v1_id == current or edge.v2_id == current:
                candidates.append(edge)

    # убираем дорогу, откуда приехали
    filtered = []
    for e in candidates:
        other = e.v2_id if e.v1_id == current else e.v1_id
        if other != prev:
            filtered.append(e)

    if not filtered:
        filtered = candidates

    return random.choice(filtered)

def vehicle_step(graph: Graph, vehicle: Vehicle, dt=0.05):

    # если машина стоит в узле — выбираем ребро
    if vehicle.edge is None:

        edge = choose_next_edge(graph, vehicle)

        vehicle.edge = edge
        vehicle.progress = 0.0
        vehicle.previous_node = vehicle.current_node

    # движение по ребру
    weight = vehicle.edge.weights[0] if vehicle.edge.weights else 1

    vehicle.progress += dt / weight

    if vehicle.progress >= 1.0:

        # приехали в следующий узел
        if vehicle.edge.v1_id == vehicle.previous_node:
            vehicle.current_node = vehicle.edge.v2_id
        else:
            vehicle.current_node = vehicle.edge.v1_id

        vehicle.edge = None
        vehicle.progress = 0.0

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(graph: Graph, vehicles: list[Vehicle]):

    fig, ax = plt.subplots()

    # рисуем дороги
    for edge in graph.edges.values():
        n1 = graph.nodes[edge.v1_id]
        n2 = graph.nodes[edge.v2_id]

        ax.plot(
            [n1.coords[0], n2.coords[0]],
            [n1.coords[1], n2.coords[1]],
            color="black"
        )

    # машины
    colors = [plt.cm.tab10(i) for i in range(len(vehicles))]
    points = [ax.plot([], [], 'o', color=c)[0] for c in colors]

    def update(frame):

        for v in vehicles:
            vehicle_step(graph, v)

        for i, v in enumerate(vehicles):
            x, y = vehicle_position(graph, v)
            points[i].set_data([x], [y])

        return points

    ax.set_aspect("equal")

    anim = FuncAnimation(fig, update, frames=500, interval=50)

    plt.show()



def choose_manhattan_edge(graph: Graph, vehicle: Vehicle):

    current = vehicle.current_node
    prev = vehicle.previous_node

    neighbors = []

    for edge in graph.edges.values():

        if edge.directed:
            if edge.v1_id == current:
                neighbor = edge.v2_id
            else:
                continue

        else:
            if edge.v1_id == current:
                neighbor = edge.v2_id
            elif edge.v2_id == current:
                neighbor = edge.v1_id
            else:
                continue

        neighbors.append((edge, neighbor))

    if not neighbors:
        return None

    # убираем дорогу, откуда приехали
    filtered = [n for n in neighbors if n[1] != prev]

    # если тупик
    if not filtered:
        filtered = neighbors

    edge, _ = random.choice(filtered)
    return edge

def vehicle_step(graph: Graph, vehicle: Vehicle, dt=0.05):

    # если машина в узле — выбираем дорогу
    if vehicle.edge is None:

        edge = choose_manhattan_edge(graph, vehicle)

        if edge is None:
            return

        vehicle.edge = edge
        vehicle.progress = 0.0
        vehicle.previous_node = vehicle.current_node

    # движение по ребру
    weight = vehicle.edge.weights[0] if vehicle.edge.weights else 1

    vehicle.progress += dt / weight
    vehicle.time_elapsed += dt

    if vehicle.progress >= 1.0:

        if vehicle.edge.v1_id == vehicle.previous_node:
            vehicle.current_node = vehicle.edge.v2_id
        else:
            vehicle.current_node = vehicle.edge.v1_id

        vehicle.edge = None
        vehicle.progress = 0.0

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


def animate(graph: Graph, vehicles):

    fig, ax = plt.subplots()

    for edge in graph.edges.values():
        n1 = graph.nodes[edge.v1_id]
        n2 = graph.nodes[edge.v2_id]

        ax.plot(
            [n1.coords[0], n2.coords[0]],
            [n1.coords[1], n2.coords[1]],
            color="black"
        )

    points = [ax.plot([], [], 'o')[0] for _ in vehicles]

    def update(frame):

        for v in vehicles:
            vehicle_step(graph, v)

        for i, v in enumerate(vehicles):
            x, y = vehicle_position(graph, v)
            points[i].set_data([x], [y])

        return points

    ax.set_aspect("equal")

    anim = FuncAnimation(fig, update, interval=50)

    plt.show()

def vehicle_position(graph: Graph, vehicle: Vehicle):

    if vehicle.edge is None:
        return graph.nodes[vehicle.current_node].coords

    n1 = graph.nodes[vehicle.edge.v1_id]
    n2 = graph.nodes[vehicle.edge.v2_id]

    x1, y1 = n1.coords
    x2, y2 = n2.coords

    t = vehicle.progress

    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    return x, y