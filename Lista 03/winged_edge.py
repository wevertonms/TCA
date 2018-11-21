class vertex:
   def __init__(self, id, coords, edge):
      self.id = id
      self.coords = coords
      self.av = edge


class face:
   def __init__(self, id, edge):
      self.id = id
      self.af = edge


class edge:
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


class winged_edge:
   def __init__(self, vertex, faces, edges):
      self.v = vertex
      self.f = faces
      self.e = edges

   def getFaceVertex(self, faceID):
      VEXTEX = []
      F = self.f[faceID]
      A = self.e[F.af]
      proxima_Aresta = A
      while True:
         if F.id == proxima_Aresta.fccw:
            VEXTEX.append(proxima_Aresta.v1)
            proxima_Aresta = self.e[proxima_Aresta.nccw]
         else:
            VEXTEX.append(proxima_Aresta.v2)
            proxima_Aresta = self.e[proxima_Aresta.ncw]
         if proxima_Aresta.id == A.id:
            break
      return VEXTEX

   def getNextVertex(self, vertexID):
      VEXTEX = []
      V = self.v[vertexID]
      A = self.e[V.av]
      proxima_Aresta = self.e[V.av]
      while True:
         if V.id == proxima_Aresta.v1:
            VEXTEX.append(proxima_Aresta.v2)
            if proxima_Aresta.pccw != None:
               proxima_Aresta = self.e[proxima_Aresta.pccw]
            else:
               break
         else:
            VEXTEX.append(proxima_Aresta.v1)
            if proxima_Aresta.pcw != None:
               proxima_Aresta = self.e[proxima_Aresta.pcw]
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

v = [vertex(0, [0, 0], 0),
     vertex(1, [1, 0], 1),
     vertex(2, [1, 1], 2),
     vertex(3, [0, 1], 3)]
f = [face(0, 0),
     face(1, 1)]
e = [edge(0, 0, 1, 0, None, 3, 4, None, None),
     edge(1, 1, 2, 1, None, 4, 2, None, None),
     edge(2, 2, 3, 1, None, 1, 4, None, None),
     edge(3, 3, 0, 0, None, 4, 0, None, None),
     edge(4, 3, 1, 1,    0, 2, 1,    0,    3)]

WE = winged_edge(v, f, e)

for i in range(len(WE.f)):
   v = WE.getFaceVertex(i)
   print(v)

for i in range(len(WE.v)):
   v = WE.getNextVertex(i)
   print(v)
