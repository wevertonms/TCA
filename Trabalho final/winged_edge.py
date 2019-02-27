"""Estrutura de dados geométrica winged-edge."""

from dataclasses import dataclass

import holoviews as hv
import pandas as pd
from bokeh.models import HoverTool

hv.extension("bokeh", logo=False)


@dataclass
class Vertex:
    """Classe que representa um vértice na estrutura winged-edge."""

    id: int
    coords: list
    edge: int


@dataclass
class Face:
    """Classe que representa uma face na estrutura winged-edge."""

    id: int  # Identificador
    edge: int  # Aresta adjacente


@dataclass
class Edge:
    """Classe que representa uma aresta na estrutura winged-edge."""

    id: int  # Identificador
    v1: int  # Vértice 1
    v2: int  # Vértice 2
    fccw: int = None  # Face adjacente no sentido anti-horário
    fcw: int = None  # Face adjacente no sentido horário
    pccw: int = None  # Aresta anterior no sentido anti-horário
    nccw: int = None  # Próxima aresta no sentido  anti-horário
    pcw: int = None  # Aresta anterior no sentido horário
    ncw: int = None  # Próxima aresta no sentido  horário

    def __eq__(self, other):
        return any(
            [
                self.v1 == other.v1 and self.v2 == other.v2,
                self.v2 == other.v1 and self.v1 == other.v2,
            ]
        )


@dataclass
class WingedEdge:
    """Classe que a estrutura winged-edge."""

    vertices: int
    faces: int
    edges: int

    def get_face_vertices(self, faceID):
        """Retorna os vértices de uma face.
        
        Args:
            faceID (int): ID da face.
        
        Returns:
            list[int]: lista de vertíces.
        """
        face = self.faces[faceID]
        vertex_list = []
        next_edge = self.edges[face.edge]
        while True:
            if next_edge.fccw == faceID:
                vertex_list.append(next_edge.v1)
                next_edge = self.edges[next_edge.nccw]
            else:
                vertex_list.append(next_edge.v2)
                next_edge = self.edges[next_edge.pcw]
            if next_edge.id == face.edge:
                break
        return vertex_list

    def get_face_edges(self, faceID):
        """Retorna as arestas de uma face em sentido anti-horário.
        
        Args:
            faceID (int): ID da face.
        
        Returns:
            list[int]: lista de vertíces.
        """
        edge_list = [self.faces[faceID].edge]
        while True:
            current_edge = self.edges[edge_list[-1]]
            if current_edge.fccw == faceID:
                edge_list.append(current_edge.nccw)
            else:
                edge_list.append(current_edge.pcw)
            if edge_list[-1] == edge_list[0]:
                edge_list.pop()
                break
        return edge_list

    def get_next_vertex(self, vertexID):
        """Retorna o próximo vértice a um dado vértice no sentido .
        
        Args:
            vertexID (int): ID do vértice.
        
        Returns:
            int: ID do vértice.
        """
        vertex_list = []
        V = self.vertices[vertexID]
        A = self.edges[V.edge]
        next_edge = self.edges[V.edge]
        while True:
            if V.id == next_edge.v1:
                vertex_list.append(next_edge.v2)
                if next_edge.pccw != None:
                    next_edge = self.edges[next_edge.pccw]
                else:
                    break
            else:
                vertex_list.append(next_edge.v1)
                if next_edge.pcw != None:
                    next_edge = self.edges[next_edge.pcw]
                else:
                    break
            if next_edge.id == A.id:
                break
        return vertex_list

    def plot_vertices(self):
        """Plot os vértices da estrutura."""
        data = {"id": [], "x": [], "y": []}
        for point in self.vertices:
            data["id"].append(point.id)
            data["x"].append(point.coords[0])
            data["y"].append(point.coords[1])
        data = pd.DataFrame(data)
        tooltips = [("id", "@id"), ("(x,y)", "(@x, @y)")]
        hover = [HoverTool(tooltips=tooltips)]
        max_x, min_x = max(data["x"]), min(data["x"])
        max_y, min_y = max(data["y"]), min(data["y"])
        xlim = (min_x - (max_x - min_x) / 10, max_x + (max_x - min_x) / 10)
        ylim = (min_y - (max_y - min_y) / 10, max_y + (max_y - min_y) / 10)
        return hv.Points(data, ["x", "y"], label="Vértices").opts(
            size=5, color="black", tools=hover, xlim=xlim, ylim=ylim, show_grid=True
        )

    def plot_faces(self):
        """Plot as faces da estrutura."""
        faces_plot = hv.Curve(data=None)
        for face in self.faces:
            vertices = self.get_face_vertices(face.id)
            data = {"x": [], "y": []}
            for vertex_id in [*vertices, vertices[0]]:
                coords = self.vertices[vertex_id].coords
                data["x"].append(coords[0])
                data["y"].append(coords[1])
            faces_plot *= hv.Curve(data, "x", "y", label=f"Face {face.id}")
        return faces_plot

    def plot_edges(self, label=True):
        """Plota as arestas da estrutura."""
        edges_plot = hv.Curve(data=None)
        for edge in self.edges:
            coords1 = self.vertices[edge.v1].coords
            coords2 = self.vertices[edge.v2].coords
            data = {"x": [coords1[0], coords2[0]], "y": [coords1[1], coords2[1]]}
            if label:
                edges_plot *= hv.Curve(data, "x", "y", label=f"Aresta {edge.id}")
            else:
                edges_plot *= hv.Curve(data, "x", "y")
        return edges_plot


if __name__ == "__main__":
    v = [
        Vertex(0, [0, 0], 0),
        Vertex(1, [1, 0], 1),
        Vertex(2, [1, 1], 2),
        Vertex(3, [0, 1], 3),
    ]
    f = [Face(0, 0), Face(1, 1)]
    e = [
        Edge(0, 0, 1, 0, None, 3, 4, None, None),
        Edge(1, 1, 2, 1, None, 4, 2, None, None),
        Edge(2, 2, 3, 1, None, 1, 4, None, None),
        Edge(3, 3, 0, 0, None, 4, 0, None, None),
        Edge(4, 3, 1, 1, 0, 2, 1, 0, 3),
    ]

    we = WingedEdge(v, f, e)

    for face in we.faces:
        print(f"Vértices adjacentes a face {face.id}:")
        v = we.get_face_vertices(face.id)
        print(v)

    for vertex in we.vertices:
        print(f"Vértices adjacentes ou vértice {vertex.id}:")
        v = we.get_next_vertex(vertex.id)
        print(v)

    hv.save(we.plot_edges(), "plot_edges.html")
