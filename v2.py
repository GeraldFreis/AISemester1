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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the start position and the path
    queue = deque([(start[0], start[1], 0, [(start[0], start[1])])])
    visited = list(start)
    min_cost = float('inf')
    min_path = []
    rows = n; cols = m;

    while queue:
        print(queue)
        row, col, cost, path = queue.popleft()

        if row == end[0] and col == end[1]:
            if cost < min_cost:
                min_cost = cost
                min_path = path
            continue
        
        current_possibles = list()
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col

            if 0 <= new_row < rows and 0 <= new_col < cols and mapple[new_row][new_col] != 'X' and (new_row, new_col) not in visited and (new_row, new_col) not in path:
                new_cost = cost + int(mapple[new_row][new_col])
                new_path = path + [(new_row, new_col)]
                queue.append((new_row, new_col, new_cost, new_path))
                # visited.append((new_row, new_col))
            
                current_possibles.append((new_row, new_col, new_cost, new_path))
        
        if(len(current_possibles) > 0):
            print("True")
            min_one = sorted(current_possibles, key=lambda x:x[2], reverse=False)
            queue.append(min_one[0])
            visited.append((min_one[0][0], min_one[0][1]))
        else:
            print("Not True")
            for d_row, d_col in directions:
                new_row, new_col = row + d_row, col + d_col

                if 0 <= new_row < rows and 0 <= new_col < cols and mapple[new_row][new_col] != 'X' and (new_row, new_col) not in visited:
                    new_cost = cost + int(mapple[new_row][new_col])
                    new_path = path + [(new_row, new_col)]
                    queue.append((new_row, new_col, new_cost, new_path))
                    visited.append((new_row, new_col))
                
                    current_possibles.append((new_row, new_col, new_cost, new_path))

    # Mark the path on the grid with asterisks
    for r, c in min_path:
        mapple[r][c] = '*'

    # Print the grid with the path
    for row in mapple:
        print(' '.join(map(str, row)))




n,m, start, end, given_map = reading_map(given_map_file)
if(algo == "bfs"): bfs(n, m, start, end, given_map)
elif(algo == "ucs"): ucs(n,m, start, end, given_map)
elif(algo == "astar"): astar(n,m,start,end,given_map,heuristic)
