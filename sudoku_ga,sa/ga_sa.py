import random
import numpy as np
import copy
import math

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def fitness(board):
    unique_numbers_row = [len(set(row)) for row in board]
    unique_numbers_col = [len(set(col)) for col in np.transpose(board)]

    unique_numbers_block = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            unique_numbers_block.append(len(set(block)))

    total_unique_numbers = sum(unique_numbers_row) + sum(unique_numbers_col) + sum(unique_numbers_block)

    return 1 / total_unique_numbers 

def crossover(parent1, parent2):
    crossover_point = random.randint(0, 8)
    child = copy.deepcopy(parent1)

    for i in range(9):
        if i < crossover_point:
            child[i] = parent1[i]
        else:
            child[i] = parent2[i]

    return child

def mutate(board, mutation_rate):
    for i in range(9):
        for j in range(9):
            if random.uniform(0, 1) < mutation_rate:
                new_number = random.randint(1, 9)
                while not is_valid(board, i, j, new_number):
                    new_number = random.randint(1, 9)
                board[i][j] = new_number

    return board

def simulated_annealing(initial_board, initial_temperature, cooling_rate, max_iterations):
    current_board = copy.deepcopy(initial_board)
    current_fitness = fitness(current_board)
    best_board = copy.deepcopy(current_board)
    best_fitness = current_fitness

    for iteration in range(max_iterations):
        temperature = initial_temperature / (1 + cooling_rate * iteration)

        new_board = mutate(copy.deepcopy(current_board), mutation_rate=0.1)
        new_fitness = fitness(new_board)

        acceptance_probability = math.exp((new_fitness - current_fitness) / temperature)

        if acceptance_probability > random.uniform(0, 1):
            current_board = copy.deepcopy(new_board)
            current_fitness = new_fitness

        if current_fitness > best_fitness:
            best_board = copy.deepcopy(current_board)
            best_fitness = current_fitness

    return best_board

def genetic_algorithm(initial_population_size, generations):
    population = [mutate([[0] * 9 for _ in range(9)], mutation_rate=0.2) for _ in range(initial_population_size)]

    for generation in range(generations):
        parents = sorted(population, key=fitness, reverse=True)[:2]
        parent1, parent2 = parents[0], parents[1]

        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate=0.2)

        index_to_replace = random.randint(0, len(population) - 1)
        population[index_to_replace] = child

    best_individual = max(population, key=fitness)
    return best_individual

sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


sudoku_solution_genetic = genetic_algorithm(initial_population_size=100, generations=1000)

sudoku_solution_sa = simulated_annealing(initial_board=sudoku_board, initial_temperature=100, cooling_rate=0.003, max_iterations=1000)

print("Sudoku Board:")
for row in sudoku_board:
    print(row)

print("\nGenetic Algorithm Solution:")
for row in sudoku_solution_genetic:
    print(row)

print("\nSimulated Annealing Solution:")
for row in sudoku_solution_sa:
    print(row)
