from graph import *
import heapq
from typing import Dict, Union, List
import math


def dijkstra(graph: Graph, start_node_id: int, return_path: bool = False, index = 0) -> Union[Dict[int, float], Dict[int, List[int]]]:
    if start_node_id not in graph.nodes:
        raise ValueError("Start node not found in graph.")

    # Инициализация расстояний
    distances = {node_id: float("inf") for node_id in graph.nodes}
    distances[start_node_id] = 0

    # Для восстановления путей
    previous = {node_id: None for node_id in graph.nodes}

    # Очередь с приоритетом (min-heap)
    priority_queue = [(0, start_node_id)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        # Перебор всех рёбер
        for edge in graph.edges.values():

            weight = edge.weights[index] if edge.weights else 1  # если весов нет — считаем 1

            # Ориентированное ребро
            if edge.directed:
                if edge.v1_id == current_node:
                    neighbor = edge.v2_id
                else:
                    continue
            # Неориентированное
            else:
                if edge.v1_id == current_node:
                    neighbor = edge.v2_id
                elif edge.v2_id == current_node:
                    neighbor = edge.v1_id
                else:
                    continue

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if not return_path:
        return distances

    # Восстановление путей
    paths = {}

    for node_id in graph.nodes:
        if distances[node_id] == float("inf"):
            paths[node_id] = []
            continue

        path = []
        current = node_id
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        paths[node_id] = path

    return paths


def a_star(
    graph: Graph,
    start_node_id: int,
    goal_node_id: int,
    return_path: bool = True,
) -> Union[List[int], float]:

    if start_node_id not in graph.nodes or goal_node_id not in graph.nodes:
        raise ValueError("Start or goal node not found in graph.")

    # --- эвристика: евклидово расстояние ---
    def heuristic(n1: int, n2: int) -> float:
        x1, y1 = graph.nodes[n1].coords
        x2, y2 = graph.nodes[n2].coords
        return math.hypot(x2 - x1, y2 - y1)

    open_set = []
    heapq.heappush(open_set, (0, start_node_id))

    g_score: Dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    g_score[start_node_id] = 0

    f_score: Dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    f_score[start_node_id] = heuristic(start_node_id, goal_node_id)

    previous: Dict[int, int] = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal_node_id:
            if not return_path:
                return g_score[current]

            # восстановление пути
            path = [current]
            while current in previous:
                current = previous[current]
                path.append(current)
            path.reverse()
            return path

        # перебор соседей через рёбра
        for edge in graph.edges.values():

            weight = edge.weights[0] if edge.weights else 1

            # ориентированное
            if edge.directed:
                if edge.v1_id == current:
                    neighbor = edge.v2_id
                else:
                    continue
            # неориентированное
            else:
                if edge.v1_id == current:
                    neighbor = edge.v2_id
                elif edge.v2_id == current:
                    neighbor = edge.v1_id
                else:
                    continue

            tentative_g = g_score[current] + weight

            if tentative_g < g_score[neighbor]:
                previous[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(
                    neighbor, goal_node_id
                )
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # если путь не найден
    if return_path:
        return []
    return float("inf")




class Vehicle:
    def __init__(self, start_node_id: int):
        self.current_node = start_node_id
        self.previous_node: Optional[int] = None
        self.time_elapsed = 0.0
        self.progress = 0.0
        self.edge = None

    def __repr__(self):
        return (
            f"Vehicle(current={self.current_node}, "
            f"previous={self.previous_node}, "
            f"time={self.time_elapsed})"
        )

def manhattan_step(graph: Graph, vehicle: Vehicle) -> None:
    """
    Один шаг движения машины.
    Машина:
    - равновероятно выбирает дорогу
    - не может ехать туда, откуда приехала
    - если тупик — возвращается
    - время движения берётся из Edge.weights[0]
    """

    current = vehicle.current_node
    prev = vehicle.previous_node

    # --- поиск доступных соседей ---
    neighbors = []

    for edge in graph.edges.values():

        weight = edge.weights[0] if edge.weights else 1

        # ориентированное ребро
        if edge.directed:
            if edge.v1_id == current:
                neighbor = edge.v2_id
            else:
                continue

        # неориентированное
        else:
            if edge.v1_id == current:
                neighbor = edge.v2_id
            elif edge.v2_id == current:
                neighbor = edge.v1_id
            else:
                continue

        neighbors.append((neighbor, weight))

    if not neighbors:
        return  # изолированная вершина

    # --- убираем дорогу, откуда приехали ---
    filtered = [n for n in neighbors if n[0] != prev]

    # --- если тупик ---
    if not filtered:
        # возвращаемся назад
        next_node = prev
        # ищем вес обратного ребра
        for edge in graph.edges.values():
            if (
                not edge.directed
                and (
                    (edge.v1_id == current and edge.v2_id == prev)
                    or (edge.v2_id == current and edge.v1_id == prev)
                )
            ):
                weight = edge.weights[0] if edge.weights else 1
                break
        else:
            weight = 1

    else:
        # равновероятный выбор
        next_node, weight = random.choice(filtered)

    # --- обновляем состояние машины ---
    vehicle.previous_node = current
    vehicle.current_node = next_node
    vehicle.time_elapsed += weight

def simulate_manhattan(graph: Graph, start_node: int, steps: int):
    vehicle = Vehicle(start_node)

    history = [start_node]

    for _ in range(steps):
        manhattan_step(graph, vehicle)
        history.append(vehicle.current_node)

    return history, vehicle.time_elapsed

def simulate_manhattan_vehicles(
    graph: Graph,
    start_nodes: list[int],
    steps: int,
):
    vehicles = [Vehicle(start) for start in start_nodes]

    history = {i: [v.current_node] for i, v in enumerate(vehicles)}

    for _ in range(steps):
        for i, vehicle in enumerate(vehicles):
            manhattan_step(graph, vehicle)
            history[i].append(vehicle.current_node)

    total_times = {i: v.time_elapsed for i, v in enumerate(vehicles)}

    return history, total_times


class NaSchVehicle(Vehicle):
    def __init__(self, start_node_id: int, vmax: int = 5):
        super().__init__(start_node_id)
        self.v = 0
        self.vmax = vmax
        self.next_node = None  # куда планирует ехать


class NaSchSimulation:
    def __init__(self, graph: Graph, p_slow: float = 0.2):
        self.graph = graph
        self.vehicles: list[NaSchVehicle] = []
        self.p_slow = p_slow  # вероятность случайного торможения

    def add_vehicle(self, start_node: int, vmax: int = 5):
        if start_node not in self.graph.nodes:
            raise ValueError("Node not in graph.")
        self.vehicles.append(NaSchVehicle(start_node, vmax))

    def neighbors(self, node_id: int):
        result = []
        for edge in self.graph.edges.values():

            # вес = 1 по условию
            if edge.directed:
                if edge.v1_id == node_id:
                    result.append(edge.v2_id)
            else:
                if edge.v1_id == node_id:
                    result.append(edge.v2_id)
                elif edge.v2_id == node_id:
                    result.append(edge.v1_id)

        return result

    def step(self):

        # --- 1. Ускорение ---
        for car in self.vehicles:
            car.v = min(car.v + 1, car.vmax)

        # --- 2. Выбор направления (манхэттенская логика) ---
        for car in self.vehicles:
            neigh = self.neighbors(car.current_node)

            if car.previous_node is not None and len(neigh) > 1:
                neigh = [n for n in neigh if n != car.previous_node]

            if not neigh:
                neigh = [car.previous_node]

            car.next_node = random.choice(neigh)

        # --- 3. Проверка дистанции (предотвращение столкновений) ---
        occupied = {car.current_node for car in self.vehicles}

        for car in self.vehicles:
            if car.next_node in occupied:
                car.v = 0

        # --- 4. Случайное торможение ---
        for car in self.vehicles:
            if car.v > 0 and random.random() < self.p_slow:
                car.v -= 1

        # --- 5. Конфликт "помеха справа" ---
        # группируем машины по целевой вершине
        conflicts = {}
        for car in self.vehicles:
            if car.v > 0:
                conflicts.setdefault(car.next_node, []).append(car)

        for node, cars in conflicts.items():
            if len(cars) > 1:

                # упорядочим по "правилу справа"
                # приближение: по углу входа
                def angle(car):
                    x0, y0 = self.graph.nodes[car.previous_node].coords
                    x1, y1 = self.graph.nodes[car.current_node].coords
                    dx, dy = x1 - x0, y1 - y0
                    return (dx, dy)

                cars.sort(key=angle)

                # первый — справа, остальные тормозят
                winner = cars[0]
                for c in cars[1:]:
                    c.v = 0

        # --- 6. Движение ---
        for car in self.vehicles:
            if car.v > 0:
                car.previous_node = car.current_node
                car.current_node = car.next_node

    def run(self, steps: int):
        history = []

        for _ in range(steps):
            self.step()
            history.append([car.current_node for car in self.vehicles])

        return history

