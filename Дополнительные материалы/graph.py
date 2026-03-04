from typing import Tuple, Optional, Dict
import random


class Node:
    def __init__(self, node_id: int, x: float, y: float):
        self.id = node_id
        self.coords = (x, y)

    def __repr__(self):
        return f"Node(id={self.id}, coords={self.coords})"


class Edge:
    def __init__(
        self,
        edge_id: int,
        v1_id: int,
        v2_id: int,
        directed: bool = False,
        weights: Optional[Tuple[float, ...]] = None,
    ):
        self.id = edge_id
        self.v1_id = v1_id
        self.v2_id = v2_id
        self.directed = directed
        self.weights = weights if weights is not None else tuple()

    def __repr__(self):
        return (
            f"Edge(id={self.id}, v1={self.v1_id}, v2={self.v2_id}, "
            f"directed={self.directed}, weights={self.weights})"
        )


class Graph:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.edges: Dict[int, Edge] = {}

    # --- Добавление вершины ---
    def add_node(self, node_id: int, x: float, y: float):
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")
        self.nodes[node_id] = Node(node_id, x, y)

    # --- Добавление ребра по ID ---
    def add_edge_by_id(
        self,
        edge_id: int,
        v1_id: int,
        v2_id: int,
        directed: bool = False,
        weights: Optional[Tuple[float, ...]] = None, # много весов нужно, чтобы на всякий случай хранить вес, время его прохода и другие параметры ребра
    ):
        if edge_id in self.edges:
            raise ValueError(f"Edge with ID {edge_id} already exists.")

        if v1_id not in self.nodes or v2_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph.")

        self.edges[edge_id] = Edge(edge_id, v1_id, v2_id, directed, weights)

    # --- Добавление ребра по вершинам ---
    def add_edge_by_nodes(
        self,
        v1_id: int,
        v2_id: int,
        edge_id: Optional[int] = None,
        directed: bool = False,
        weights: Optional[Tuple[float, ...]] = None,
    ):
        if v1_id not in self.nodes or v2_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph.")

        # Проверяем, есть ли уже такое ребро
        for edge in self.edges.values():
            if (
                edge.v1_id == v1_id
                and edge.v2_id == v2_id
                and edge.directed == directed
            ):
                return edge  # уже существует

            if (
                not directed
                and not edge.directed
                and edge.v1_id == v2_id
                and edge.v2_id == v1_id
            ):
                return edge

        # Если ID не передан — генерируем
        if edge_id is None:
            edge_id = max(self.edges.keys(), default=0) + 1

        if edge_id in self.edges:
            raise ValueError("Edge ID already exists.")

        edge = Edge(edge_id, v1_id, v2_id, directed, weights)
        self.edges[edge_id] = edge
        return edge

    # --- Копирование графа ---
    def copy_from(self, other_graph: "Graph"):
        self.nodes = {
            node_id: Node(node.id, *node.coords)
            for node_id, node in other_graph.nodes.items()
        }
        self.edges = {
            edge_id: Edge(
                edge.id,
                edge.v1_id,
                edge.v2_id,
                edge.directed,
                edge.weights,
            )
            for edge_id, edge in other_graph.edges.items()
        }

    # --- Удаление вершины ---
    def remove_node(self, node_id: int):
        if node_id not in self.nodes:
            raise ValueError("Node not found.")

        # Удаляем все связанные рёбра
        edges_to_delete = [
            edge_id
            for edge_id, edge in self.edges.items()
            if edge.v1_id == node_id or edge.v2_id == node_id
        ]
        for edge_id in edges_to_delete:
            del self.edges[edge_id]

        del self.nodes[node_id]

    # --- Удаление ребра ---
    def remove_edge(self, edge_id: int):
        if edge_id not in self.edges:
            raise ValueError("Edge not found.")
        del self.edges[edge_id]
