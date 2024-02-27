import sys
from collections import deque


given_map_file = sys.argv[1]
algo = sys.argv[2]
heuristic = sys.argv[3] if algo == "astar" else None

possible_directions = [(-1,0), (1,0), (0,-1), (0,1)] # left down up right

"""Function Definitions"""
def reading_map(filename: str)->tuple: ...

def bfs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:...

def ucs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:...

def astar(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list,
        heuristic: str)->None:...

"""Function Implementations"""

def reading_map(filename: str)->tuple:
    with open(filename, 'r') as f:
        rows, cols = map(int, f.readline().split())
        start_row, start_col = map(int, f.readline().split())
        end_row, end_col = map(int, f.readline().split())
        grid = [list(map(str, f.readline().split())) for _ in range(rows)]
    return (rows, cols, (start_row-1, start_col-1), (end_row-1, end_col-1), grid)


# def is_surrounded(coords: (int, int), mapple: list)->bool:
#     """This function checks if we are currently surrounded by x's"""
#     if()

def bfs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:
    """This is my implementation of the bfs algorithm"""

    # first we need a queue to plop items in
    q = deque()
    visited = list() # this  will contain (int, int) referring to the points that we have visited thus far
    path = list() # this will hold the current path we have travelled

    # adding the first point into the queue and the 
    q.append([start[0], start[1], 0, [start]]) 

    while q: # while we still have things in the queue and we haven't visited all nodes
        current_row, current_column, cost, current_path = q.popleft()
        if((current_row, current_column) not in visited):
            print((current_row, current_column))
            # checking if we have reached the end
            if(current_row == end[0] and current_column == end[1]):
                path = current_path
                print(path)
                break;

            possible_cost = list()

            for d_row, d_col in possible_directions:
                new_row, new_col = current_row + d_row, current_column + d_col
                print(f"{new_row < n} {new_row}"); print(f"{new_col < m} {new_col}")
                if 0 <= new_row and new_row < n and 0 <= new_col and new_col < m and mapple[new_row][new_col] != 'X' and (new_row, new_col) not in visited:
                    new_cost = cost + int(mapple[new_row][new_col])
                    new_path = current_path + [(new_row, new_col)]
                    possible_cost.append(([d_row, d_col], new_cost))        

            min_cost = float('inf'); min_idx = 0
            for idx, ((r,c), cost) in enumerate(possible_cost):
                if(cost < min_cost):
                    min_cost = cost
                    min_idx = idx

            visited.append((current_row, current_column))

            if(len(possible_cost) > 0):
                q.append((current_row+possible_cost[min_idx][0][0], current_column+possible_cost[idx][0][1], cost+min_cost, new_path+[(possible_cost[idx][0][0], possible_cost[idx][0][1])]))
                if(((current_row + possible_cost[min_idx][0][0]) == end[0]) and ((current_column + possible_cost[min_idx][0][1]) == end[1])):
                    path = current_path + (end)
                    break;
    for r, c in path:
        mapple[r][c] = '*'

    for row in mapple:
        print(' '.join(map(str, row)))




n,m, start, end, given_map = reading_map(given_map_file)
if(algo == "bfs"): bfs(n, m, start, end, given_map)
elif(algo == "ucs"): ucs(n,m, start, end, given_map)
elif(algo == "astar"): astar(n,m,start,end,given_map,heuristic)
