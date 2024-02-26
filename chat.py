import sys
from collections import deque

def bfs(map_file):
    # Read the map from the file
    with open(map_file, 'r') as f:
        rows, cols = map(int, f.readline().split())
        start_row, start_col = map(int, f.readline().split())
        end_row, end_col = map(int, f.readline().split())
        grid = [list(map(str, f.readline().split())) for _ in range(rows)]

    # Define the directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the start position and the path
    queue = deque([(start_row - 1, start_col - 1, 0, [(start_row - 1, start_col - 1)])])
    visited = set()
    min_cost = float('inf')
    min_path = []

    while queue:
        row, col, cost, path = queue.popleft()

        if row == end_row - 1 and col == end_col - 1:
            if cost < min_cost:
                min_cost = cost
                min_path = path
            continue

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col

            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != 'X' and (new_row, new_col) not in visited:
                new_cost = cost + int(grid[new_row][new_col])
                new_path = path + [(new_row, new_col)]
                queue.append((new_row, new_col, new_cost, new_path))
                visited.add((new_row, new_col))

    # Mark the path on the grid with asterisks
    for r, c in min_path:
        grid[r][c] = '*'

    # Print the grid with the path
    for row in grid:
        print(' '.join(map(str, row)))

    return min_cost

# Example usage# Example usage
print(bfs('t1.txt'))