# IMPORTS
import random
import math


class TSP_SA:

    def __init__(self, graph, T_max=100):
        self.matrix = graph
        self.size = len(graph)
        self.T_max = T_max
        self.T = T_max

    def run(self):

        # start from a random configuration and calculate its energy
        current = self.init_random_config()
        current.calc_energy(self.matrix)

        # loop over the decreasing T
        for _ in range(1, self.T_max):

            print('#{}: {} || {}'.format(
                _, current.composition, current.energy))

            # decrease T
            self.update_T()
            # get a neighbor
            new = self.pick_neighbor(current)
            new.calc_energy(self.matrix)
            # allow a move if possible
            if random.random() <= TSP_SA.probability(current.energy, new.energy, self.T):
                current = new

    # get a random starting config for the algo
    def init_random_config(self):
        composition = [v for v in range(self.size)]
        random.shuffle(composition)
        return Config(composition, self.matrix)

    # decrement T by 1
    def update_T(self):
        self.T -= 1

    # find a neighbor
    def pick_neighbor(self, current):
        neighbor_composition = current.composition.copy()
        v1_idx = random.randint(0, self.size-1)
        v2_idx = random.randint(0, self.size-1)
        v1 = neighbor_composition[v1_idx]
        v2 = neighbor_composition[v2_idx]
        neighbor_composition[v1_idx] = v2
        neighbor_composition[v2_idx] = v1

        return Config(neighbor_composition, self.matrix)

    # get the probability of the move happening
    @classmethod
    def probability(cls, E_curr, E_new, T):
        delta_E = E_curr - E_new   # should the sign not be flipped?
        return 1 / (1 + pow(math.e, -delta_E/T))


# objects are permutations of the vertices for the TSP
class Config:

    INF = 10000

    def __init__(self, composition, matrix):
        self.composition = composition
        self.size = len(composition)
        self.energy = 0

    def __str__(self):
        return '({}, {})'.format(self.composition, self.energy)

    def calc_energy(self, matrix):

        self.energy = 0
        # if all the vertices have not been visited
        if len(self.composition) > len(set(self.composition)):
            self.energy = Config.INF
        else:
            for i in range(1, self.size):
                self.energy += matrix[self.composition[i-1]
                                      ][self.composition[i]]
            self.energy += matrix[self.composition[-1]][self.composition[0]]
