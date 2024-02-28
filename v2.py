import sys
from collections import deque
import copy

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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the start position and the path
    queue = deque([(start[0], start[1], int(mapple[start[0]][start[1]]), [(start[0], start[1])])])
    visited = list(start)
    min_cost = float('inf')
    min_path = []
    cost_list = list()
    path_list = list()
    rows = n; cols = m;
    counter = 0
    while queue:
        if(counter == 40): break;
        
        row, col, cost, path = queue.popleft()
        # print((row, col, cost))
        if row == end[0] and col == end[1]:
            if cost < min_cost:
                min_cost = cost
                min_path = path
            else:
                counter += 1
            continue
        
        current_possibles = list()
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col


            if 0 <= new_row < rows and 0 <= new_col < cols and mapple[new_row][new_col] != 'X' and (new_row, new_col) not in path:
                new_cost = cost + int(mapple[new_row][new_col])
                new_path = path + [(new_row, new_col)]
                queue.append((new_row, new_col, new_cost, new_path))

    # Mark the path on the grid with asterisks
    if(len(min_path) >= 1):
        for r, c in min_path:
            mapple[r][c] = '*'

        # Print the grid with the path
        for row in mapple:
            print(' '.join(map(str, row)))
    else:
        print("null")

def ucs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    node = start
    frontier = deque([(node, mapple[node[0]][node[1]], list([node]))]) # [node, cost, path_list]
    explored = list(); path = list()
    while frontier:
        frontier = deque(sorted(frontier, key=lambda x:int(x[1])))
        node, cost, path_list = frontier.popleft()
        if(node[0] == end[0] and node[1] == end[1]):
            path = path_list
            break
        
        explored.append(node)

        for d in directions:
            child_row = node[0] + d[0]; child_col = node[1]+d[1]
            child = (child_row, child_col)

            child_path = copy.deepcopy(path_list); 

            if(child not in explored and child not in frontier and child not in child_path and child_row >= 0 and child_col >= 0 and child_row < n and child_col < m and mapple[child_row][child_col] != 'X'):
                child_path.append(child)
                frontier.append((child,int(mapple[child_row][child_col]), child_path))

            
    if(len(path) >= 1):
        for r, c in path:
            mapple[r][c] = '*'

        # Print the grid with the path
        for row in mapple:
            print(' '.join(map(str, row)))
    else:
        print("null")

def astar(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list,
        heuristic: str)->None:
    


n,m, start, end, given_map = reading_map(given_map_file)
if(algo == "bfs"): bfs(n, m, start, end, given_map)
elif(algo == "ucs"): ucs(n,m, start, end, given_map)
elif(algo == "astar"): astar(n,m,start,end,given_map,heuristic)
