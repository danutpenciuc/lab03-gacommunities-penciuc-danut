import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings

import os

from main.community import Community
from main.repository import Repository


def run():
    while True:
        repo = Repository()
        community = Community()
        populationSize = int(input('Population size: '))
        numberOfIterations = int(input('Number of iterations: '))

        print('1. krebs\n2. dolphins\n3. karate\n4. football')

        option = int(input())
        crtDir = os.getcwd()
        if option == 1:
            filePathGML = os.path.join(crtDir, 'krebs.gml')
        elif option == 2:
            filePathGML = os.path.join(crtDir, 'dolphins.gml')
        elif option == 3:
            filePathGML = os.path.join(crtDir, 'karate.gml')
        elif option == 4:
            filePathGML = os.path.join(crtDir, 'football.gml')

        cities, network = repo.load_gml(filePathGML)

        warnings.simplefilter('ignore')

        bestSolution = community.findComponents(populationSize, numberOfIterations, cities, network, cities)
        print('\nCea mai buna este ' + str(bestSolution))
        print('fitness: ' + str(community.modularity(bestSolution, network)))

        A = np.matrix(network["mat"])
        G = nx.from_numpy_matrix(A)
        pos = nx.spring_layout(G)  # compute graph layout
        plt.figure(figsize=(10, 10))  # image is 8 x 8 inches
        nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu, node_color=bestSolution)
        nx.draw_networkx_edges(G, pos, alpha=0.3)
        plt.show(G)


run()
