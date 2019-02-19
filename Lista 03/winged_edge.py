class Vertex:
    def __init__(self, id, coords, edge):
        self.id = id
        self.coords = coords
        self.adj_vertex = edge

    def __str__(self):
        return f"ID: {self.id}\n" + f"Coords: {self.coords}\n" + f"Edge: {self.adj_vertex}"


class Face:
    def __init__(self, id, edge):
        self.id = id
        self.af = edge

    def __str__(self):
        return f"ID: {self.id}\n" + f"Edge: {self.af}"


class Edge:
    def __init__(self, id, v1, v2, fccw, fcw, pccw, nccw, pcw, ncw):
        self.id = id
        self.v1 = v1
        self.v2 = v2
        self.fccw = fccw
        self.fcw = fcw
        self.pccw = pccw
        self.nccw = nccw
        self.pcw = pcw
        self.ncw = ncw

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            + f"Vertex 1: {self.v1}\n"
            + f"Vertex 2: {self.v2}\n"
            + f"Counter-clock-wise face: {self.fccw}\n"
            + f"Clock-wise face: {self.fcw}\n"
            + f"Previous counter-clock-wise edge: {self.pccw}\n"
            + f"Next counter-clock-wise edge: {self.nccw}\n"
            + f"Previous clock-wise edge: {self.pcw}\n"
            + f"Next clock-wise edge: {self.ncw}"
        )


class WingedEdge:
    def __init__(self, vertex, faces, edges):
        self.vextex = vertex
        self.faces = faces
        self.edges = edges

    def get_face_vertex(self, faceID):
        VEXTEX = []
        F = self.faces[faceID]
        A = self.edges[F.af]
        proxima_Aresta = A
        while True:
            if F.id == proxima_Aresta.fccw:
                VEXTEX.append(proxima_Aresta.v1)
                proxima_Aresta = self.edges[proxima_Aresta.nccw]
            else:
                VEXTEX.append(proxima_Aresta.v2)
                proxima_Aresta = self.edges[proxima_Aresta.ncw]
            if proxima_Aresta.id == A.id:
                break
        return VEXTEX

    def get_next_vertex(self, vertexID):
        VEXTEX = []
        V = self.vextex[vertexID]
        A = self.edges[V.adj_vertex]
        proxima_Aresta = self.edges[V.adj_vertex]
        while True:
            if V.id == proxima_Aresta.v1:
                VEXTEX.append(proxima_Aresta.v2)
                if proxima_Aresta.pccw != None:
                    proxima_Aresta = self.edges[proxima_Aresta.pccw]
                else:
                    break
            else:
                VEXTEX.append(proxima_Aresta.v1)
                if proxima_Aresta.pcw != None:
                    proxima_Aresta = self.edges[proxima_Aresta.pcw]
                else:
                    break
            if proxima_Aresta.id == A.id:
                break
        return VEXTEX


# vertex = [vertex([1, 0, 0], 1),
#          vertex([1, 1, 0], 2),
#          vertex([1, 1, 1], 3),
#          vertex([1, 0, 1], 4),
#          vertex([0, 0, 0], 9),
#          vertex([0, 1, 0], 10),
#          vertex([0, 1, 1], 11),
#          vertex([0, 0, 1], 12)]
# faces = [face(1),
#         face(2),
#         face(10),
#         face(12),
#         face(1),
#         face(8)]
# edges = [edge(1, 2, 1, 5, 4, 2, 6, 5),
#         edge(2, 3, 1, 5, 4, 2, 6, 5),
#         edge(3, 4, 1, 5, 4, 2, 6, 5),
#         edge(4, 1, 1, 5, 4, 2, 6, 5),
#         edge(1, 5, 1, 5, 4, 2, 6, 5),
#         edge(2, 6, 1, 5, 4, 2, 6, 5),
#         edge(3, 7, 1, 5, 4, 2, 6, 5),
#         edge(4, 8, 1, 5, 4, 2, 6, 5),
#         edge(5, 6, 1, 5, 4, 2, 6, 5),
#         edge(6, 7, 1, 5, 4, 2, 6, 5),
#         edge(7, 8, 1, 5, 4, 2, 6, 5),
#         edge(8, 5, 1, 5, 4, 2, 6, 5)]

if __name__ == "__main__" :
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

    for i in range(len(we.faces)):
        v = we.get_face_vertex(i)
        print(v)

    for i in range(len(we.vextex)):
        v = we.get_next_vertex(i)
        print(v)
