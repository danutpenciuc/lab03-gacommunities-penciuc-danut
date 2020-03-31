import ast
from random import randint, random
import numpy as np


class Community:
    def modularity(self, communities, param):
        noNodes = param['noNodes']
        mat = param['mat']
        degrees = param['degrees']
        noEdges = param['noEdges']
        M = 2 * noEdges
        Q = 0.0
        for i in range(0, noNodes):
            for j in range(0, noNodes):
                if communities[i] == communities[j]:
                    Q += (mat[i][j] - degrees[i] * degrees[j] / M)
        return Q * 1 / M

    def getPopulation(self, size, colors, cities, network):
        population = set()
        indexes = [i for i in range(1, colors + 1)]

        while population.__len__() < size:
            individual = []
            sameColorForAll = False

            for i in range(cities):
                position = randint(0, colors - 1)
                individual.append(indexes[position])

            for i in range(1, colors + 1):
                if individual.count(i) == len(individual):
                    sameColorForAll = True
                    break

            if not sameColorForAll:
                population.add(str(individual))

        return population

    def bestSolution(self, population, network):
        pop = list(population)
        best = pop[0]
        best = ast.literal_eval(best)
        for community in pop:
            community = ast.literal_eval(community)
            if self.modularity(community, network) > self.modularity(best, network):
                best = community
        return best

    def getProbabilityList(self, fitness):
        fitness = fitness.values()
        totalFit = float(sum(fitness))
        relativeFitness = [f / totalFit for f in fitness]
        probabilities = [sum(relativeFitness[:i + 1]) for i in range(len(relativeFitness))]
        return probabilities

    def selection(self, generation, fitness):
        generation = list(generation)
        probabilities = self.getProbabilityList(fitness)

        r = random()
        for (i, individual) in enumerate(generation):
            if r <= probabilities[i]:
                return ast.literal_eval(individual)

    def crossOver(self, left, right, network):
        # Get length of chromosome
        chromosome_length = len(left)

        # Pick crossover point, avoding ends of chromsome
        crossover_point1 = randint(1, chromosome_length - 1)
        crossover_point2 = randint(1, chromosome_length - 1)
        minn, maxx = min(crossover_point1, crossover_point2), max(crossover_point1, crossover_point2)

        # Create children. np.hstack joins two arrays
        child_1 = np.hstack((left[0:minn],
                             right[minn:maxx], left[maxx:]))
        child_2 = np.hstack((right[0:minn],
                             left[minn:maxx], right[maxx:]))
        child_1 = list(child_1)
        child_2 = list(child_2)
        if self.modularity(child_1, network) > self.modularity(child_2, network):
            return child_1
        return child_2

    def mutation(self, copil):
        p1 = randint(0, len(copil) - 1)
        p2 = randint(0, len(copil) - 1)
        copil[p1], copil[p2] = copil[p2], copil[p1]
        return copil

    def findComponents(self, size, iterations, colors, network, cities):
        population = self.getPopulation(size, colors, cities, network)
        best = self.bestSolution(population, network)
        index = 0
        while index < iterations:
            fitness = dict()
            for p in population:
                fitness[p] = self.modularity(ast.literal_eval(p), network)

            newPopulation = set()
            newPopulation.add(str(self.bestSolution(population, network)))

            while newPopulation.__len__() < population.__len__():
                first = self.selection(population, fitness)
                second = self.selection(population, fitness)

                result = self.crossOver(first, second, network)
                resultAfterMutation = self.mutation(result)

                newPopulation.add(str(resultAfterMutation))

            # we obtained a new generation
            index += 1
            population = newPopulation
            best = self.bestSolution(population, network)
            print(best)
            print(self.modularity(best, network))
        return best