# first I need to read in the arguments
import sys
import csv
from statistics import median
from math import ceil, floor

train_filename = sys.argv[1]
test_filename = sys.argv[2]
dimensions = int(sys.argv[3])

# I now need to construct a KD tree from the training data (meaning I need to read in the training and testing data)

# Im gonna store everything as a list of lists because im lazy

def read_in(filename: str)->list:...

# then Im going to need to build the tree

def build_tree(points: list):...

# then I want to be able to classify each point

def classify_point(root, point: list)->None:...

"""Okay so Now I am going to actually write the functions because I am lazy lol"""

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

"""Need a node class"""

class Node():
    def __init__(self, d, val, point):
        self.d = d
        self.val = val
        self.point = point
    
# def median(l: list)->tuple:
#     # I want to take a list and not only return the median but also the index
#     return None

def euclidean_distance(node_a, node_b)->float:
    dist = 0
    for i in range(0, dimensions):
        dist += ((node_a[i] - node_b.point[i]) ** 2)
    return dist
    

def build_tree(points: list, depth: int = 0):
    """This takes in a list of points and builds a kdtree from it
    the KDtree is represented"""

    if len(points) == 0: return None
    elif len(points) == 1:
        d = depth % dimensions
        val = points[0][d] # getting value at dimension
        new_node = Node(d, val, points[0])
        new_node.left = None; new_node.right = None
        return new_node
    else:
        d = depth % dimensions
        points.sort(key=lambda x: x[d])
        middle = int(len(points) / 2)

        val = points[middle][d]# median value at the d'th dimension
        
        new_node = Node(d, val, points[middle]) # adding the new node with info
        
        new_node.left = build_tree([p for p in points if p[d] < val], depth+1)
        new_node.right = build_tree([p for p in points if p[d] > val], depth+1)

        return new_node
import heapq

def classify_point(root, point: list, heap, i = 0, tiebreaker = 1)->None:
    """Here we take a root node (from a KD tree) and a given point (list) and classify it
    based on its 1nn
    """
    k = 1
    if root is not None:
        dist_sq = euclidean_distance(point, root)
        dx = root.point[i] - point[i]
        if len(heap) < k:
            heapq.heappush(heap, (-dist_sq, tiebreaker, root))
        elif dist_sq < -heap[0][0]:
            heapq.heappushpop(heap, (-dist_sq, tiebreaker, root))
        i = (i + 1) % dimensions
        # Goes into the left branch, then the right branch if needed
        for b in (dx < 0, dx >= 0)[:1 + (dx * dx < -heap[0][0])]:
            if(b):
                classify_point(root.left, point, 
                    heap, i, (tiebreaker << 1) | b)
            else:
                classify_point(root.right, point, 
                    heap, i, (tiebreaker << 1) | b)
    if tiebreaker == 1:
        return [h for h in sorted(heap)][0][2].point[::-1]


train_file = read_in(train_filename)
train_root = build_tree(train_file)



test_file = read_in(test_filename)
print(classify_point(train_root, test_file[0], []))






