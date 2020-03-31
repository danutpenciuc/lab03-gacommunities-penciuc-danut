import os
from networkx import *


class Repository:
    def load_gml(self, fileName):
        net = {}
        communityGraph = read_gml(fileName, "id")
        matrix = nx.to_numpy_matrix(communityGraph)
        cities = len(matrix)
        net['noNodes'] = cities
        mat = []

        for i in range(cities):
            mat.append([])
            for j in range(cities):
                mat[i].append(0)
        for i in range(cities):
            for j in range(cities):
                mat[i][j] = matrix.item(i, j)

        net['mat'] = mat
        degrees = []
        noEdges = 0
        for i in range(cities):
            d = 0
            for j in range(cities):
                if mat[i][j] == 1:
                    d += 1
                if j > i:
                    noEdges += mat[i][j]
            degrees.append(d)
        net["noEdges"] = noEdges
        net["degrees"] = degrees
        return cities, net
