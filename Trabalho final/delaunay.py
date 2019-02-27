"""Triângulação de Delaunay."""

from dataclasses import dataclass, field
from typing import List

import holoviews as hv
from bokeh.models import HoverTool
import numpy as np
import pandas as pd

from jarvis_fc2d import next_point, pseudo_angle
from winged_edge import Edge, Face, Vertex, WingedEdge

hv.extension("bokeh", logo=False)


class Mesh:
    """Malha de triângulos."""

    def __init__(self, points):
        """Construtor.
        
        Args:
            points (array): lista de pontos.
        """
        # Ordena os pontos po ordenda (y)
        self.points = sorted(points, key=lambda p: p[1])
        self.vertex_list = {}
        # Adiciona o ponto de menor ordenada ao triângulo inicial
        coords = np.array(self.points[0])
        self.vertex_list[0] = Vertex(0, coords, 0)
        # Acha a primeira aresta do fecho convexo e adiciona ao triângulo
        direction = [1.0, 0.0]
        second_point = next_point(self.points, 0, direction)
        coords = np.array(self.points[second_point])
        self.vertex_list[second_point] = Vertex(second_point, coords, 0)
        # OBS: uma vez que a função find_vertex_for_edge procura vértices no
        # semi-plano que não contém o triângulo, há uma inversão da ordens dos
        # vértices da primeira aresta que permite usar a tal função neste caso
        edge0 = Edge(id=0, v1=second_point, v2=0, fccw=0, fcw=None, pccw=2, nccw=1)
        third_point = self.find_vertex_for_edge(edge0)
        self.we = WingedEdge(self.vertex_list, [Face(id=0, edge=0)], [edge0])
        self.update_winged_edge(third_point, edge0)
        # Inverte a conectividade da aresta
        edge0.v1, edge0.v2 = edge0.v2, edge0.v1
        data = {"id": [], "x": [], "y": []}
        for index, point in enumerate(self.points):
            data["id"].append(index)
            data["x"].append(point[0])
            data["y"].append(point[1])
        data = pd.DataFrame(data)
        tooltips = [("id", "@id"), ("(x,y)", "(@x, @y)")]
        hover = [HoverTool(tooltips=tooltips)]
        max_x, min_x = max(data["x"]), min(data["x"])
        max_y, min_y = max(data["y"]), min(data["y"])
        xlim = (min_x - (max_x - min_x) / 10, max_x + (max_x - min_x) / 10)
        ylim = (min_y - (max_y - min_y) / 10, max_y + (max_y - min_y) / 10)
        self.plot = hv.Points(data, ["x", "y"], label="Vértices").opts(
            size=10,
            color="black",
            tools=hover,
            xlim=xlim,
            ylim=ylim,
            width=1400,
            height=750,
            show_grid=True,
        )
        self.add_face_to_plot(self.we.faces[0])

    def angle_with_edge2(self, point, edge):
        """Determina o ângulo entre um ponto e uma aresta.
        
        Args:
            point (list): coordendas do ponto.
            edge (Edge): aresta.
        
        Returns:
            float: ângulo entre o ponto e a aresta.
        """
        direction = self.vertex_list[edge.v2].coords - self.vertex_list[edge.v1].coords
        vector1 = point - self.vertex_list[edge.v1].coords
        angle1 = pseudo_angle(direction, vector1)
        vector2 = point - self.vertex_list[edge.v2].coords
        angle2 = pseudo_angle(direction, vector2)
        internal_angle = angle2 - angle1
        return internal_angle

    def angle_with_edge(self, point, edge):
        """Determina o ângulo entre um ponto e uma aresta.
        
        Args:
            point (list): coordendas do ponto.
            edge (Edge): aresta.
        
        Returns:
            float: ângulo entre o ponto e a aresta.
        """
        direction = self.vertex_list[edge.v2].coords - self.vertex_list[edge.v1].coords
        vector1 = point - self.vertex_list[edge.v1].coords
        vector2 = point - self.vertex_list[edge.v2].coords
        angle = (
            np.arccos(
                vector1 @ vector2 / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
            )
            * 180
            / np.pi
        )
        if pseudo_angle(direction, vector1) > 4:
            internal_angle = -angle
        else:
            internal_angle = angle
        # print(f"{point}: {real_angle:.3g}, {internal_angle:.3g}")
        return internal_angle

    def find_vertex_for_edge(self, edge):
        """Encontra o vértice que forma um triângulo de Delanouy com a dada aresta.
        
        Args:
            edge (Edge): aresta.
        
        Returns:
            array: coordenadas do ponto.
        """
        max_angle = 0
        next_vertex = None
        for point in self.points:
            if point not in [self.points[edge.v1], self.points[edge.v2]]:
                angle = self.angle_with_edge(point, edge)
                if angle > max_angle:
                    max_angle = angle
                    next_vertex = point
                elif angle == max_angle and angle > 0:
                    new_edge1 = Edge(id=None, v1=edge.v1, v2=self.points.index(point))
                    new_edge2 = Edge(id=None, v1=edge.v2, v2=self.points.index(point))
                    if new_edge1 in self.we.edges:
                        existing_edge = self.we.edges[self.we.edges.index(new_edge1)]
                        if point == self.points[existing_edge.v1]:
                            next_vertex = self.points[existing_edge.v1]
                        else:
                            next_vertex = self.points[existing_edge.v2]
                    elif new_edge2 in self.we.edges:
                        existing_edge = self.we.edges[self.we.edges.index(new_edge2)]
                        if point == self.points[existing_edge.v1]:
                            next_vertex = self.points[existing_edge.v1]
                        else:
                            next_vertex = self.points[existing_edge.v2]

        return next_vertex

    def add_face_to_plot(self, face):
        """Adiciona uma face ao plot. Função mais útil durante o debugging.
        
        Args:
            face (wingededge.Face): face.
        """
        vertices = self.we.get_face_vertices(face.id)
        data = {"x": [], "y": []}
        for vertex_id in [*vertices, vertices[0]]:
            coords = self.we.vertices[vertex_id].coords
            data["x"].append(coords[0])
            data["y"].append(coords[1])
        self.plot *= hv.Curve(data, "x", "y", label=f"Face {face.id}")

    def generate_mesh(self):
        """Gera a malha de triângulo pela algoritmo de Delaunay."""
        face_queue = list(self.we.faces)
        while face_queue:
            face = face_queue[0]
            face_queue.remove(face)  # Retira a última face da fila
            free_edges = self.we.get_face_edges(face.id)[1:]
            for edge_id in free_edges:
                if self.we.edges[edge_id].fcw is not None:
                    # Se a aresta já tem as duas faces definidas, fim de papo para ela
                    continue
                point = self.find_vertex_for_edge(self.we.edges[edge_id])
                if point is not None:
                    self.update_winged_edge(point, self.we.edges[edge_id])
                    # Adiciona a última face à fila
                    face_queue.append(self.we.faces[-1])
                    self.add_face_to_plot(self.we.faces[-1])
                    # hv.save(self.plot, "plot.html")

    def update_winged_edge(self, point, current_edge):
        """Atualiza a estrututa winged-edge.
        
        Args:
            point (array): coordenadas no nodo vérttice.
            current_edge (Edge): aresta de referências.
        """
        point_id = self.points.index(point)
        num_faces = len(self.we.faces)
        self.we.vertices[point_id] = Vertex(
            point_id, np.array(point), len(self.we.edges)
        )
        new_edge1 = Edge(
            id=len(self.we.edges),
            v1=current_edge.v1,
            v2=point_id,
            fccw=num_faces,
            pccw=current_edge.id,
            nccw=len(self.we.edges) + 1,
        )
        try:  # Se new_edge1 já estiver na estrutura de dados
            new_edge1_id = self.we.edges.index(new_edge1)
            self.we.edges[new_edge1_id].fcw = num_faces
            self.we.edges[new_edge1_id].ncw = current_edge.id
            self.we.edges[new_edge1_id].pcw = len(self.we.edges)
        except:  # Se new_edge1 não estiver na estrutura de dados
            self.we.edges.append(new_edge1)
            new_edge1_id = len(self.we.edges) - 1
        new_edge2 = Edge(
            id=len(self.we.edges),
            v1=point_id,
            v2=current_edge.v2,
            fccw=num_faces,
            pccw=new_edge1_id,
            nccw=current_edge.id,
        )
        try:  # Se new_edge1 já estiver na estrutura de dados
            new_edge2_id = self.we.edges.index(new_edge2)
            self.we.edges[new_edge2_id].fcw = num_faces
            self.we.edges[new_edge2_id].pcw = current_edge.id
            self.we.edges[new_edge2_id].ncw = len(self.we.edges) - 1
            if self.we.edges[new_edge1_id].pcw is None:  # new_edge1 foi criada agora
                self.we.edges[new_edge1_id].nccw = new_edge2_id
            else:  # new_edge1 já existia
                self.we.edges[new_edge1_id].pcw = new_edge2_id
        except:
            self.we.edges.append(new_edge2)
            new_edge2_id = len(self.we.edges) - 1
        # Atualiza a conectividade da aresta atual
        current_edge.ncw = new_edge2_id
        current_edge.pcw = new_edge1_id
        current_edge.fcw = num_faces
        self.we.faces.append(Face(num_faces, current_edge.id))


if __name__ == "__main__":
    points = [
        [4, 8],
        [3, 4],
        [7, 6],
        [10, 9],
        [11, 10],
        [6, 6],
        [3, 10],
        [3, 1],
        [4, 4],
        [11, 6],
        [10, 7],
        [2, 6],
        [10, 8],
        [6, 1],
        [5, 3],
    ]
    mesh = Mesh(points)
    mesh.generate_mesh()
    hv.save(mesh.plot, "plot.html")
