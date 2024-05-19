from sys import argv
import numpy as np
from numpy import zeros, ones


# first we need the input_file_address

input_filepath = argv[1]

# okay now we can do all we need

# possible directions are north south west east
possible_directions = [(-1, 0),  (1, 0), (0, -1), (0, 1)] # by adding this to any position in the grid (we get the traversible directions)


"""Function definitions"""

def read_in(filename: str)->list:...

def viterbi(observations, error_rate, emission_matrix, transition_matrix ): ...


"""Function implementations"""

def read_in(filename: str)->list:
    """Takes filename returns a list of lists
    Return:
        List of points ->points are tab separated from the file
    """
    with open(filename, 'r') as f:
        rows, cols = map(int, f.readline().split()) # first line is row, cols

        # now reading in the map
        grid = list()

        for _ in range(rows):
            grid.append(list(map(str, f.readline().split())))
        
        sensor_observations = int(f.readline())
        observed_values_list = [int(f.readline()) for _ in range(sensor_observations)]
        error_rate = float(f.readline())


        return (rows, cols, grid, observed_values_list, error_rate)


def viterbi_forward(K, N, pi, Y, Tm, Em):
    # Initialize the trellis matrix
    T = len(Y)
    trellis = np.zeros((K, T))
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

# Read input from file
with open(input_filepath, 'r') as file:
    lines = file.readlines()
    rows, cols = map(int, lines[0].split())
    map_data = [[c for c in row.strip().split(" ")] for row in lines[1:1+rows]]
    num_observations = int(lines[1+rows])
    # observations = [str(obs).strip() for obs in lines[2+rows:2+rows+num_observations]]
    observations = [int(obs, 2) for obs in lines[2+rows:2+rows+num_observations]]

    sensor_error_rate = float(lines[2+rows+num_observations])

# Map positions to state indices
map_to_index = {}
index_to_map = []
for i in range(rows):
    for j in range(cols):
        if map_data[i][j] != "X":
            map_to_index[(i, j)] = len(index_to_map)
            index_to_map.append((i, j))

K = len(index_to_map)

# Define initial probabilities, transition matrix, and emission matrix
pi = np.ones(K) / K
Tm = np.zeros((K, K))

# Fill the transition matrix Tm
Tm = np.zeros((K, K))
Em = np.zeros((K, num_observations))

for i, (x, y) in enumerate(index_to_map):
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    valid_neighbors = [map_to_index[(nx, ny)] for (nx, ny) in neighbors if (nx, ny) in map_to_index]
    # Tm[x][y] = 1/len(valid_neighbors) if len(valid_neighbors) > 0 else 0
    # getting the transition matrice
    for neighbor in valid_neighbors:
        Tm[i] [neighbor] = 1 / len(valid_neighbors)

Em = np.zeros((K, 16))
for i, (x, y) in enumerate(index_to_map):
    for n in range(16):
        bits = f"{n:04b}"
        error_prob = sensor_error_rate ** bits.count('1') * (1 - sensor_error_rate) ** bits.count('0')
        Em[i][n] = error_prob

        observation = [int(j) for j in str(bits)]
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        valid_neighbors = [map_to_index[(nx, ny)] for (nx, ny) in neighbors if (nx, ny) in map_to_index]
    #     # getting number of incorrect directions
        valid_expansion = [1 if (nx, ny) in map_to_index else 0 for (nx, ny) in neighbors ]
        aligned_sensors = [1 if j == observation[x] else 0 for x, j in enumerate(valid_expansion)] # if each position in the observation and adjacent traversible squares align
        number_of_wrong_sensors = sum(aligned_sensors)
        Em[i][n] = ((1-sensor_error_rate) ** (4-number_of_wrong_sensors)) * (sensor_error_rate ** (number_of_wrong_sensors))

# Run Viterbi algorithm
trellis = viterbi_forward(K, 16, pi, observations, Tm, Em)

# Output map representations to file
maps = []  # List to store map representations
for t in range(len(observations)):
    map_rep = np.zeros((rows, cols))
    for (x, y), i in map_to_index.items():
        map_rep[x, y] = trellis[i, t]
        # print(trellis[i])
    maps.append(map_rep)

# print(maps[0])
np.savez("output.npz", *maps)