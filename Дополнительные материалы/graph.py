from math import *


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

        Параметры:
        :param node_id: int -- ID вершины
        :param x: float -- координата вершины по X
        :param y: float -- координата вершины по Y
        """
        if node_id in self.nodes:
            raise ValueError(f"Ребро с ID {node_id} уже существует.")
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

        Параметры:
        :param edge_id: int -- ID ребра
        :param v1_id: int -- ID начальной вершины ребра
        :param v2_id: int -- ID конечной вершины ребра
        :param directed: bool = False -- односторонность ребра (True если ребро ориентированное)
        :param weights: tuple[float] = None -- веса ребра
        """
        if edge_id in self.edges:
            raise ValueError(f"Ребро с ID {edge_id} уже существует в графе.")

        if v1_id not in self.nodes or v2_id not in self.nodes:
            raise ValueError("Одна из вершин не найдена.")

        self.edges[edge_id] = Edge(edge_id, v1_id, v2_id, directed, weights)

    def copy_from(self, other_graph: "Graph"):
        """Копирует заданный граф

        Параметры:
        :param other_graph: other_graph: Graph -- граф, который нужно скопировать
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

        Параметры:
        :param node_id: ID вершины, которую нужно удалить
        """
        if node_id not in self.nodes:
            raise ValueError("Вершина не найдена.")

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

        Параметры:
        :param edge_id: int -- ID ребра, которое нужно удалить
        """
        if edge_id not in self.edges:
            raise ValueError("Вершнина не найдена.")
        del self.edges[edge_id]


def haversine(x1: float, y1: float, x2: float, y2: float) -> float:
    """Формула гаверсинуса
    Находит расстояние между двумя точками (в метрах), с заданными координатами концов

    Параметры:
    :param x1: float -- координата X первой точки
    :param y1: float -- координата Y первой точки
    :param x2: float -- координата X второй точки
    :param y2: float -- координата Y второй точки

    Возвращает length: float -- длина между двумя точками в метрах
    """
    R_earth = 6371000
    rad_1 = radians(y1)
    rad_2 = radians(y2)
    drad = radians(y2 - y1)
    dlambda = radians(x2 - x1)
    a = sin(drad / 2) ** 2 + cos(rad_1) * cos(rad_2) * sin(dlambda / 2) ** 2
    length = 2 * R_earth * atan2(sqrt(a), sqrt(1 - a))
    return length


def graph_from_file(osm_file: str):
    """Функция, преобразовывающая .osm-файл в граф

    Параметры:
    :param osm_file: str -- файл с расширением .osm

    Возвращает graph: Graph -- граф, содержащий сетку дорог
    """
    try:
        import xml.etree.ElementTree as ET
    except Exception:
        raise ImportError("Библиотека xml не установлена.")
    else:
        tree = ET.parse(osm_file)
        root = tree.getroot()
        graph = Graph()

        for node in root.findall("node"):
            node_id = int(node.attrib["id"])
            lon = float(node.attrib["lon"])
            lat = float(node.attrib["lat"])
            graph.add_node(node_id, lon, lat)

        edge_id = 1
        for way in root.findall("way"):
            tags = {tag.attrib["k"]: tag.attrib["v"] for tag in way.findall('tag')}
            oneway = tags.get("oneway", 'no') in ['yes']
            node_refs = [int(nd.attrib['ref']) for nd in way.findall('nd')]
            for k in range(len(node_refs) - 1):
                n1 = node_refs[k]
                n2 = node_refs[k + 1]
                if n1 not in graph.nodes or n2 not in graph.nodes:
                    raise UserWarning("Файл имеет в себе неточности, и как следствие, его невозможно обработать")
                x1, y1 = graph.nodes[n1].coords
                x2, y2 = graph.nodes[n2].coords
                length = haversine(x1, y1, x2, y2)
                graph.add_edge_by_id(edge_id, n1, n2, directed=oneway, weights=tuple([length]))

                edge_id += 1
        return graph
    finally:
        return None

def file_from_place(place:str, path:str='current_folder') -> bool:
    """Функция, сохраняющая карту местности в .osm-файл
    !!! Возможно потребуется VPN для корректной работы !!!

    Параметры:
    :param place: str -- место
    :param path: str = current_folder -- папка, куда сохраняется файл. Если поле не заполнить, то файл сохранится в текущую папку

    Возвращает bool, где True -- успешное сохранение, False -- неуспешное сохранение
    """
    try:
        import osmnx as ox
    except Exception:
        raise ImportError("Библиотека osmnx не установлена. ")
    else:

        G = ox.graph.graph_from_place(place, network_type='all', simplify=False, retain_all = True)
        if path == 'current_folder':
            path = '.'
        try:
            ox.io.save_graph_xml(G, filepath=f'{path}/')
        except Exception:
            raise UserWarning("Указанного пути не существует.")
        else:
            return True
        finally:
            return False
    finally:
        return False

def create_graph_from_place(place, path) -> Graph:
    """Возвращает граф, созданный из данного места

    !!! Возможно требует VPN для корректной работы !!!

    Параметры
    :param place: str -- место, из которого нужно создать граф
    :param path: str -- папка, куда нужно сохранить файл

    Возвращает graph: Graph -- граф, созданный из карты указанного места
    """
    flag = file_from_place(place, path)
    if flag == True:
        graph = graph_from_file(f'{path}/{place}.osm')
        return graph
    else:
        raise UserWarning("Не удалось создать граф из места")