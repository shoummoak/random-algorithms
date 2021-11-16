import TSP_GA
import TSP_SA
import random

# ignore build_graph()


def build_graph():

    f = open('input.txt', 'r')
    # read number of nodes
    n_nodes = int(f.readline())
    # construct the matrix
    matrix = [[0 for v in range(n_nodes)] for u in range(n_nodes)]

    # parse distances and fill the matrix
    line = f.readline().strip()
    while line != '0':
        num_list = [int(num) for num in line.split()]
        matrix[num_list[0]-1][num_list[1]-1] = num_list[2]
        line = f.readline().strip()

    f.close()

    # if edge(u,v) = 0, there is no path there
    # therefore, edge(u,v) = INFINITY
    for u in range(n_nodes):
        for v in range(n_nodes):
            if matrix[u][v] == 0:
                matrix[u][v] = 100000

    return matrix


def build_graph2(vertices):

    # construct the matrix
    matrix = [[0 for v in range(vertices)] for u in range(vertices)]

    for u in range(vertices):
        for v in range(vertices):
            if u == v:
                matrix[u][v] = 0
            else:
                matrix[u][v] = int(random.random() * 100)

    return matrix


def print_matrix(matrix):
    for i in matrix:
        print(i)


# check the matrix
matrix = build_graph2(20)
print('MATRIX')
print_matrix(matrix)
print()

# GA
# pop = TSP_GA.TSP_GA(10, 200, matrix)
# pop.set_params(iterations=200)
# pop.train()

# SA
pop = TSP_SA.TSP_SA(matrix, T_max=200)
pop.run()

# # check2
# pop_print = [str(i) for i in pop.population]
# print(pop_print)
