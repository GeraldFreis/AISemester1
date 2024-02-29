import sys
from collections import deque
import copy

given_map_file = sys.argv[1]
algo = sys.argv[2]
heuristic = sys.argv[3] if algo == "astar" else None

directions = [(-1,0), (1,0), (0,-1), (0,1)] # left down up right

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
    """Opening filename and returning a tuple of the information we need from the file"""
    with open(filename, 'r') as f:
        rows, cols = map(int, f.readline().split()) # first line is row, cols

        start_row, start_col = map(int, f.readline().split()) # second line is start row and col
        start = (start_row-1, start_col-1)

        dest_row, dest_col = map(int, f.readline().split()) # third line is goal row and col
        goal = (dest_row-1, dest_col-1)

        grid = [list(map(str, f.readline().split())) for _ in range(rows)] # making a grid of lines of rows and reading them all in

    return (rows, cols, start, goal, grid) # return (n, m, start tuple, end tuple, grid)

def bfs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:

    """This is my implementation of the bfs algorithm"""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # up, down, left and right

    # Initialize the queue with the start position, cost and the path
    queue = deque([(start[0], start[1], int(mapple[start[0]][start[1]]), [(start[0], start[1])])])

    visited = list(start) # 
    min_cost = float('inf')
    min_path = []
  
    rows = n; cols = m;
    counter = 0

    while queue: # while the queue is not empty 
        
        row, col, cost, path = queue.popleft() # popping the data from the queue
        # print((row, col, cost))

        if row == end[0] and col == end[1]: # if we are at the end point
            if cost < min_cost:
                min_cost = cost
                min_path = path
            else:
                counter += 1
            continue
        
        for d_row, d_col in directions: # for each (row, column) tuple in the directions list
            new_row, new_col = row + d_row, col + d_col


            if 0 <= new_row < rows and 0 <= new_col < cols and mapple[new_row][new_col] != 'X' and (new_row, new_col) not in visited:
                # if we are in the grid and not at an X and we have not visited the current node 
                new_cost = cost + int(mapple[new_row][new_col]) # cost is the path cost thus far alongside the current value

                new_path = copy.deepcopy(path) # deepcopy otherwise my laptop does some weird data sharing stuff
                new_path.append((new_row, new_col))

                visited.append((new_row, new_col)) # adding to visited
                queue.append((new_row, new_col, new_cost, new_path)) # adding to queue because thats bfs

    # Mark the path on the grid with asterisks
    if(len(min_path) >= 1):
        for r, c in min_path:
            mapple[r][c] = '*'

        # Print the grid with the path
        for row in mapple:
            print(' '.join(map(str, row)))

    else: # if we do not have a path, then we think there is none
        print("null")

def ucs(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list)->None:

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    node = start
    frontier = deque([(node, mapple[node[0]][node[1]], list([node]))]) # [node, cost, path_list]
    visited = list(); path = list()

    while frontier: # while the frontier is not empty

        frontier = deque(sorted(frontier, key=lambda x:int(x[1]))) # sorting the frontier because we need the minimum value to explore

        node, cost, path_list = frontier.popleft() # popping current valuees from the deque
        if(node[0] == end[0] and node[1] == end[1]): # are we at the end point and if so we want to put the path into where it needs to go
            path = path_list
            break
        
        visited.append(node) # adding the node to the visited list

        for d in directions: # for each direction tuple (up, down, left and right)
            child_row = node[0] + d[0]; child_col = node[1]+d[1]
            child = (child_row, child_col)

            child_path = copy.deepcopy(path_list);  # making a deep copy because python does some weird pointer problems

            # if(child not in visited and child not in frontier and child not in child_path and child_row >= 0 and child_col >= 0 and child_row < n and child_col < m and mapple[child_row][child_col] != 'X'):
            #     # if not visited and not in the frontier and in the map and not an obstruction we want to visit it
            #     child_path.append(child)
            #     frontier.append((child,int(mapple[child_row][child_col]), child_path))
            if(child not in visited and child not in frontier and child_row >= 0 and child_col >= 0 and child_row < n and child_col < m and mapple[child_row][child_col] != 'X'):
                # if not visited and not in the frontier and in the map and not an obstruction we want to visit it
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

from math import sqrt
def calculate_euclidean(node_1: tuple, node_2: tuple)->int:

    return sqrt(pow(node_1[0]-node_2[0], 2) + pow(node_1[1]-node_2[1], 2))

def calculate_manhatten(node_1: tuple, node_2: tuple)->int:
    return abs(node_1[0]-node_2[0]) + abs(node_1[1] - node_2[1])

def astar(n: int,
        m: int,
        start: (int, int),
        end: (int, int),
        mapple: list,
        heuristic: str)->None:

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    open_set = list([(start, mapple[start[0]][start[1]], list([start]))]) # making a set to hold what we have visited but not fully explored
    closed_set = list() # making a set to hold all those fully explored
    path = list()

    while open_set: # while there are things in the open_set
        if(heuristic == "euclidean"):
            sorted_opens = sorted(open_set, key=lambda x: (int(x[1])+calculate_euclidean(x[0], end) ) ) # sorting because again we want the optimal value
        else:
            sorted_opens = sorted(open_set, key=lambda x: (int(x[1])+calculate_manhatten(x[0], end) ) ) # sorting because again we want the optimal value

        # in this case the optimal value comes from the heuristic + cost
        node, cost, current_path = sorted_opens[0] # getting the best value in the top & cleaning it from the set

        current_path.append(node)

        if(node[0] == end[0] and node[1] == end[1]): # if we are at the end point we want the best path
            path = current_path
            break
        
        for d in directions: # for each direction (up, down, left and right)
            child_row = node[0] + d[0]; child_col = node[1]+d[1]
            child = (child_row, child_col)

            child_path = copy.deepcopy(current_path);  # deep copy because python has weird management problems
            if(child_row >= 0 and child_row < n and child_col >= 0 and child_col < m):

                if(mapple[child_row][child_col] != 'X' and child not in current_path):
                    if (child in open_set):
                        if(int(mapple[child_row][child_col]) <= cost): continue;
                    elif(child in closed_set):
                        if(int(mapple[child_row][child_col]) <= cost):
                            continue
                        open_set.append([child, mapple[child_row][child_col], child_path])
                        closed_set = [i for i in closed_set if i[0] != child]
                    else:
                        open_set.append([child, mapple[child_row][child_col], child_path])
   
    if(len(path) >= 1):
        for r, c in path:
            mapple[r][c] = '*'

        # Print the grid with the path
        for row in mapple:
            print(' '.join(map(str, row)))
    else:
        print("null")


n,m, start, end, given_map = reading_map(given_map_file)
if(algo == "bfs"): bfs(n, m, start, end, given_map)
elif(algo == "ucs"): ucs(n,m, start, end, given_map)
elif(algo == "astar"): astar(n,m,start,end,given_map,heuristic)
