# imports
import random
import math


class TSP_GA:

    def __init__(self, chrom_size, pop_size, graph):
        self.chrom_size = chrom_size
        self.pop_size = pop_size
        self.matrix = graph
        self.population = []
        self.best_routes = []
        self.set_params()

    def set_params(self, iterations=100, elitism_rate=0.1, mutation_rate=0.02):
        self.mutation_rate = mutation_rate
        self.top_n_survival = math.ceil(self.pop_size * elitism_rate)
        self.iterations = iterations

    def train(self):

        # INITIALIZE POPULATION
        self.init_population()

        for _ in range(self.iterations):

            # calculate fitness of individuals
            for individual in self.population:
                individual.calc_fitness(self.matrix)

            # sort the individuals according to fitness
            self.population = sorted(
                self.population, key=lambda individual: individual.fitness)

            # print('POPULATION')
            # for i in self.population:
            #     print('{} || {}'.format(i.composition, i.fitness))

            # get the best generational individual
            self.best_routes.append(self.population[0])
            print('#{} best: {} || {}'.format(
                _+1, self.best_routes[-1].composition, self.best_routes[-1].fitness))

            # pop for the next generation
            self.population = self.populate_next_generation()

            # break
        best = min(self.best_routes, key=lambda individual: individual.fitness)
        print('BEST OVERALL: {} || {}'.format(best.composition, best.fitness))

    # create a population of chromosomes with randomized gene sequence
    def init_population(self):
        for _ in range(self.pop_size):
            # shuffle a list of vertices
            composition = [v for v in range(self.chrom_size)]
            random.shuffle(composition)
            # add to the population
            self.population.append(Individual(composition))

    # 20% of next_gen will be the best individuals of prev_gen
    def elitism(self):
        return self.population[:self.top_n_survival]

    # two types of crossover to choose between
    def crossover(self, parent1, parent2, single_point_crossover=True):

        if single_point_crossover:
            # single point swap crossover
            crossover_point = random.randint(0, self.chrom_size)
            child1, child2 = [], []
            child1.extend(parent1.composition[:crossover_point])
            child1.extend(parent2.composition[crossover_point:])
            child2.extend(parent2.composition[:crossover_point])
            child2.extend(parent1.composition[crossover_point:])

        else:
            # dual point swap crossover
            crossover_points = [random.randint(
                0, self.chrom_size), random.randint(0, self.chrom_size)]
            crossover_point_a = min(crossover_points)
            crossover_point_b = max(crossover_points)
            # produce two children from parents
            child1, child2 = [], []

            child1.extend(parent1.composition[:crossover_point_a])
            child1.extend(
                parent2.composition[crossover_point_a:crossover_point_b])
            child1.extend(parent1.composition[crossover_point_b:])

            child2.extend(parent2.composition[:crossover_point_a])
            child2.extend(
                parent1.composition[crossover_point_a:crossover_point_b])
            child2.extend(parent2.composition[crossover_point_b:])

        return child1, child2

    def mutation(self, child1, child2):
        for child in [child1, child2]:
            for v1_idx, v1 in enumerate(child):
                if random.random() <= self.mutation_rate:  # mutate / swap vertices
                    v2_idx = int(random.random() * self.chrom_size)
                    v2 = child[v2_idx]
                    child[v2_idx] = v1
                    child[v1_idx] = v2

        return child1, child2

    def populate_next_generation(self):

        next_gen = []

        # SELECTION - ELITISM
        elites = self.elitism()
        next_gen.extend(elites)

        # SELECTION - BRED OFFSPRING
        # remaining 80% will be offspring bred randomly among parents
        # of the top 40% of prev_gen
        # loop runs until next_gen is fully populated
        # two children per breeding, thus '/2' in loop
        top_40_n = math.ceil(0.4 * self.pop_size)
        for _ in range(math.ceil((self.pop_size - self.top_n_survival)/2)):
            parent1 = random.choice(self.population[:top_40_n])
            parent2 = random.choice(self.population[:top_40_n])

            # CROSSOVER
            child1, child2 = self.crossover(parent1, parent2)

            # MUTATION
            child1, child2 = self.mutation(child1, child2)

            next_gen.append(Individual(child1))
            next_gen.append(Individual(child2))

        if len(next_gen) > self.pop_size:
            del(next_gen[-1])

        return next_gen


class Individual:

    INF = 10000

    def __init__(self, composition):
        self.composition = composition
        self.size = len(composition)
        self.fitness = 0

    def __str__(self):
        return '({}, {})'.format(self.composition, self.fitness)

    def calc_fitness(self, matrix):

        self.fitness = 0
        # if all the vertices have not been visited
        if len(self.composition) > len(set(self.composition)):
            self.fitness = Individual.INF
        else:
            for i in range(1, self.size):
                self.fitness += matrix[self.composition[i-1]
                                       ][self.composition[i]]
            self.fitness += matrix[self.composition[-1]][self.composition[0]]
