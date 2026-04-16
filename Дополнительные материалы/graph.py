

class Node:
    """Вершина графа

        Параметры:
        node_id: int, ID вершины
        x: float, координата вершины по X
        y: float, координата вершины по Y
        """
    def __init__(self, node_id: int, x: float, y: float):
        self.id = node_id
        self.coords = (x, y)

    def __repr__(self):
        return f"Node(id={self.id}, coords={self.coords})"


class Edge:
    """Ребро графа

        Параметры:
            node_id: int, ID ребра
            v1_id: int, ID вершины начала ребра
            v2_id: int, ID вершины конца ребра
            directed: bool = False, направление ребра (по умолчанию не ориентировано)
            weights = tuple[float] = None, веса вершин
            """
    def __init__(
            self,
            edge_id: int,
            v1_id: int,
            v2_id: int,
            directed: bool = False,
            weights: tuple[float] = None,
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
    """
    Класс графа

    Функции:
    add_node(node_id: int, x: float, y: float) -- добавление вершины
    add_edge(edge_id: int, v1_id: int, v2_id: int, ...) -- создание ребра и добавление его в граф
    copy_from(other_graph: Graph) -- копирование графа
    remove_node(node_id: int) -- удаление вершины из графа
    remove_edge(edge_id: int) -- удаление ребра из графа
    """
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()

    # --- Добавление вершины ---
    def add_node(self, node_id: int, x: float, y: float):
        """Создаёт вершину и добавляет её в граф.
        Если ID вершины уже занят, то вызывает ValueError

        :param node_id: int -- ID вершины
        :param x: float -- координата вершины по X
        :param y: float -- координата вершины по Y
        :return: None
        """
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")
        self.nodes[node_id] = Node(node_id, x, y)


    def add_edge_by_id(
            self,
            edge_id: int,
            v1_id: int,
            v2_id: int,
            directed: bool = False,
            weights: tuple[float] = None,
    ):
        """Создаёт ребро с заданным ID и помещает его в граф
        Если одна из вершин отсутствует в графе или ID уже занято другим ребром, то вызывает ValueError

        :param edge_id: int -- ID ребра
        :param v1_id: int -- ID начальной вершины ребра
        :param v2_id: int -- ID конечной вершины ребра
        :param directed: bool = False -- односторонность ребра (True если ребро ориентированное)
        :param weights: tuple[float] = None -- веса ребра
        :return: None
        """
        if edge_id in self.edges:
            raise ValueError(f"Edge with ID {edge_id} already exists.")

        if v1_id not in self.nodes or v2_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph.")

        self.edges[edge_id] = Edge(edge_id, v1_id, v2_id, directed, weights)


    def copy_from(self, other_graph: "Graph"):
        """Копирует заданный граф

        :param other_graph: other_graph: Graph -- граф, который нужно скопировать
        :return: None
        """
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

    def remove_node(self, node_id: int):
        """Удаляет вершину и все прилегающие к ней рёбра в вершине.
        Вызывает ValueError, если вершины нет в графе

        :param node_id:
        :return:
        """
        if node_id not in self.nodes:
            raise ValueError("Node not found.")

        edges_to_delete = [
            edge_id
            for edge_id, edge in self.edges.items()
            if edge.v1_id == node_id or edge.v2_id == node_id
        ]
        for edge_id in edges_to_delete:
            del self.edges[edge_id]

        del self.nodes[node_id]

    def remove_edge(self, edge_id: int):
        """Удаляет ребро из графа
        Вызывает ValueError, если ребра нет в графе

        :param edge_id: int -- ID ребра, которое нужно удалить
        :return: None
        """
        if edge_id not in self.edges:
            raise ValueError("Edge not found.")
        del self.edges[edge_id]
