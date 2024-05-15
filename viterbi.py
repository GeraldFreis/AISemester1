# so viterbi takes in the path to the input file as first argument
from sys import argv
input_file = argv[1]
import numpy as np


"""Function definitions"""
def read_in(filename: str)->list:...

def viterbi_forward(observations_list: list, error_rate: list, grid: list)->None:...

"""Okay so Now I am going to actually write the functions because I am lazy lol"""

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


# the probability function 
p_x = lambda x, d, e: pow((1-e), 4-d)*pow(e, d) 

# the trellis matrix is going to have zeros at all x values - as they are not traversible

# possible directions are north south west east
possible_directions = [(-1, 0),  (1, 0), (0, -1), (0, 1)] # by adding this to any position in the grid (we get the traversible directions)

def number_of_possible_directions(grid, index_i, index_j)->int:
    """Function returns the number of possible directions we can move"""
    traversible_directions = 0
    for direction in possible_directions:
        resulting_i = index_i + direction[0]
        resulting_j = index_j + direction[1]

        if(resulting_j < 0 or resulting_j < 0 or resulting_j >= len(grid[0]) or resulting_i >= len(grid)):
            continue;
        else:
            if(grid[resulting_i][resulting_j] != 'X'):
                traversible_directions += 1
    return traversible_directions


"""For the algorithm I need to take the transition matrix and emission matrix"""

def viterbi_forward(observations_list: list, error_rate: list, grid: list)->None:
    """Takes in the observations, error and grid and for each state prints the trellis matrix
    """
    # making the trellis matrix
    trellis = np.zeros((len(grid[0]), len(grid))) # n x m matrix (filled with zeros for non-traversible paths)



    return None


# now we read in the input file
input_values = read_in(filename=input_file)
# print(input_values)
# print(input_values[2])
# initial matrix is a uniform distribution to 1/k 
number_of_non_zeros = len([int(i) for j in input_values[2] for i in j if i != 'X'])

original_matrix = list()
for i in input_values[2]:
    row = list()
    for j in i:
        if(j != 'X'):
            row.append(float(1/number_of_non_zeros))
        else:
            row.append(0)
    original_matrix.append(row)




# making the transition matrix
transition_matrix = list()
for i in range(len(input_values[2])):
    row = list()
    for j in range(len(input_values[2][0])):
        # for each
        # we now need to find the number of neighbours that are traversible
        row.append(1/number_of_possible_directions(input_values[2], i, j) if input_values[2][i][j] != 'X' else 0)
    transition_matrix.append(row)

# Now that we have each matrix I can pass them into the algorithm and do as required

print(transition_matrix)