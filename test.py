import numpy as np

file = np.load("./assignment3-test-cases\op5.npz", mmap_mode='r')
print(file['arr_0'])

file = np.load("output.npz", mmap_mode='r')
print(file['arr_0'])