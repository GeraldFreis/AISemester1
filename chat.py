import numpy as np

class Node:
    def __init__(self, point=None, label=None, left=None, right=None):
        self.point = point
        self.label = label
        self.left = left
        self.right = right

def build_kd_tree(points, labels, depth=0):
    n = len(points)
    if n == 0:
        return None
    k = len(points[0])  # Number of dimensions
    axis = depth % k

    # Sort points by the axis
    sorted_points = sorted(zip(points, labels), key=lambda x: x[0][axis])
    median = n // 2

    # Create node and construct subtrees
    node = Node(
        point=sorted_points[median][0],
        label=sorted_points[median][1],
        left=build_kd_tree([x[0] for x in sorted_points[:median]], [x[1] for x in sorted_points[:median]], depth + 1),
        right=build_kd_tree([x[0] for x in sorted_points[median+1:]], [x[1] for x in sorted_points[median+1:]], depth + 1)
    )
    return node
def make_tree(points:list, labels:list, depth=0):
    """Takes in a list of points and their respective labels and returns the root node"""
    if len(points) == 0: # if we don't have any points
        return None

    d = depth % len(points[0]) # modding current depth by M

    # Sort points by the cut (d)
    sorted_points = sorted(zip(points, labels), key=lambda x: x[0][d]) # I want to sort both together
    # because otherwise the order of their labels will not be maintained
    m = len(points) // 2

    # getting all points to the left of the median
    left_node = make_tree([x[0] for x in sorted_points[:m]], [x[1] for x in sorted_points[:m]], depth + 1)
    right_node = make_tree([x[0] for x in sorted_points[m+1:]], [x[1] for x in sorted_points[m+1:]], depth + 1)


    # Create node and construct subtrees
    node = Node(
        point=sorted_points[m][0],
        label=sorted_points[m][1],
        left=left_node,
        right=right_node
    )
    return node
def find_nearest(node, point, depth=0):
    if node is None:
        return float('inf'), None
    
    k = len(point)
    axis = depth % k

    next_branch = None
    opposite_branch = None

    if point[axis] < node.point[axis]:
        next_branch = node.left
        opposite_branch = node.right
    else:
        next_branch = node.right
        opposite_branch = node.left

    best_dist, best_label = find_nearest(next_branch, point, depth + 1)
    node_dist = np.sum((np.array(node.point) - np.array(point))**2)

    if node_dist < best_dist:
        best_dist = node_dist
        best_label = node.label

    if (point[axis] - node.point[axis])**2 < best_dist:
        dist, label = find_nearest(opposite_branch, point, depth + 1)
        if dist < best_dist:
            best_dist = dist
            best_label = label

    return best_dist, best_label

import sys
import csv

def read_in(filename: str)->list:
    """Takes filename returns a list of lists
    Return:
        List of points ->points are tab separated from the file
    """
    file = list()
    with open(filename, 'r') as f:
        tsv_file = csv.reader(f, delimiter="\t")
        next(tsv_file)
        for row in tsv_file:
            row = row[0].split(' ')
            row = [float(i) for i in row if i != '']
            # row = [float(i) for i in row]
            file.append(row)

    return file

def main(train_path, test_path, dimension):
    train_file = read_in(train_path)
    test_file = read_in(test_path)

    train_points = [i[:-1] for i in train_file]
    train_labels = [i[-1] for i in train_file]

    test_points = test_file

    tree = make_tree(train_points, train_labels, int(dimension))
    predictions = []

    for point in test_points:
        _, label = find_nearest(tree, point, int(dimension))
        predictions.append(label)

    for pred in predictions:
        print(int(pred))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python nn_kdtree.py [train] [test] [dimension]")
    else:
        _, train, test, dimension = sys.argv
        main(train, test, dimension)
