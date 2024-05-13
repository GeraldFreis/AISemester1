# so viterbi takes in the path to the input file as first argument
from sys import argv
input_file = argv[1]


"""Function definitions"""
def read_in(filename: str)->list:...



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

# now we read in the input file
input_values = read_in(filename=input_file)
# print(input_values)

