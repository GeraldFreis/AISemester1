# so viterbi takes in the path to the input file as first argument
from sys import argv
input_file = argv[1]
import numpy as np
from numpy import ones, zeros

"""Defining the functions I want to use"""

# the typical read in function first as always
def read_in(filename: str)->tuple:
    """Reading in the file because hmm maybe that is neccessary lmao"""
    with open(filename, 'r') as file:
        file_lines = file.readlines()
        r, c, depth = map(int, file_lines[0].split()) # because we now have a 3rd parameter
        # reading the grid in, idc about readability anymore list comprehension is how i do things now
        
        # the map is segmented into fractions that represent depth so we just do what we did for the normal viteerbi
        # but we do it n times for n 3rd dimension
        grid = [[[col for col in row.strip().split(" ")[d:(d+1)*(c)]] for d in range(depth)] for row in file_lines[1:1+r]]

        n = int(file_lines[1+r])
        # reading the n observations in as a list of base 2 integers
        observations = [int(observation, 2) for observation in file_lines[2+r:2+r+n]]
        error_rate = float(file_lines[2+r+n])
    
        return (r, c, depth, grid, n, observations, error_rate)

def transition_matrix(mapping_of_grid_to_matrix, mapping_of_matrix_to_grid, K):
    """Making the transition matrix of the map
        for each entry in the K x K matrix we have the probability of 1/N where N is the number of adjacent traversible squares
    """
    Tm = zeros((K, K))

    for i, (x, y, d) in enumerate(mapping_of_matrix_to_grid): # for each traversible index 
        # I want to compute their traversible neighbours by checking if they are in the traversible set
        neighbours = [(x-1, y, d), (x+1, y, d), (x, y-1, d), (x, y+1, d), (x, y, d-1), (x, y, d+1)]
        valid_neighbours = [mapping_of_grid_to_matrix[(nx, ny, nd)] for (nx, ny, nd) in neighbours if (nx, ny, nd) in mapping_of_grid_to_matrix]
        # Tm[x][y] = 1/len(valid_neighbors) if len(valid_neighbors) > 0 else 0
        # getting the transition matrice
        for neighbour in valid_neighbours:
            Tm[i] [neighbour] = 1 / len(valid_neighbours)
    return Tm

def emission_matrix(mapping_of_grid_to_matrix, mapping_of_matrix_to_grid, error_rate, K):
    """Calculates the emission matrix from a mapping of each index to the map and a mapping of each position to an index
    """
    Em = zeros((K, 64))
    for i, (x, y, d) in enumerate(mapping_of_matrix_to_grid):

        # for each traversible index I want to get its emission probabilities for each combination of bits
        for n in range(64):
            bits = f"{n:06b}"
            observation = [int(j) for j in str(bits)]
            neighbours = [(x-1, y, d), (x+1, y, d), (x, y-1, d), (x, y+1, d), (x, y, d-1), (x, y, d+1)]
            valid_neighbours = [mapping_of_grid_to_matrix[(nx, ny, nd)] for (nx, ny, nd) in neighbours if (nx, ny, nd) in mapping_of_grid_to_matrix]
        #     # getting number of incorrect directions
            
            valid_expansion = [1 if (nx, ny, nd) in mapping_of_grid_to_matrix else 0 for (nx, ny, nd) in neighbours ]
            aligned_sensors = [1 if j == observation[x] else 0 for x, j in enumerate(valid_expansion)] # if each position in the observation and adjacent traversible squares align
            
            number_of_wrong_sensors = sum(aligned_sensors)
            Em[i][n] = ((1-error_rate) ** (6-number_of_wrong_sensors)) * (error_rate ** (number_of_wrong_sensors))
    return Em

def mapping_sets_because_input_grid_is_different_to_trellis_etc(r, c, depth,  grid):
    """For guidance refer to name of function"""
    map_to_index = {}
    index_to_map = []
    
    for i in range(r):
        for d in range(depth):
            for j in range(c):
                if grid[i][d][j] != "X": # if the current square is traversible
                    map_to_index[(i, j, d)] = len(index_to_map)
                    index_to_map.append((i, j, d))
    return (map_to_index, index_to_map)

def viterbi_forward(K, N, pi, Y, Tm, Em):
    # Initialize the trellis matrix
    T = len(Y)
    trellis = zeros((K, T))
    # Initialize the first column of the trellis matrix
    for i in range(K):
        trellis[i, 0] = pi[i] * Em[i, Y[0]]
        
    
    # Fill in the rest of the trellis matrix
    for j in range(1, T):
        for i in range(K):
            possible_states = [trellis[k, j-1] * Tm[k, i] * Em[i, Y[j]] for k in range(K)]
            # print((i,j))
            # print(possible_states);
            # print(max(possible_states))
            trellis[i, j] = max(possible_states)
    return trellis
"""Now actually doing everything inshallah"""
r,c,depth, grid,n,observation_list,epsilon = read_in(input_file)

# now getting the mapping sets
map_to_idx, idx_to_map = mapping_sets_because_input_grid_is_different_to_trellis_etc(r,c,depth, grid)

# now calculating each matrix
Tm = transition_matrix(map_to_idx, idx_to_map, len(idx_to_map))
Em = emission_matrix(map_to_idx, idx_to_map, epsilon, len(idx_to_map))
initial_probabilities = ones(len(idx_to_map)) / len(idx_to_map)

# calculating the trellis matrices
trellis = viterbi_forward(len(idx_to_map), 64, initial_probabilities, observation_list, Tm, Em)

# okay now I need to map the trellis back to the necessary matrix
maps = []  # List to store map representations
for t in range(n):
    map_rep = zeros((r, c, depth))
    for (x, y, d), i in map_to_idx.items(): # for each traversible point I want the current state's probability
        map_rep[x, y, d] = trellis[i, t]
        # print(trellis[i])
        # print(trellis[i])
    maps.append(map_rep)

print(maps[0])
np.savez("output.npz", *maps)