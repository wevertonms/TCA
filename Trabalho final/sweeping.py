"""Malha de triângulo pelo algoritmo de varredura."""
import holoviews as hv
import numpy as np
from holoviews import opts

from jarvis_fc2d import pseudo_angle
from winged_edge import Edge, Face, Vertex, WingedEdge

hv.extension("bokeh", logo=False)


class Mesh:
    """Malha de triângulos."""

    def __init__(self, points):
        """Construtor.

        Args:
            points (array): lista de pontos.
        """
        self.points = sorted(points, key=lambda p: p[0])
        vertices = [Vertex(id=i, coords=p, edge=i) for i, p in enumerate(points)]
        edges = [Edge(id=0, v1=0, v2=1), Edge(id=1, v1=1, v2=2), Edge(id=2, v1=2, v2=0)]
        faces = [Face(id=0, edge=0)]
        v1 = points[1] - points[0]
        v2 = points[2] - points[0]
        if pseudo_angle(v2, v1) < 4:
            for edge in edges:
                edge.fccw = 0
                edge.pccw = (edge.id - 1) % 3
                edge.nccw = (edge.id + 1) % 3
        else:
            for edge in edges:
                edge.fcw = 0
                edge.pcw = (edge.id - 1) % 3
                edge.ncw = (edge.id + 1) % 3
        self.we = WingedEdge(vertices=vertices, edges=edges, faces=faces)

    def check_interception(self, point1, point2):
        """Checa se uma uma aresta entre dois pontos intercepta as outras.

        Args:
            point1 (numpy.array): coordenadas do ponto 1.
            point2 (numpy.array): coordenadas do ponto 2.

        Returns:
            bool: True se há intersecção, False caso contrário.
        """
        new_edge = point2 - point1
        for edge in self.we.edges:
            vector1 = self.points[edge.v1] - point1
            vector2 = self.points[edge.v2] - point1
            cross1 = np.cross(new_edge, vector1)
            cross2 = np.cross(new_edge, vector2)
            if cross1 * cross2 < 0:
                vector1 = self.points[edge.v2] - self.points[edge.v1]
                vector2 = point1 - self.points[edge.v1]
                vector3 = point2 - self.points[edge.v1]
                cross1 = np.cross(vector1, vector2)
                cross2 = np.cross(vector1, vector3)
                if cross1 * cross2 < 0:
                    return True
        return False

    def generate_mesh(self):
        """Gera a malha de triângulos."""
        for i in range(3, len(self.points)):
            point = self.points[i]
            for index in range(len(self.we.edges)):
                intercept = self.check_interception(point, self.points[index])
                if not intercept:
                    self.we.edges.append(Edge(id=len(self.we.edges), v1=i, v2=index))

    def full_plot(self):
        """Gera um plot completo da malha de triângulos.

        Returns:
            holoviews: plot.
        """
        return self.we.plot_vertices() * self.we.plot_edges()


if __name__ == "__main__":
    n_verts = 10
    points = np.random.randint(1, 100, (n_verts, 2))
    mesh = Mesh(points)
    mesh.generate_mesh()
    mesh.full_plot()
